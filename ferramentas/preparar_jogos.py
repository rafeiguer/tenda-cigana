"""Leva as imagens dos jogos (geradas na RX 7900 XTX) para assets/jogos.

Uso: python ferramentas/preparar_jogos.py pasta_rodada3
As moedas e a roda vieram sobre fundo preto: são recortadas em círculo (centro e raio medidos na imagem 1024x1024).
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ORIGEM = Path(sys.argv[1])
DESTINO = Path(__file__).resolve().parent.parent / "assets" / "jogos"
DESTINO.mkdir(parents=True, exist_ok=True)

def circulo(nome, cx, cy, r, lado):
    img = Image.open(ORIGEM / f"{nome}.png").convert("RGBA").crop((cx - r, cy - r, cx + r, cy + r))
    m = Image.new("L", img.size, 0); ImageDraw.Draw(m).ellipse((2, 2, 2 * r - 2, 2 * r - 2), fill=255)
    img.putalpha(m.filter(ImageFilter.GaussianBlur(1.5)))
    img.resize((lado, lado), Image.LANCZOS).save(DESTINO / f"{nome}.webp", "WEBP", quality=90, method=6)

circulo("moeda-lua", 512, 512, 432, 360)
circulo("moeda-rosa", 512, 512, 492, 360)
circulo("roda-fortuna", 512, 487, 476, 800)

m = Image.open(ORIGEM / "mao.png").convert("RGB"); m.thumbnail((832, 1216))
m.save(DESTINO / "mao.webp", "WEBP", quality=86, method=6)
x = Image.open(ORIGEM / "xicara.png").convert("RGB"); x.thumbnail((900, 900), Image.LANCZOS)
x.save(DESTINO / "xicara.webp", "WEBP", quality=86, method=6)
print("ok", sorted(p.name for p in DESTINO.iterdir()))
