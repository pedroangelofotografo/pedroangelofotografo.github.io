#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera o ficheiro fotos.js a partir do conteúdo da pasta fotos/.

Como funciona
-------------
Cada subpasta de fotos/ vira um álbum. Cada imagem dentro dela vira uma foto.
Ninguém precisa editar o index.html para acrescentar fotos: basta pôr o
ficheiro na pasta certa.

- Nome bonito e ordem dos álbuns  -> fotos/albuns.json (opcional)
- Capa do álbum                    -> ficheiro chamado "capa.*", se existir;
                                      senão, a primeira foto por ordem de nome
- Ordem das fotos                  -> ordem alfabética do nome do ficheiro
                                      (por isso vale a pena nomear 01, 02, 03...)

Uso:  python3 scripts/gerar-galeria.py
"""

import json
import os
import re
import sys
from urllib.parse import quote

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_FOTOS = os.path.join(RAIZ, "fotos")
CONFIG = os.path.join(PASTA_FOTOS, "albuns.json")
SAIDA = os.path.join(RAIZ, "fotos.js")

EXT_IMAGEM = {".jpg", ".jpeg", ".png", ".webp", ".avif", ".gif"}
EXT_VIDEO = {".mp4", ".webm", ".mov"}
EXT_COMPRIMIVEL = {".jpg", ".jpeg", ".webp"}  # formatos que sabemos reduzir com segurança

# Nomes tipo "{7780330C-60B2-4717-BE07-B975EA5B22CA}.png" são capturas de
# ecrã do Windows (Ctrl+Shift+S), quase nunca uma foto de verdade — ignoradas.
PADRAO_CAPTURA_ECRA = re.compile(
    r"^\{[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}\}"
)

# Pastas antigas com nome de cliente que já foram substituídas por uma versão
# renomeada (ex.: "andre luiz" -> "retratos"). Ficam aqui de propósito, como
# rede de segurança: mesmo que alguém esqueça de apagar a pasta antiga do
# computador, o site nunca vai publicar o nome do cliente por engano.
PASTAS_IGNORADAS = {
    "andre luiz",
    "militar 20 11 2025",
}

# Acima disto, a foto é comprimida antes de entrar no site (ver comprimir_se_preciso).
LIMITE_BYTES = 700_000     # 700 KB
LADO_MAIOR_PX = 2000       # lado maior da imagem, em pixels, depois de reduzida
QUALIDADE_JPEG = 82


def titulo_por_defeito(pasta):
    """'festa-do-divino' -> 'Festa Do Divino' (usado se não houver albuns.json)."""
    return pasta.replace("-", " ").replace("_", " ").strip().title()


def legenda(ficheiro, titulo_album, n):
    """Legenda da foto no lightbox.

    Se o ficheiro tiver um nome com sentido ("cerimonia-igreja.jpg"), usa-o.
    Se for um nome cru de exportação ("2026-07-23 at 12.45.29.jpeg", "IMG_4821"),
    usa "<Nome do álbum> 01", que fica muito melhor à vista.
    """
    base = os.path.splitext(ficheiro)[0]
    palavras = base.replace("-", " ").replace("_", " ").split()
    # Fica só com as palavras que são mesmo texto (>=3 letras, não "at"/"img"/"foto")
    uteis = [
        w for w in palavras
        if sum(c.isalpha() for c in w) >= 3
        and w.lower() not in {"img", "image", "foto", "photo", "whatsapp", "screenshot"}
    ]
    if uteis:
        return " ".join(uteis).replace(".", " ").strip().capitalize()
    return "%s %02d" % (titulo_album, n)


def comprimir_se_preciso(caminho_completo):
    """Reduz uma foto grande de câmara para tamanho de web, no próprio ficheiro.

    Corre sozinho sempre que o gerador roda — no computador de quem estiver a
    testar, e no robô do GitHub a cada foto nova. Sem isto, uma pasta de
    fotos de câmara (5-17 MB cada) deixaria o site lentíssimo no celular.

    Fotos já pequenas (<= LIMITE_BYTES) não são tocadas. PNG/GIF/AVIF também
    não — só JPG/WEBP, que são os formatos que as câmaras e celulares usam.
    """
    ext = os.path.splitext(caminho_completo)[1].lower()
    if ext not in EXT_COMPRIMIVEL:
        return False
    try:
        if os.path.getsize(caminho_completo) <= LIMITE_BYTES:
            return False
    except OSError:
        return False

    try:
        from PIL import Image, ImageOps
    except ImportError:
        print("  aviso: Pillow não está instalado — fotos grandes não foram comprimidas "
              "(pip install Pillow --break-system-packages)", file=sys.stderr)
        return False

    try:
        img = Image.open(caminho_completo)
        img = ImageOps.exif_transpose(img)  # respeita a rotação da câmara
        if img.mode != "RGB":
            img = img.convert("RGB")
        largura, altura = img.size
        maior_lado = max(largura, altura)
        if maior_lado > LADO_MAIOR_PX:
            escala = LADO_MAIOR_PX / maior_lado
            img = img.resize(
                (max(1, round(largura * escala)), max(1, round(altura * escala))),
                Image.LANCZOS,
            )
        img.save(caminho_completo, "JPEG", quality=QUALIDADE_JPEG, optimize=True)
        return True
    except Exception as e:
        print("  aviso: não consegui comprimir %s (%s)" % (caminho_completo, e), file=sys.stderr)
        return False


def caminho_web(*partes):
    """Monta o caminho para o HTML, escapando espaços e acentos."""
    return "/".join(quote(p) for p in partes)


def carregar_config():
    if not os.path.isfile(CONFIG):
        return {"ordem": [], "titulos": {}}
    with open(CONFIG, encoding="utf-8") as f:
        cfg = json.load(f)
    cfg.setdefault("ordem", [])
    cfg.setdefault("titulos", {})
    return cfg


def main():
    if not os.path.isdir(PASTA_FOTOS):
        print("ERRO: não existe a pasta fotos/", file=sys.stderr)
        return 1

    cfg = carregar_config()

    pastas = sorted(
        d for d in os.listdir(PASTA_FOTOS)
        if os.path.isdir(os.path.join(PASTA_FOTOS, d))
        and not d.startswith(".")
        and d not in PASTAS_IGNORADAS
    )

    # Álbuns listados em "ordem" vêm primeiro, na ordem indicada.
    # Os restantes vêm a seguir, por ordem alfabética.
    ordenadas = [p for p in cfg["ordem"] if p in pastas]
    ordenadas += [p for p in pastas if p not in ordenadas]

    albuns = []
    proximo_id = 1
    total_fotos = 0

    for pasta in ordenadas:
        caminho = os.path.join(PASTA_FOTOS, pasta)
        ficheiros = sorted(
            f for f in os.listdir(caminho)
            if os.path.isfile(os.path.join(caminho, f))
            and os.path.splitext(f)[1].lower() in (EXT_IMAGEM | EXT_VIDEO)
            and not PADRAO_CAPTURA_ECRA.match(f)
        )
        if not ficheiros:
            print("  (vazio, ignorado): fotos/%s/" % pasta)
            continue

        comprimidas = 0
        for f in ficheiros:
            if comprimir_se_preciso(os.path.join(caminho, f)):
                comprimidas += 1
        if comprimidas:
            print("  %-20s %d foto(s) comprimida(s) para tamanho de web" % (pasta, comprimidas))

        capas = [f for f in ficheiros if os.path.splitext(f)[0].lower() == "capa"]
        capa_ficheiro = capas[0] if capas else ficheiros[0]
        # A capa não se repete dentro do álbum se for um ficheiro "capa.*"
        lista = [f for f in ficheiros if f not in capas]

        titulos = cfg["titulos"].get(pasta)
        if not titulos:
            t = titulo_por_defeito(pasta)
            titulos = {"pt": t, "en": t}

        fotos = []
        for n, f in enumerate(lista, 1):
            ext = os.path.splitext(f)[1].lower()
            item = {
                "id": proximo_id,
                "imagem": caminho_web("fotos", pasta, f),
                "titulo": legenda(f, titulos["pt"], n),
            }
            if ext in EXT_VIDEO:
                item["tipo"] = "video"
                item["video"] = item["imagem"]
            fotos.append(item)
            proximo_id += 1

        albuns.append({
            "key": pasta,
            "titulo": titulos,
            "capa": caminho_web("fotos", pasta, capa_ficheiro),
            "fotos": fotos,
        })
        total_fotos += len(fotos)
        print("  %-20s %2d foto(s)" % (pasta, len(fotos)))

    cabecalho = (
        "// ============================================================\n"
        "// FICHEIRO GERADO AUTOMATICAMENTE — NÃO EDITAR À MÃO.\n"
        "// É reescrito sempre que se acrescentam fotos à pasta fotos/.\n"
        "// Para mudar nomes ou ordem dos álbuns: fotos/albuns.json\n"
        "// ============================================================\n"
        "window.ALBUNS = "
    )
    corpo = json.dumps(albuns, ensure_ascii=False, indent=2)

    with open(SAIDA, "w", encoding="utf-8") as f:
        f.write(cabecalho + corpo + ";\n")

    print("\nfotos.js gerado: %d álbum(ns), %d foto(s)." % (len(albuns), total_fotos))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
