"""Tira o fundo da carroça de lado, da bola de cristal e da bola da logo (rembg, no processador)."""
import sys
from pathlib import Path
from PIL import Image
from rembg import remove, new_session

pasta = Path(sys.argv[1])
sessao = new_session("isnet-general-use")
for nome in ["vardo-a", "bola", "logo-bola"]:
    img = Image.open(pasta / f"{nome}.png").convert("RGB")
    out = remove(img, session=sessao, alpha_matting=True, alpha_matting_foreground_threshold=240,
                 alpha_matting_background_threshold=15, alpha_matting_erode_size=8)
    out = out.crop(out.getbbox())
    out.save(pasta / f"{nome}-recorte.png")
    print("ok", nome, out.size, flush=True)
