"""Rodada 7: carroça com os cavalos à frente dos varais, pernas que andam e roda que gira.

Uso: python preparar_rodada7.py pasta_r6 carroca_sem_cavalos.png
- pasta_r6: onde está a vardo-cavalos-112.png (gerador/montar_rodada6.py)
- carroca_sem_cavalos.png: a mesma imagem com a frente da carroça repintada sem os cavalos (gerador/separar_cavalos.py)
Saídas em assets/: cavalos-corpo.webp (carroça + varal + corpos dos cavalos), cavalos-perna-1..4.webp (faixas das
pernas, que balançam no CSS em volta do quadril/ombro) e cavalos-roda.webp (miolo da roda de trás, para girar).
Imprime as posições em % para colar no index.html.
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from rembg import remove, new_session

sys.path.insert(0, str(Path(__file__).resolve().parent / "gerador"))
from cavalos_contorno import CAVALOS, PERNAS, CORTE_PERNAS

R6, SEM = Path(sys.argv[1]), Path(sys.argv[2])
ASSETS = Path(__file__).resolve().parent.parent / "assets"
sessao = new_session("isnet-general-use")
recorta = lambda im: remove(im, session=sessao, alpha_matting=True, alpha_matting_foreground_threshold=240,
                            alpha_matting_background_threshold=15, alpha_matting_erode_size=8)

original = Image.open(R6 / "vardo-cavalos-112.png").convert("RGB")
W, H = original.size

# ---------- cavalos: recorte do fundo + contorno ----------
cav = recorta(original)
m = Image.new("L", (W, H), 0)
ImageDraw.Draw(m).polygon(CAVALOS, fill=255)
m = m.filter(ImageFilter.GaussianBlur(1.2))
cav.putalpha(Image.fromarray(np.minimum(np.asarray(cav.getchannel("A")), np.asarray(m))))

# ---------- carroça repintada, sem os cavalos ----------
car = recorta(Image.open(SEM).convert("RGB"))
FRENTE = 1402  # a repintura pôs uma plataforma com buquê de rosas na frente; nada passa daqui
a = np.asarray(car.getchannel("A")).copy()
a[:, FRENTE:] = 0
car.putalpha(Image.fromarray(a))

# ---------- rodas: o miolo (raios e cubo) de cada uma é desentortado para círculo e gira no CSS ----------
# de trás: elipse 109,5 x 126, cubo em (272;470); da frente (repintada): elipse 114,5 x 119, cubo em (959;482)
RODAS = [("cavalos-roda", 272, 470, 109.5 / 126, 100, 126), ("cavalos-roda2", 959, 482, 114.5 / 119, 96, 119)]
for nome, CX, CY, K, R, _ in RODAS:
    larg = int(round(2 * R * K))
    miolo = car.crop((CX - larg // 2, CY - R, CX - larg // 2 + larg, CY + R)).resize((2 * R, 2 * R), Image.LANCZOS)
    masc = Image.new("L", (2 * R, 2 * R), 0)
    ImageDraw.Draw(masc).ellipse((0, 0, 2 * R - 1, 2 * R - 1), fill=255)
    miolo.putalpha(Image.fromarray(np.minimum(np.asarray(miolo.getchannel("A")), np.asarray(masc))))
    miolo.resize((240, 240), Image.LANCZOS).save(ASSETS / f"{nome}.webp", "WEBP", quality=88, method=6)
    a = car.getchannel("A")
    ImageDraw.Draw(a).ellipse((CX - larg / 2, CY - R, CX + larg / 2, CY + R), fill=0)
    car.putalpha(a)

# ---------- montagem: cavalos à frente, entre os varais ----------
DX = 695                       # a garupa (x 684) fica logo depois do buquê da frente da carroça
LARG = 1414 + DX + 6
tela = Image.new("RGBA", (LARG, H), (0, 0, 0, 0))
tela.alpha_composite(car)
# varal: o cavalo de perto já traz o varal dourado de (675;392) até a coalheira; prolonga ele para trás até a carroça
INCL = (392 - 330) / (940 - 675)
x_ini, x_fim = 1290, 700 + DX   # sai de baixo da plataforma da frente
y = lambda x: 392 + INCL * (675 + DX - x)
cor = original.getpixel((760, 372))
d = ImageDraw.Draw(tela)
d.line([(x_ini, y(x_ini) + 1), (x_fim, y(x_fim) + 1)], fill=(60, 34, 12, 255), width=11)     # sombra/borda
d.line([(x_ini, y(x_ini)), (x_fim, y(x_fim))], fill=cor + (255,), width=8)
d.line([(x_ini, y(x_ini) - 2), (x_fim, y(x_fim) - 2)], fill=(255, 236, 170, 200), width=2)  # brilho de metal
d.ellipse((x_ini - 7, y(x_ini) - 7, x_ini + 7, y(x_ini) + 7), fill=(70, 44, 16, 255))       # ferragem na carroça

# corpo dos cavalos (com o topo das pernas, que fica por cima das peças que balançam)
ca = np.asarray(cav).copy()
corpo = ca.copy()
corpo[CORTE_PERNAS + 30:, :, 3] = 0
camada = Image.new("RGBA", (LARG, H), (0, 0, 0, 0))
camada.alpha_composite(Image.fromarray(corpo), (DX, 0))

# pernas: uma faixa por par de pernas, de CORTE_PERNAS até o chão
pernas = []
for i, p in enumerate(PERNAS, 1):
    pe = ca.copy()
    pe[:CORTE_PERNAS] = 0
    pe[:, :p["x0"], 3] = 0
    pe[:, p["x1"]:, 3] = 0
    im = Image.fromarray(pe)
    cx = im.getbbox()
    peca = im.crop(cx)
    peca.save(ASSETS / f"cavalos-perna-{i}.webp", "WEBP", quality=88, method=6)
    pernas.append((cx, p))

# tudo junto, corta a sobra e salva
tela.alpha_composite(camada)
caixa = tela.getbbox()
# a caixa precisa incluir as pernas também
for cx, _ in pernas:
    caixa = (min(caixa[0], cx[0] + DX), min(caixa[1], cx[1]), max(caixa[2], cx[2] + DX), max(caixa[3], cx[3]))
tela = tela.crop(caixa)
tela.save(ASSETS / "cavalos-corpo.webp", "WEBP", quality=86, method=6)
TW, TH = tela.size
pc = lambda v, t: f"{v / t * 100:.2f}%"
print("cavalos-corpo", tela.size)
for nome, CX, CY, K, R, aro in RODAS:
    print(f'{nome}: --x:{pc(CX - caixa[0], TW)};--y:{pc(CY - caixa[1], TH)};--h:{pc(2 * R, TH)};--k:{K:.3f}  raio/largura={aro / TW:.4f}')
for i, (cx, p) in enumerate(pernas, 1):
    x0, y0 = cx[0] + DX - caixa[0], cx[1] - caixa[1]
    w, h = cx[2] - cx[0], cx[3] - cx[1]
    ox, oy = p["pivo"][0] + DX - caixa[0] - x0, p["pivo"][1] - caixa[1] - y0
    print(f'perna {i}: left:{pc(x0, TW)};top:{pc(y0, TH)};width:{pc(w, TW)};--ox:{pc(ox, w)};--oy:{pc(oy, h)};--f:{p["fase"]}')
