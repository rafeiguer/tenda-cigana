"""Prepara as imagens geradas na placa (Juggernaut XL) para o site.

Uso: python ferramentas/preparar_cenas.py pasta_cenas
- vardo-a-recorte.png -> carroca-corpo.webp + carroca-roda.webp (a roda gira por cima do corpo)
- interior-b.png -> interior.webp
- bola.png -> bola.webp
- logo-bola-recorte.png -> logo-bola.webp
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

ORIGEM = Path(sys.argv[1])
DESTINO = Path(__file__).resolve().parent.parent / "assets"

# rodas da frente medidas na imagem recortada (1091 x 738)
RODAS = [(262, 622), (822, 622)]
RAIO = 110

v = Image.open(ORIGEM / "vardo-a-recorte.png").convert("RGBA")
# a roda da direita é a mais nítida: vira a roda que gira nas duas posições
cx, cy = RODAS[1]
roda = v.crop((cx - RAIO, cy - RAIO, cx + RAIO, cy + RAIO))
mascara = Image.new("L", roda.size, 0)
ImageDraw.Draw(mascara).ellipse((0, 0, RAIO * 2 - 1, RAIO * 2 - 1), fill=255)
alfa = Image.composite(roda.getchannel("A"), Image.new("L", roda.size, 0), mascara)
roda.putalpha(alfa)
# corpo sem as rodas da frente (a roda girando cobre o buraco)
corpo = v.copy()
a = corpo.getchannel("A")
d = ImageDraw.Draw(a)
for x, y in RODAS:
    d.ellipse((x - RAIO + 4, y - RAIO + 4, x + RAIO - 4, y + RAIO - 4), fill=0)
corpo.putalpha(a)

escala = 0.5
corpo.resize((round(v.width * escala), round(v.height * escala)), Image.LANCZOS).save(DESTINO / "carroca-corpo.webp", "WEBP", quality=88, method=6)
roda.resize((round(RAIO * 2 * escala),) * 2, Image.LANCZOS).save(DESTINO / "carroca-roda.webp", "WEBP", quality=90, method=6)
print("carroça: corpo", corpo.size, "rodas em", RODAS, "raio", RAIO)

Image.open(ORIGEM / "interior-b.png").convert("RGB").save(DESTINO / "interior.webp", "WEBP", quality=84, method=6)
Image.open(ORIGEM / "bola.png").convert("RGB").save(DESTINO / "bola.webp", "WEBP", quality=86, method=6)
bm = Image.open(ORIGEM / "bola-recorte.png").convert("RGBA")
bm.resize((160, round(bm.height * 160 / bm.width)), Image.LANCZOS).save(DESTINO / "bola-mesa.webp", "WEBP", quality=90, method=6)
lb = Image.open(ORIGEM / "logo-bola-recorte.png").convert("RGBA")
lb.resize((round(lb.width * .5), round(lb.height * .5)), Image.LANCZOS).save(DESTINO / "logo-bola.webp", "WEBP", quality=90, method=6)
print("ok")
