# Portfólio de Fotografia — Pedro [SOBRENOME]

Site de portfólio (uma página, sem back-end). Tudo vive no ficheiro **`index.html`**.

## Publicar / atualizar

O site é servido pelo **GitHub Pages** a partir do `index.html` na raiz.
Para atualizar: edite o ficheiro, faça *commit* e *push* pelo GitHub Desktop.
As alterações aparecem online em 1–2 minutos.

Endereço do site (depois de ativar o Pages em *Settings → Pages*):
`https://arthur-mahalaeth.github.io/Catalogue-Photo-Pedro/`

## Público ou privado?

- **Só para ver no seu PC:** basta abrir o `index.html` com duplo-clique. Não precisa do GitHub.
- **Online e grátis (GitHub Pages):** o repositório precisa de ser **público**. Isso significa apenas que qualquer pessoa pode *ver* o código — **ninguém pode editar nada além de você**. As fotos de qualquer site são sempre visíveis, então isto não expõe nada de sensível.
- **Site online com código privado:** possível com serviços como Netlify ou Vercel (aceitam repositório privado no plano grátis).

## Antes de ir para o ar (preencher)

No `index.html`, procure (Ctrl+F) e substitua:

| Procurar por        | O quê                                   | Onde está |
|---------------------|-----------------------------------------|-----------|
| `[SOBRENOME]`       | Sobrenome do fotógrafo                  | constante `NOME_SOBRENOME` |
| `[SEU EMAIL]`       | Email de contacto                       | constante `EMAIL_CONTATO` + bloco de contacto |
| `[SEU INSTAGRAM]`   | Utilizador do Instagram                 | bloco de contacto |
| `556293793792`      | Número de WhatsApp (⚠️ confirmar dígitos)| constante `WHATSAPP_NUMERO` |

> ⚠️ O número atual tem 8 dígitos após o DDD; celulares no Brasil têm 9. Confirmar antes de publicar.

## Como funciona a navegação

O site mostra primeiro as **capas dos álbuns** (Retratos, Casamentos, Paisagens).
Ao clicar numa capa, só aparecem as fotos daquele álbum — nunca tudo junto.
Cada álbum tem o seu próprio link (ex.: `.../#album-casamentos`), que pode ser
partilhado diretamente, e o botão "voltar" do navegador funciona normalmente.

## Como editar o conteúdo

Tudo se edita nas primeiras secções do `<script>` dentro do `index.html`:

- **Nome:** constantes `NOME_PRIMEIRO` e `NOME_SOBRENOME` — muda em todo o site (título, cabeçalho, rodapé, meta tags e políticas) a partir deste único sítio.
- **Álbuns e fotos:** array `ALBUNS`. Cada álbum tem `key`, `titulo` (PT/EN), `capa` e a sua própria lista `fotos`. Para adicionar uma foto, copie um bloco `{ ... }` dentro do álbum certo e dê um `id` **único em todo o site** (nunca repita, mesmo entre álbuns diferentes):
  ```js
  { id: 13, imagem: 'fotos/casamentos/01.jpg', titulo: 'Cerimónia', ano: 2026 }
  ```
- **Novo álbum:** copie um bloco `{ key, titulo, capa, fotos: [...] }` inteiro dentro de `ALBUNS`.
- **Formato de uma foto** (opcional): `formato: '4 / 5'` (ou `'1 / 1'`, `'16 / 9'`...) — só essa foto muda de proporção.
- **Vídeo** (opcional): `tipo: 'video', video: 'videos/x.mp4', imagem: 'capa.jpg'`.
- **Cor principal:** variável CSS `--primary` (azul marinho `#1A2F5C`).
- **Textos PT/EN:** objeto `STRINGS`.

## Fotos

⚠️ **As fotos atuais são só de amostra** — vêm de um banco de imagens gratuito
(loremflickr.com), usadas apenas para pré-visualizar o layout dos álbuns.
**Não são fotos do Pedro.** Substitua todas antes de publicar.

A pasta **`fotos/`** já existe — coloque lá as fotos reais (sugestão: uma subpasta
por álbum, ex. `fotos/casamentos/`) e aponte o campo `imagem` de cada item do
array `ALBUNS` para o caminho correspondente. Veja o guia em `fotos/README.md`.

## Página 404

O `404.html` aparece quando alguém acede a um endereço que não existe no site
— por exemplo um link antigo, um erro de digitação no URL, ou uma página
apagada. **Não tem relação com os álbuns**: navegar entre álbuns usa apenas a
parte `#...` do endereço, que nunca chega a ser pedida ao servidor, por isso o
404 nunca aparece ao trocar de álbum. O GitHub Pages mostra-o automaticamente
por já se chamar `404.html` na raiz — não precisa de configuração extra.

## Licença e proteção

- **`LICENSE`** — todo o conteúdo é *© Todos os direitos reservados*. As fotos, vídeos e textos **não** podem ser reutilizados sem autorização (Lei 9.610/98). O código está lá apenas para o site funcionar.
- **Proteção das imagens:** o site bloqueia clique-direito e arrastar, mas isso é só um travão leve. Proteção real = marca d'água + publicar em resolução de web + o aviso legal do `LICENSE`. Detalhes em `fotos/README.md`.
- **Dados (LGPD):** o site não usa cookies nem *analytics*; o formulário envia direto para o WhatsApp e não guarda nada. As políticas (Privacidade / Termos / LGPD) estão no rodapé do site. A única ligação externa é o Google Fonts (carrega a fonte e regista o IP do visitante) — já divulgado na política; se quiser privacidade máxima, dá para trocar por fontes do sistema.

## Estrutura do projeto

```
index.html          O site (página única)
404.html            Página de erro personalizada
LICENSE             Direitos autorais (todos os direitos reservados)
README.md           Este guia
fotos/              Imagens e vídeos do portfólio (+ guia próprio)
```

---
© 2026 Pedro [SOBRENOME]. Todos os direitos reservados.
