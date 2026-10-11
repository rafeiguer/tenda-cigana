"""Acha e recorta as 36 cartas da imagem "Polaridade das cartas do baralho cigano".

Uso: python ferramentas/recortar_cartas.py pasta_saida
Salva carta-NN.png (tamanho original) e uma folha de conferência.
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image

ORIGEM = Path.home() / "Desktop" / "site thays" / "54e7f8d2cbcba1fd5e716f0db8684622.jpg"
SAIDA = Path(sys.argv[1]); SAIDA.mkdir(parents=True, exist_ok=True)

# Ordem das cartas como aparecem na imagem, linha por linha
LINHAS = [
    [2, 9, 13, 16, 18, 24, 30, 31, 32],
    [6, 7, 8, 10, 11, 14, 21, 23, 36],
    [1, 3, 4, 5, 12, 15, 17, 19, 20],
    [22, 25, 26, 27, 28, 29, 33, 34, 35],
]

im = Image.open(ORIGEM).convert("RGB")
a = np.asarray(im).astype(int)
# fundo creme do pôster; tudo que foge muito dele é carta
fundo = np.array([243, 234, 216])
mascara = np.abs(a - fundo).sum(axis=2) > 70

def faixas(perfil, minimo, menor):
    """Trechos contínuos onde o perfil passa do mínimo, com pelo menos `menor` pixels."""
    res, ini = [], None
    for i, v in enumerate(list(perfil) + [0]):
        if v > minimo and ini is None:
            ini = i
        elif v <= minimo and ini is not None:
            if i - ini >= menor:
                res.append((ini, i))
            ini = None
    return res

# Alturas medidas olhando a imagem ampliada (a faixa creme do nome engana a detecção automática)
linhas_y = [(229, 433), (526, 739), (834, 1016), (1024, 1199)]

caixas = {}
for (y0, y1), numeros in zip(linhas_y, LINHAS):
    cols = faixas(mascara[y0:y1].sum(axis=0), (y1 - y0) * 0.5, 40)
    # cartas encostadas viram uma faixa só: divide pela largura típica
    larg = sorted(x1 - x0 for x0, x1 in cols)[len(cols) // 2]
    separadas = []
    for x0, x1 in cols:
        k = max(1, round((x1 - x0) / larg))
        passo = (x1 - x0) / k
        separadas += [(round(x0 + i * passo), round(x0 + (i + 1) * passo)) for i in range(k)]
    cols = separadas
    print(f"linha {y0}-{y1}: {len(cols)} colunas", cols)
    assert len(cols) == 9, "esperava 9 cartas na linha"
    for (x0, x1), n in zip(cols, numeros):
        caixas[n] = (x0, y0, x1, y1)

for n, cx in sorted(caixas.items()):
    im.crop(cx).save(SAIDA / f"carta-{n:02d}.png")

# folha de conferência
w = max(c[2] - c[0] for c in caixas.values()); h = max(c[3] - c[1] for c in caixas.values())
folha = Image.new("RGB", (w * 9, h * 4), "white")
for i, n in enumerate(range(1, 37)):
    folha.paste(Image.open(SAIDA / f"carta-{n:02d}.png"), ((i % 9) * w, (i // 9) * h))
folha.save(SAIDA / "_folha.png")
print("ok", len(caixas), "cartas")
