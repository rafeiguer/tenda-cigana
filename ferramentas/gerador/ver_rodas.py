"""Amplia as duas rodas da frente e desenha por cima a elipse candidata (centro, semi-eixos, inclinação)."""
import sys, math
from pathlib import Path
from PIL import Image, ImageDraw

p = Path(__file__).parent / "rodada2"
img = Image.open(p / "carroca-ouro-recorte.png").convert("RGBA")
fundo = Image.new("RGBA", img.size, (30, 10, 16, 255)); fundo.alpha_composite(img)
# cada roda: cx, cy, rx (semi-eixo menor), ry (maior), ângulo do eixo maior em graus (0 = vertical)
RODAS = [tuple(map(float, a.split(","))) for a in sys.argv[1:]]
Z = 3
pecas = []
for cx, cy, rx, ry, ang in RODAS:
    m = 115
    c = fundo.crop((int(cx - m), int(cy - m), int(cx + m), int(cy + m))).resize((m * 2 * Z,) * 2, Image.LANCZOS)
    d = ImageDraw.Draw(c)
    pts = []
    for k in range(120):
        t = 2 * math.pi * k / 120
        x, y = rx * math.cos(t), ry * math.sin(t)
        a = math.radians(ang)
        xr, yr = x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)
        pts.append(((xr + m) * Z, (yr + m) * Z))
    d.line(pts + [pts[0]], fill=(0, 255, 0, 255), width=3)
    d.ellipse(((m - 2) * Z, (m - 2) * Z, (m + 2) * Z, (m + 2) * Z), fill=(255, 0, 0, 255))
    pecas.append(c)
folha = Image.new("RGBA", (sum(x.width for x in pecas) + 10, pecas[0].height), "white")
x = 0
for c in pecas:
    folha.paste(c, (x, 0)); x += c.width + 10
folha.convert("RGB").save(p / "rodas.jpg", quality=88)
print("ok")
