# -*- coding: utf-8 -*-
"""
Gera os arquivos de assets/img a partir das aquarelas originais e do monograma.

Por que existe: as imagens do site precisam ser ARQUIVOS de verdade, otimizados,
com WebP e fallback JPEG. Nada de base64 embutido no HTML e nada de arquivo
truncado -- foi exatamente isso que quebrou o hero na primeira versao.

Uso:
    python scripts/gerar-imagens.py [pasta-com-os-originais]

A pasta padrao e o diretorio pai do repositorio (Desktop/casamento), onde moram
as aquarelas, o manual de identidade e os monogramas.
"""

import os
import sys

from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTE = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(RAIZ, ".."))
DESTINO = os.path.join(RAIZ, "assets", "img")

AQUARELAS = os.path.join(FONTE, "Aquarelas", "Aquarela paleta (atual)")

# As escolhas de cada arte, e o porque de cada uma.
VARANDA_CORCOVADO = os.path.join(AQUARELAS, "ChatGPT Image 18 de jun. de 2026, 20_41_18 - Copia.png")  # hero: a varanda do casarao com o Corcovado ao fundo
CASAL_MANSAO = os.path.join(AQUARELAS, "ChatGPT Image 18 de ago. de 2026, 12_57_29.png")   # compartilhamento: o casal, o casarao e o Cristo
VISTA_RIO = os.path.join(AQUARELAS, "ChatGPT Image 18 de ago. de 2026, 12_24_25.png")      # local: o Pao de Acucar visto do mirante
CASAL_VARANDA = os.path.join(AQUARELAS, "ChatGPT Image 18 de jun. de 2026, 20_33_40.png")  # faixa: o casal na varanda
MONOGRAMA = os.path.join(FONTE, "monograma ANAe.png")  # o unico dos tres com canal alfa de verdade

ALGODAO = (249, 248, 245)


def abrir(caminho):
    if not os.path.exists(caminho):
        raise SystemExit("Arquivo de origem nao encontrado: %s" % caminho)
    return Image.open(caminho)


def salvar_par(im, nome, largura, qualidade=82):
    """Grava o par WebP + JPEG do mesmo recorte, na mesma largura."""
    im = im.convert("RGB")
    if im.width != largura:
        altura = round(im.height * largura / im.width)
        im = im.resize((largura, altura), Image.LANCZOS)
    jpg = os.path.join(DESTINO, nome + ".jpg")
    webp = os.path.join(DESTINO, nome + ".webp")
    im.save(jpg, "JPEG", quality=qualidade, optimize=True, progressive=True)
    im.save(webp, "WEBP", quality=qualidade, method=6)
    print("%-22s %sx%s  jpg %6.0f kB  webp %6.0f kB"
          % (nome, im.width, im.height,
             os.path.getsize(jpg) / 1024, os.path.getsize(webp) / 1024))
    return im


def recortar_proporcao(im, proporcao, ancora=0.5):
    """Corta a imagem na proporcao pedida, ancorando verticalmente em `ancora`."""
    alvo = im.width / proporcao
    if alvo <= im.height:
        topo = round((im.height - alvo) * ancora)
        return im.crop((0, topo, im.width, topo + round(alvo)))
    alvo = im.height * proporcao
    esq = round((im.width - alvo) * 0.5)
    return im.crop((esq, 0, esq + round(alvo), im.height))


def main():
    os.makedirs(DESTINO, exist_ok=True)

    # 1. Hero -- a arte nasce em 1.29:1, entao o recorte 3:2 tira altura: um
    #    pouco de ceu em cima, um pouco de gramado embaixo.
    hero = recortar_proporcao(abrir(VARANDA_CORCOVADO), 3 / 2, ancora=0.5)
    salvar_par(hero, "hero-varanda", 1800, qualidade=84)

    # 1b. Hero em retrato -- no celular o corte 3:2 ampliaria um pedaco liso da
    #     parede e a aquarela viraria um degrade. Este recorte vertical mantem o
    #     Cristo e um pedaco da casa dentro da tela ao mesmo tempo.
    #
    #     A ancora nao e o centro do que aparece no celular. A tela do celular e
    #     mais estreita que 3:4, entao o `object-fit: cover` ainda come as
    #     laterais deste recorte, e sobra so o miolo. Por isso 0.46 foi medido
    #     na tela, e nao na arte: nela o Cristo cai a um quinto da borda
    #     esquerda e a casa entra pela direita com telhado, parede e um arco.
    #     Mexer aqui pede outra rodada de conferencia no navegador.
    retrato = abrir(VARANDA_CORCOVADO).convert("RGB")
    alvo_l = round(retrato.height * 3 / 4)
    esq = min(max(round(retrato.width * 0.46 - alvo_l / 2), 0), retrato.width - alvo_l)
    retrato = retrato.crop((esq, 0, esq + alvo_l, retrato.height))
    salvar_par(retrato, "hero-varanda-retrato", 900, qualidade=84)

    # 2. Local -- a vista do Rio, no lugar do line art que vinha quebrado.
    salvar_par(abrir(VISTA_RIO), "local-rio", 1400)

    # 3. Faixa entre a historia e o local.
    faixa = recortar_proporcao(abrir(CASAL_VARANDA), 3 / 1, ancora=0.42)
    salvar_par(faixa, "faixa-varanda", 1800)

    # 4. Compartilhamento -- 1200x630 e o formato que WhatsApp e redes esperam.
    #    Aqui fica o casal: a previa de link e o unico lugar onde a arte aparece
    #    sozinha, sem texto por cima, e o casal e o que convida a abrir.
    og = recortar_proporcao(abrir(CASAL_MANSAO), 1200 / 630, ancora=0.16)
    salvar_par(og, "og-cover", 1200, qualidade=86)

    # 5. Monograma -- recortado no proprio traco e reduzido. O alfa e preservado
    #    porque o hero pinta ele de branco por filtro CSS.
    mono = abrir(MONOGRAMA).convert("RGBA")
    caixa = mono.getchannel("A").getbbox()
    mono = mono.crop(caixa)
    largura = 600
    mono = mono.resize((largura, round(mono.height * largura / mono.width)), Image.LANCZOS)
    saida = os.path.join(DESTINO, "monograma-transparente.png")
    mono.save(saida, "PNG", optimize=True)
    print("%-22s %sx%s  png %6.0f kB"
          % ("monograma", mono.width, mono.height, os.path.getsize(saida) / 1024))

    # 6. Favicon -- o traco fica ilegivel pequeno demais sem respiro, entao vai
    #    sobre algodao com margem, e nao transparente.
    for lado, nome in ((32, "favicon-32.png"), (180, "apple-touch-icon.png")):
        respiro = round(lado * 0.14)
        util = lado - respiro * 2
        marca = mono.copy()
        marca.thumbnail((util, util), Image.LANCZOS)
        icone = Image.new("RGBA", (lado, lado), ALGODAO + (255,))
        icone.paste(marca, ((lado - marca.width) // 2, (lado - marca.height) // 2), marca)
        icone.save(os.path.join(DESTINO, nome), "PNG", optimize=True)
        print("%-22s %sx%s" % (nome.replace(".png", ""), lado, lado))


if __name__ == "__main__":
    main()
