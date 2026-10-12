"""Rodada 9: imagens da entrada da tenda (o filme da primeira página).

Uso: python preparar_tenda.py pasta_r9 fora_fechada.png dentro.png
- assets/tenda-fora.webp: a tenda com a entrada aberta (fora-152), com o vão escuro da entrada vazado
  (transparente), para o interior aparecer por ele enquanto a câmera anda;
- assets/tenda-aba-esq.webp / -dir.webp: as abas fechadas (da repintura), cada uma numa imagem do mesmo
  tamanho da foto, só com o pano dela; a divisão é a fresta do meio;
- assets/tenda-dentro.webp: o interior escolhido.
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent / "gerador"))
from porta_medidas import PORTA, LANTERNAS, FRESTA  # noqa: E402

R9, FECHADA, DENTRO = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
ASSETS = Path(__file__).resolve().parent.parent / "assets"
aberta = Image.open(R9 / "fora-152.png").convert("RGBA")
fechada = Image.open(FECHADA).convert("RGBA")
W, H = aberta.size

vao = Image.new("L", (W, H), 0)
d = ImageDraw.Draw(vao)
d.polygon(PORTA, fill=255)
for r in LANTERNAS:
    d.rectangle(r, fill=0)
vao = vao.filter(ImageFilter.GaussianBlur(2))

# fora: o vão vira transparente (o interior aparece atrás); as bordas ficam macias
a = np.asarray(aberta.getchannel("A")).astype(np.float32) * (1 - np.asarray(vao) / 255)
fora = aberta.copy(); fora.putalpha(Image.fromarray(a.astype(np.uint8)))
fora.save(ASSETS / "tenda-fora.webp", "WEBP", quality=88, method=6)

# abas: o pano da repintura dentro do vão, dividido na fresta
for nome, lado in (("tenda-aba-esq", "esq"), ("tenda-aba-dir", "dir")):
    m = np.asarray(vao).astype(np.float32).copy()
    if lado == "esq":
        m[:, FRESTA:] = 0
    else:
        m[:, :FRESTA] = 0
    aba = fechada.copy(); aba.putalpha(Image.fromarray(m.astype(np.uint8)))
    aba.save(ASSETS / f"{nome}.webp", "WEBP", quality=88, method=6)

Image.open(DENTRO).convert("RGB").save(ASSETS / "tenda-dentro.webp", "WEBP", quality=88, method=6)
print("ok")
