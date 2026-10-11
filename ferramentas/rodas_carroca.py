"""Monta a carroça que passeia a partir da foto "Entre na carroça" recortada (carroca-ouro-recorte.png, 736x736).

Uso: python ferramentas/rodas_carroca.py carroca-ouro-recorte.png

A foto é em perspectiva: cada roda é uma elipse inclinada, com o aro grosso de um lado só.
Por isso o aro fica parado no corpo da carroça (ele é redondo e parece igual girando) e só o miolo
(raios e cubo, dentro do aro) vira uma peça que gira: ela é "desentortada" para um círculo aqui
e o CSS a entorta de volta (rotate + scaleX) enquanto ela gira.
"""
import math, sys
from pathlib import Path
from PIL import Image, ImageDraw

ASSETS = Path(__file__).resolve().parent.parent / "assets"
# miolo de cada roda medido na foto: centro, semi-eixo menor (rx), maior (ry), inclinação do eixo maior em graus
RODAS = [(145, 481, 44, 72, -4), (392, 561, 50, 67, -3)]

co = Image.open(sys.argv[1]).convert("RGBA")
caixa = co.getbbox()

def elipse(cx, cy, rx, ry, ang, n=180):
    a = math.radians(ang); pts = []
    for k in range(n):
        t = 2 * math.pi * k / n; x, y = rx * math.cos(t), ry * math.sin(t)
        pts.append((cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)))
    return pts

pecas = []
for i, (cx, cy, rx, ry, ang) in enumerate(RODAS):
    m = int(ry + 10)
    q = co.crop((cx - m, cy - m, cx + m, cy + m))
    q = q.rotate(ang, center=(m, m), resample=Image.BICUBIC)                       # endireita o eixo maior
    q = q.resize((round(2 * m * ry / rx), 2 * m), Image.LANCZOS)                   # desachata: vira círculo de raio ry
    c = q.width // 2
    q = q.crop((c - ry, m - ry, c + ry, m + ry))
    mk = Image.new("L", q.size, 0); ImageDraw.Draw(mk).ellipse((0, 0, 2 * ry - 1, 2 * ry - 1), fill=255)
    q.putalpha(Image.composite(q.getchannel("A"), Image.new("L", q.size, 0), mk))
    q.save(ASSETS / f"carroca-roda{i + 1}.webp", "WEBP", quality=92, method=6)
    pecas.append((cx, cy, rx, ry, ang))

corpo = co.copy(); a = corpo.getchannel("A"); d = ImageDraw.Draw(a)
for cx, cy, rx, ry, ang in RODAS:
    d.polygon(elipse(cx, cy, rx - 1.5, ry - 1.5, ang), fill=0)   # tira o miolo; o aro continua
corpo.putalpha(a); corpo = corpo.crop(caixa)
corpo.save(ASSETS / "carroca-corpo.webp", "WEBP", quality=88, method=6)
W, H = corpo.size
for i, (cx, cy, rx, ry, ang) in enumerate(pecas):
    print(f'roda{i + 1}: style="--x:{100 * (cx - caixa[0]) / W:.2f}%;--y:{100 * (cy - caixa[1]) / H:.2f}%;'
          f'--h:{100 * 2 * ry / H:.2f}%;--k:{rx / ry:.3f};--a:{ang}deg"')
print("corpo", corpo.size)
