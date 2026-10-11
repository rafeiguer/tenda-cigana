"""Recorta a carroça dourada da foto original (sem o chão de pedras) e mostra uma grade para achar as rodas."""
from pathlib import Path
from PIL import Image, ImageDraw
from rembg import remove, new_session

foto = Path.home() / "Desktop" / "site thays" / "17f0e89fa6a801112d01c68d5f2444cf.jpg"
saida = Path(__file__).parent / "rodada2"
img = Image.open(foto).convert("RGB")
out = remove(img, session=new_session("isnet-general-use"), alpha_matting=True,
             alpha_matting_foreground_threshold=240, alpha_matting_background_threshold=15, alpha_matting_erode_size=6)
out.save(saida / "carroca-ouro-recorte.png")
b = Image.new("RGBA", out.size, (40, 12, 20, 255)); b.alpha_composite(out)
d = ImageDraw.Draw(b)
for x in range(0, out.width, 50): d.line((x, 0, x, out.height), fill=(0, 255, 0, 110)); d.text((x + 2, 2), str(x), fill="yellow")
for y in range(0, out.height, 50): d.line((0, y, out.width, y), fill=(0, 255, 0, 110)); d.text((2, y + 2), str(y), fill="yellow")
b.convert("RGB").save(saida / "carroca-ouro-grade.jpg", quality=88)
print("ok", out.size)
