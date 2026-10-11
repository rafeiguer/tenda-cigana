"""Prepara as imagens da segunda rodada (geradas na RX 7900 XTX) para o site.

Uso (com o Python que tem rembg): python ferramentas/preparar_rodada2.py pasta_rodada2 [vardo-escolhido]
- cortina.png  -> assets/cortina.webp (só o veludo do meio, sem o babado de cima nem as franjas laterais)
- rosa.png     -> rosa recortada + 5 cartas do baralho em leque e em perspectiva atrás -> assets/logo-centro.webp
- gramofone.png -> assets/gramofone.webp (sem fundo)
- vela-*.png   -> assets/velas/vela-*.webp
- vardo escolhido -> assets/carroca-corpo.webp + assets/carroca-roda.webp (rodas achadas à mão, ver RODAS)
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from rembg import remove, new_session

ORIGEM = Path(sys.argv[1])
RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "assets"
sessao = new_session("isnet-general-use")

def sem_fundo(img):
    out = remove(img.convert("RGB"), session=sessao, alpha_matting=True, alpha_matting_foreground_threshold=240,
                 alpha_matting_background_threshold=15, alpha_matting_erode_size=8)
    return out.crop(out.getbbox())

# ---------- cortina: recorta o veludo do meio ----------
c = Image.open(ORIGEM / "cortina.png").convert("RGB")
w, h = c.size
c.crop((int(w * .3), int(h * .15), int(w * .7), h)).save(ASSETS / "cortina.webp", "WEBP", quality=86, method=6)
print("cortina ok")

# ---------- logo: cartas em perspectiva atrás da rosa ----------
def coeficientes(origem, destino):
    """Coeficientes da transformação de perspectiva do PIL (destino -> origem)."""
    m = []
    for (x, y), (u, v) in zip(destino, origem):
        m.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); m.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    A = np.array(m, dtype=float); B = np.array(origem, dtype=float).reshape(8)
    return np.linalg.solve(A, B).tolist()

TAM = 1000
leque = Image.new("RGBA", (TAM, TAM), (0, 0, 0, 0))
cartas = [9, 32, 24, 31, 33]
ch = 560; cw = round(ch * 360 / 840)
piv = (TAM // 2, 900)
for ang, n in zip([-44, -22, 0, 22, 44], cartas):
    carta = Image.open(ASSETS / "cartas" / f"carta-{n:02d}.webp").convert("RGBA").resize((cw, ch), Image.LANCZOS)
    sombra = Image.new("RGBA", (cw + 40, ch + 40), (0, 0, 0, 0))
    sombra.paste((0, 0, 0, 150), (20, 20, cw + 20, ch + 20)); sombra = sombra.filter(ImageFilter.GaussianBlur(10))
    camada = Image.new("RGBA", (TAM, TAM), (0, 0, 0, 0))
    x, y = piv[0] - cw // 2, piv[1] - ch
    camada.alpha_composite(sombra, (x - 20 + 6, y - 20 + 10)); camada.alpha_composite(carta, (x, y))
    leque.alpha_composite(camada.rotate(-ang, center=piv, resample=Image.BICUBIC))
# perspectiva: o leque deita para trás (topo mais estreito e mais baixo)
orig = [(0, 0), (TAM, 0), (TAM, TAM), (0, TAM)]
dest = [(150, 210), (850, 210), (TAM, TAM), (0, TAM)]
leque = leque.transform((TAM, TAM), Image.PERSPECTIVE, coeficientes(orig, dest), Image.BICUBIC)

rosa = sem_fundo(Image.open(ORIGEM / "rosa.png"))
rh = 700; rosa = rosa.resize((round(rosa.width * rh / rosa.height), rh), Image.LANCZOS)
logo = leque.copy()
logo.alpha_composite(rosa, (TAM // 2 - rosa.width // 2, TAM - rh - 20))
logo = logo.crop(logo.getbbox())
logo.thumbnail((640, 640), Image.LANCZOS)
logo.save(ASSETS / "logo-centro.webp", "WEBP", quality=90, method=6)
print("logo ok", logo.size)

# ---------- gramofone ----------
g = sem_fundo(Image.open(ORIGEM / "gramofone.png"))
g.thumbnail((420, 420), Image.LANCZOS)
g.save(ASSETS / "gramofone.webp", "WEBP", quality=90, method=6)
print("gramofone ok", g.size)

# (a carroça que passeia é montada por ferramentas/rodas_carroca.py, a partir de carroca-ouro-recorte.png)

# ---------- velas ----------
(ASSETS / "velas").mkdir(exist_ok=True)
for p in sorted(ORIGEM.glob("vela-*.png")):
    v = Image.open(p).convert("RGB"); v.thumbnail((420, 560), Image.LANCZOS)
    v.save(ASSETS / "velas" / f"{p.stem}.webp", "WEBP", quality=84, method=6)
print("velas ok")
