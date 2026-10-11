"""Converte as fotos da pasta "site thays" (área de trabalho) para os assets do site.

Uso: python ferramentas/preparar_imagens.py
"""
from pathlib import Path
from PIL import Image, ImageOps

ORIGEM = Path.home() / "Desktop" / "site thays"
DESTINO = Path(__file__).resolve().parent.parent / "assets"
DESTINO.mkdir(exist_ok=True)

FOTOS = {
    "17f0e89fa6a801112d01c68d5f2444cf.jpg": "carroca-ouro.webp",
    "65242ac2f5b6092e61f9edca27974093.jpg": "velas.webp",
    "eaef34ac08fa2373cb5490475f973889.jpg": "mesa-ouro.webp",
    "60428adcdbdbb3db27e263d4fd4ac1cc.jpg": "carroca-jardim.webp",
    "WhatsApp Image 2026-10-10 at 16.41.14.jpeg": "ervas.webp",
}

for nome, saida in FOTOS.items():
    img = Image.open(ORIGEM / nome).convert("RGB")
    if img.width > 1100:
        img = img.resize((1100, round(img.height * 1100 / img.width)), Image.LANCZOS)
    img.save(DESTINO / saida, "WEBP", quality=82, method=6)
    print(saida, img.size)

# Silhueta dos dançarinos: preto vira dourado e o branco vira transparente.
img = Image.open(ORIGEM / "e3e422267604365426af44838fcc0dec.jpg").convert("L")
w, h = img.size
img = img.crop((0, int(h * 0.38), w, h))
alfa = ImageOps.invert(img).point(lambda v: 0 if v < 40 else min(255, int((v - 40) * 1.3)))
alfa = alfa.resize((alfa.width // 2, alfa.height // 2), Image.LANCZOS)
ouro = Image.new("RGBA", alfa.size, (226, 172, 86, 255))
ouro.putalpha(alfa)
ouro = ouro.crop(ouro.getbbox())
ouro.save(DESTINO / "danca.webp", "WEBP", quality=88, method=6)
print("danca.webp", ouro.size)
