"""Cortinas da abertura (rodada 5): exporta as fotos escolhidas para assets/.

Uso: python preparar_cortinas.py pasta_com_as_geradas
Geradas por gerador/montar_rodada5.py + gerador/gerar.py.
"""
import sys
from pathlib import Path
from PIL import Image

ORIGEM = Path(sys.argv[1])
ASSETS = Path(__file__).resolve().parent.parent / "assets"
for nome, escolhida in (("cortina-roxa", "roxa-93"), ("cortina-vermelha", "vermelha-91")):
    Image.open(ORIGEM / f"{escolhida}.png").convert("RGB").save(ASSETS / f"{nome}.webp", "WEBP", quality=86, method=6)
    print(nome, "ok")
