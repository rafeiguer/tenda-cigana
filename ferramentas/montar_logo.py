"""Monta o centro da logo: 5 cartas do baralho em leque, deitadas em perspectiva, atrás da rosa.

Uso: python ferramentas/montar_logo.py rosa-recorte.png
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter

ASSETS = Path(__file__).resolve().parent.parent / "assets"

def coeficientes(origem, destino):
    """Coeficientes da transformação de perspectiva do PIL (destino -> origem)."""
    m = []
    for (x, y), (u, v) in zip(destino, origem):
        m.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); m.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    return np.linalg.solve(np.array(m, float), np.array(origem, float).reshape(8)).tolist()

TAM = 1000
CARTAS = [9, 32, 24, 31, 33]      # ramalhete, lua, coração (no meio), sol, chave
ANGULOS = [-30, -15, 0, 15, 30]
ch = 600; cw = round(ch * 360 / 840)
piv = (TAM // 2, 940)

leque = Image.new("RGBA", (TAM, TAM), (0, 0, 0, 0))
for ang, n in zip(ANGULOS, CARTAS):
    carta = Image.open(ASSETS / "cartas" / f"carta-{n:02d}.webp").convert("RGBA").resize((cw, ch), Image.LANCZOS)
    sombra = Image.new("RGBA", (cw + 40, ch + 40), (0, 0, 0, 0))
    sombra.paste((0, 0, 0, 160), (20, 20, cw + 20, ch + 20)); sombra = sombra.filter(ImageFilter.GaussianBlur(9))
    camada = Image.new("RGBA", (TAM, TAM), (0, 0, 0, 0))
    x, y = piv[0] - cw // 2, piv[1] - ch
    camada.alpha_composite(sombra, (x - 14, y - 12)); camada.alpha_composite(carta, (x, y))
    leque.alpha_composite(camada.rotate(-ang, center=piv, resample=Image.BICUBIC))

# perspectiva leve: o leque inclina para trás (topo um pouco mais estreito)
orig = [(0, 0), (TAM, 0), (TAM, TAM), (0, TAM)]
dest = [(90, 70), (910, 70), (TAM, TAM), (0, TAM)]
leque = leque.transform((TAM, TAM), Image.PERSPECTIVE, coeficientes(orig, dest), Image.BICUBIC)

rosa = Image.open(sys.argv[1]).convert("RGBA")
rh = 470; rosa = rosa.resize((round(rosa.width * rh / rosa.height), rh), Image.LANCZOS)
logo = leque.copy()
logo.alpha_composite(rosa, (TAM // 2 - rosa.width // 2, TAM - rh - 10))
logo = logo.crop(logo.getbbox())
logo.thumbnail((640, 640), Image.LANCZOS)
logo.save(ASSETS / "logo-centro.webp", "WEBP", quality=90, method=6)
print("logo ok", logo.size)
