"""Leva as cartas ampliadas (Real-ESRGAN, com 20 e 36 consertadas) e o verso gerado para assets/cartas.

Uso: python ferramentas/exportar_cartas.py pasta_ampliadas verso.png
Todas ficam com 360 x 840, o formato do baralho na imagem de referência.
"""
import sys
from pathlib import Path
from PIL import Image, ImageOps

ORIGEM = Path(sys.argv[1])
DESTINO = Path(__file__).resolve().parent.parent / "assets" / "cartas"
DESTINO.mkdir(parents=True, exist_ok=True)
TAM = (360, 840)

for n in range(1, 37):
    img = Image.open(ORIGEM / f"carta-{n:02d}.png").convert("RGB")
    # as linhas do pôster têm alturas um pouco diferentes; ajusta sem cortar a moldura
    img = img.resize(TAM, Image.LANCZOS)
    img.save(DESTINO / f"carta-{n:02d}.webp", "WEBP", quality=86, method=6)

verso = Image.open(sys.argv[2]).convert("RGB")
ImageOps.fit(verso, TAM, Image.LANCZOS).save(DESTINO / "verso.webp", "WEBP", quality=86, method=6)
print("ok", len(list(DESTINO.glob("*.webp"))), "arquivos em", DESTINO)
