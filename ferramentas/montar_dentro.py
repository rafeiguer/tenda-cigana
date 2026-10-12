"""Rodada 9: monta a cena de dentro da tenda com os objetos que levam às páginas.

Base: dentro-objetos-191.png (o interior 162 repintado: xícaras de porcelana numa bandeja dourada e um pedestal
dourado vazio no meio da mesa). Põe a bola de cristal (assets/bola.webp recortada) sobre o pedestal, com brilho,
e deita três cartas do baralho na frente da bandeja, em perspectiva (como em montar_mesa.py).

Uso: python ferramentas/montar_dentro.py dentro-objetos-191.png saida.png
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ASSETS = Path(__file__).resolve().parent.parent / "assets"
cena = Image.open(sys.argv[1]).convert("RGBA")

# ---------- bola de cristal: o globo da foto da bola, recortado em círculo, sobre o pedestal ----------
BOLA_FOTO = (507, 250, 230)       # centro e raio do globo em assets/bola.webp (1024x1024)
BOLA_CENA = (645, 356, 29)        # onde ele pousa na cena (o pedestal dourado fica em x 645, topo em y ~382)
foto = Image.open(ASSETS / "bola.webp").convert("RGBA")
cx, cy, r = BOLA_FOTO
globo = foto.crop((cx - r, cy - r, cx + r, cy + r))
m = Image.new("L", globo.size, 0); ImageDraw.Draw(m).ellipse((2, 2, 2 * r - 3, 2 * r - 3), fill=255)
globo.putalpha(m.filter(ImageFilter.GaussianBlur(2)))
d = 2 * BOLA_CENA[2]
globo = globo.resize((d, d), Image.LANCZOS)
# um pouco mais clara: ela é a luz da mesa
globo = Image.merge("RGBA", (*ImageEnhance.Brightness(globo.convert("RGB")).enhance(1.12).split(), globo.getchannel("A")))
# brilho rosado em volta, que ilumina a tapeçaria atrás
halo = Image.new("RGBA", cena.size, (0, 0, 0, 0))
hx, hy, hr = BOLA_CENA
ImageDraw.Draw(halo).ellipse((hx - hr * 2.6, hy - hr * 2.6, hx + hr * 2.6, hy + hr * 2.6), fill=(255, 170, 210, 70))
halo = halo.filter(ImageFilter.GaussianBlur(26))
cena.alpha_composite(halo)
cena.alpha_composite(globo, (hx - hr, hy - hr))

# ---------- cartas deitadas na frente da bandeja ----------
CW, CH, ACHATA = 22, 52, .4

def _coef(origem, destino):
    m = []
    for (x, y), (u, v) in zip(destino, origem):
        m.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); m.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    return np.linalg.solve(np.array(m, float), np.array(origem, float).reshape(8)).tolist()

def deitada(img, ang):
    c = img.convert("RGBA").resize((CW * 3, CH * 3), Image.LANCZOS)
    rgb = ImageEnhance.Brightness(c.convert("RGB")).enhance(.66)
    rgb = Image.blend(rgb, Image.new("RGB", rgb.size, (255, 150, 70)), .14)
    c = Image.merge("RGBA", (*rgb.split(), c.getchannel("A")))
    borda = Image.new("RGBA", (c.width + 6, c.height + 6), (190, 150, 80, 255)); borda.alpha_composite(c, (3, 3)); c = borda
    c = c.rotate(-ang, expand=True, resample=Image.BICUBIC)
    w, h = c.size; nh = round(h * ACHATA)
    c = c.resize((w, nh), Image.LANCZOS)
    k = .08 * w
    c = c.transform((w, nh), Image.PERSPECTIVE, _coef([(0, 0), (w, 0), (w, nh), (0, nh)], [(k, 0), (w - k, 0), (w, nh), (0, nh)]), Image.BICUBIC)
    return c.resize((w // 3, nh // 3), Image.LANCZOS)

def pousa(img, x, y):
    sombra = Image.new("RGBA", img.size, (0, 0, 0, 0)); sombra.putalpha(img.getchannel("A").point(lambda a: int(a * .5)))
    cena.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(3)), (int(x - img.width / 2 + 2), int(y - img.height / 2 + 3)))
    cena.alpha_composite(img, (int(x - img.width / 2), int(y - img.height / 2)))

# a tiragem: a Chave, o Coração e o Buquê, na frente da bandeja, postas à mão
for n, x, y, ang in [(33, 606, 487, -12), (24, 645, 491, -1), (9, 684, 487, 11)]:
    pousa(deitada(Image.open(ASSETS / "cartas" / f"carta-{n:02d}.webp"), ang), x, y)

cena.convert("RGB").save(sys.argv[2])
print("ok", sys.argv[2])
