# Portfolio de Fotografia - Pedro Angelo

Site de portfolio (uma pagina, sem back-end). Tudo vive no ficheiro `index.html`, mais o `fotos.js` que e gerado automaticamente a partir da pasta `fotos/`.

Site no ar: https://pedroangelofotografo.github.io/

## Como adicionar fotos

Basta arrastar as fotos para a pasta do album certo, dentro de `fotos/`, pelo proprio site do GitHub (Add file -> Upload files). Um robo (GitHub Action) regenera a lista sozinho e comprime fotos grandes automaticamente. Nao precisa editar nenhum codigo.

Guia completo com passo a passo: ver o link fixado na conversa com o Claude, ou pedir uma copia nova.

## Estrutura

- `index.html` - a pagina inteira (HTML/CSS/JS), sem dependencias externas
- `fotos/` - uma pasta por album; o nome da pasta vira o album
- `fotos/albuns.json` - nomes bonitos e ordem dos albuns
- `fotos.js` - gerado automaticamente, nao editar a mao
- `scripts/gerar-galeria.py` - o gerador (tambem comprime fotos grandes)
- `.github/workflows/atualizar-galeria.yml` - roda o gerador a cada push

## Publicado com GitHub Pages

O site e servido direto da branch `main`, pasta raiz. Qualquer commit em `main` atualiza o site em 1-2 minutos.
