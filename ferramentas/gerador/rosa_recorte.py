from pathlib import Path
from PIL import Image
from rembg import remove, new_session
p = Path(__file__).parent / "rodada2"
out = remove(Image.open(p / "rosa.png").convert("RGB"), session=new_session("isnet-general-use"), alpha_matting=True,
             alpha_matting_foreground_threshold=240, alpha_matting_background_threshold=15, alpha_matting_erode_size=8)
out.crop(out.getbbox()).save(p / "rosa-recorte.png"); print("ok")
