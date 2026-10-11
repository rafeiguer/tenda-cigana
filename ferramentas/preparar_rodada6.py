"""Rodada 6: cortinas presas nas bordas do herói e carroça puxada por cavalos que passeia.

Uso: python preparar_rodada6.py pasta_com_as_geradas
Entradas (de gerador/montar_rodada6.py): presa-vermelha-102.png e vardo-cavalos-112.png.
Saídas em assets/:
- cortina-presa-esq.webp / cortina-presa-dir.webp: cada metade do par de cortinas, sem o fundo preto e sem a
  cortina de trás (a do meio); a franja dourada da borda de dentro marca até onde vai cada lado.
- cavalos-corpo.webp: carroça e cavalos sem fundo, com o miolo da roda de trás vazado.
- cavalos-roda.webp: o miolo da roda de trás (raios e cubo), desentortado para círculo, para girar no CSS.
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ORIGEM = Path(sys.argv[1])
ASSETS = Path(__file__).resolve().parent.parent / "assets"

# ---------- cortinas ----------
c = np.asarray(Image.open(ORIGEM / "presa-vermelha-102.png").convert("RGB")).astype(np.int16)
H, W, _ = c.shape
r, g, b = c[..., 0], c[..., 1], c[..., 2]
ouro = (g > 95) & (r > g) & (r - b > 40) & (g - b > 25)  # o cordão dourado da borda de dentro
# fundo preto some aos poucos (sem serrilhado); o tecido escuro ainda tem vermelho suficiente
brilho = c.max(axis=2)
# só o preto do fundo some; as dobras escuras do veludo ainda têm um pouco de vermelho e ficam
alfa_luz = np.clip((brilho - 5) / 9, 0, 1)
PRESILHA = 790  # abaixo da presilha só sobra a parte que cai junto da borda da tela

def lado(esq):
    m = np.zeros((H, W), np.float32)
    # a borda de dentro (cordão dourado) desce em curva suave: mede linha a linha e ajusta um polinômio,
    # assim fios soltos e o cordão da presilha não fazem degraus no recorte
    ys, xs = [], []
    for y in range(40, PRESILHA):
        linha = ouro[y, :W // 2 + 15] if esq else ouro[y, W // 2 - 15:]
        p = np.nonzero(linha)[0]
        if len(p):
            ys.append(y); xs.append(p.max() + 5 if esq else W // 2 - 15 + p.min() - 5)
    ys, xs = np.array(ys), np.array(xs, float)
    for _ in range(3):  # descarta os pontos que fogem da curva e ajusta de novo
        coef = np.polyfit(ys, xs, 3)
        ok = np.abs(np.polyval(coef, ys) - xs) < 18
        ys, xs = ys[ok], xs[ok]
    for y in range(H):
        if y < PRESILHA:
            borda = int(round(np.polyval(coef, max(y, 40))))
        else:
            # abaixo da presilha: borlas e a sobra da cortina, sem pegar a barra da cortina de trás
            d = 105 if y > 985 else min(175, int(230 - (y - 600) * .172) - 8)
            borda = d if esq else W - d
        if esq:
            m[y, :max(0, borda)] = 1
        else:
            m[y, min(W, borda):] = 1
    m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))) / 255
    a = (m * alfa_luz * 255).astype(np.uint8)
    img = Image.fromarray(c.astype(np.uint8)).convert("RGBA")
    img.putalpha(Image.fromarray(a))
    img = img.crop(img.getbbox())
    return img

for nome, esq in (("cortina-presa-esq", True), ("cortina-presa-dir", False)):
    im = lado(esq)
    im.save(ASSETS / f"{nome}.webp", "WEBP", quality=88, method=6)
    print(nome, im.size)

# ---------- carroça com cavalos ----------
from rembg import remove, new_session
v = Image.open(ORIGEM / "vardo-cavalos-112.png").convert("RGB")
corpo = remove(v, session=new_session("isnet-general-use"), alpha_matting=True, alpha_matting_foreground_threshold=240,
               alpha_matting_background_threshold=15, alpha_matting_erode_size=8)
# roda de trás (de quem olha): elipse de semieixos 109,5 x 126 em volta de (279,5; 468); os raios
# se encontram no cubo, em (272; 470). O miolo é desentortado para círculo (fator K) e gira em volta do cubo.
CX, CY, K, R = 272, 470, 109.5 / 126, 100
larg = int(round(2 * R * K))
miolo = corpo.crop((CX - larg // 2, CY - R, CX - larg // 2 + larg, CY + R)).resize((2 * R, 2 * R), Image.LANCZOS)
mascara = Image.new("L", (2 * R, 2 * R), 0)
ImageDraw.Draw(mascara).ellipse((0, 0, 2 * R - 1, 2 * R - 1), fill=255)
miolo.putalpha(Image.fromarray(np.minimum(np.asarray(miolo.getchannel("A")), np.asarray(mascara))))
miolo = miolo.resize((240, 240), Image.LANCZOS)
miolo.save(ASSETS / "cavalos-roda.webp", "WEBP", quality=88, method=6)
# vaza o miolo no corpo (senão os raios parados aparecem entre os que giram)
a = corpo.getchannel("A")
ImageDraw.Draw(a).ellipse((CX - larg / 2, CY - R, CX + larg / 2, CY + R), fill=0)
corpo.putalpha(a)
caixa = corpo.getbbox()
corpo = corpo.crop(caixa)
corpo.save(ASSETS / "cavalos-corpo.webp", "WEBP", quality=86, method=6)
cw, ch = corpo.size
print("cavalos-corpo", corpo.size, "caixa", caixa)
print(f"roda: --x:{(CX - caixa[0]) / cw * 100:.2f}% --y:{(CY - caixa[1]) / ch * 100:.2f}% --h:{2 * R / ch * 100:.2f}% --k:{K:.3f}")
