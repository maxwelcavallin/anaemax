# anaemax

Site do casamento de Ana Flávia & Maxwel — 22 de agosto de 2027, Rio de Janeiro.

HTML, CSS e um arquivo de JavaScript. Sem build, sem dependência: abrir o
`index.html` já mostra o site inteiro.

```
index.html
assets/css/style.css
assets/js/main.js
assets/img/            gerado por scripts/gerar-imagens.py
scripts/gerar-imagens.py
```

## As imagens

**Elas são arquivos. Nunca base64 dentro do HTML.** A primeira versão publicada
tinha as três imagens gravadas a partir de strings base64 que chegaram cortadas:
o arquivo existia, o servidor devolvia 200, e o navegador não decodificava nada
— o hero aparecia como texto alternativo no canto da tela.

O que está no `assets/img/` sai de `scripts/gerar-imagens.py`, que lê as
aquarelas e o monograma originais e grava cada peça em WebP e JPEG:

```
python scripts/gerar-imagens.py [pasta-com-os-originais]
```

A pasta padrão é o diretório pai deste repositório (`Desktop/casamento`), onde
moram as aquarelas, o manual de identidade e os três monogramas. Os originais
não entram no repositório: são cerca de 3 MB cada e não mudam.

| arquivo | de onde vem | onde aparece |
| --- | --- | --- |
| `hero-casal` | aquarela do casal com o casarão e o Cristo | fundo do topo, em telas largas |
| `hero-casal-retrato` | mesma aquarela, recorte 3:4 | fundo do topo, no celular |
| `local-rio` | aquarela do Pão de Açúcar visto do mirante | seção "Uma cidade maravilhosa" |
| `faixa-varanda` | aquarela do casal na varanda | faixa entre a história e o local |
| `og-cover` | recorte 1200×630 da aquarela do casal | prévia no WhatsApp e nas redes |
| `monograma-transparente.png` | `monograma ANAe.png` | topo e rodapé |
| `favicon-32.png`, `apple-touch-icon.png` | monograma sobre algodão | aba do navegador e tela inicial |

Dos três monogramas entregues, só o `monograma ANAe.png` tem canal alfa de
verdade — os outros dois vêm com fundo chapado. O site pinta o traço de branco
por filtro CSS, então a transparência não é detalhe, é requisito.

Cada imagem entra num `<picture>` com WebP primeiro e JPEG como reserva, com
`width` e `height` declarados para a página não pular enquanto carrega.

## Identidade

Do manual `ID_VISUAL ANA E MAX_OP2.pdf`:

- **Cores** — marinho `#0b3d5e`, oliva `#5e7d61`, areia `#e2ddcf`, algodão `#f9f8f5`
- **Tipografia** — Cormorant Garamond nos títulos, Montserrat no texto

## Publicação

Site estático: qualquer host serve a pasta como está. Hoje ele responde em
`ana-e-maxwel.vercel.app`; o domínio `anaemax.com.br` ainda não aponta para cá.
Quando apontar, trocar as URLs absolutas de `og:url` e `og:image` no
`index.html` — prévia de link não aceita caminho relativo.
