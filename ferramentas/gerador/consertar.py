"""Conserta as cartas 20 (Parque) e 36 (Cruz), que vieram com marcas por cima na imagem original.

Repinta só a área estragada com o Juggernaut XL (inpainting) na RX 7900 XTX; o resto da carta fica igual.
Uso: python consertar.py pasta_ampliadas
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import torch, torch_directml
from diffusers import StableDiffusionXLInpaintPipeline, DPMSolverMultistepScheduler

PASTA = Path(sys.argv[1])
MODELO = r"C:\Users\Rafa\Desktop\foocus_novo\Fooocus\models\checkpoints\juggernautXL_v8Rundiffusion.safetensors"
ESTILO = "antique vintage lithograph illustration, hand painted, muted warm colors, aged paper, soft painterly detail, "
NEG = "text, letters, watermark, logo, circle, frame, border, people, cartoon, 3d render, blurry, lowres"

def mascara_vazia(img):
    return Image.new("L", img.size, 0)

# ---------- 36: troca a metade de baixo pela moldura e faixa limpas da carta 23 ----------
c36 = Image.open(PASTA / "carta-36.png").convert("RGB")
c23 = Image.open(PASTA / "carta-23.png").convert("RGB").resize(c36.size, Image.LANCZOS)
W, H = c36.size
CORTE = 440
base36 = c36.copy()
base36.paste(c23.crop((0, CORTE, W, H)), (0, CORTE))
# apaga o texto "OS RATOS" da faixa e escreve "A CRUZ"
a = np.asarray(base36).astype(int)
linha_faixa = [y for y in range(int(H * .84), H - 10) if a[y, W // 2].sum() > 600]
y0, y1 = min(linha_faixa), max(linha_faixa)
cor = tuple(int(v) for v in np.median(a[y0 + 4:y1 - 4, 40:60].reshape(-1, 3), axis=0))
d = ImageDraw.Draw(base36)
d.rectangle((44, y0 + 6, W - 44, y1 - 6), fill=cor)
fonte = ImageFont.truetype(r"C:\Windows\Fonts\timesbd.ttf", 46)
d.text((W / 2, (y0 + y1) / 2 + 2), "A CRUZ", font=fonte, fill=(34, 24, 16), anchor="mm")
m36 = mascara_vazia(c36)
ImageDraw.Draw(m36).rectangle((16, CORTE - 60, W - 16, y0 - 14), fill=255)
p36 = "a simple wooden cross standing on a grassy hill, golden sunset sky with clouds, spiritual light, rocks and grass at the base"

# ---------- 20: véu em forma de coração no alto e círculo claro no caminho ----------
c20 = Image.open(PASTA / "carta-20-original.png").convert("RGB")
W2, H2 = c20.size
m20 = mascara_vazia(c20)
d2 = ImageDraw.Draw(m20)
d2.ellipse((80, -30, 360, 220), fill=255)          # coração
d2.ellipse((80, 395, 370, 675), fill=255)         # círculo no caminho
d2.ellipse((128, -6, 250, 112), fill=0)            # protege o círculo do número
d2.rectangle((0, 610, W2, H2), fill=0)             # protege a faixa do nome
d2.rectangle((0, 0, 14, H2), fill=0); d2.rectangle((W2 - 16, 0, W2, H2), fill=0); d2.rectangle((0, 0, W2, 10), fill=0)
p20 = "a romantic garden park with a green arch of climbing roses, cloudy sky, tall trees, stone paved path leading to a fountain"

# ---------- inpainting na placa certa ----------
i = next(i for i in range(torch_directml.device_count()) if "7900" in torch_directml.device_name(i))
dev = torch_directml.device(i)
print("usando", torch_directml.device_name(i), flush=True)
pipe = StableDiffusionXLInpaintPipeline.from_single_file(MODELO, torch_dtype=torch.float32, use_safetensors=True)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config, use_karras_sigmas=True, algorithm_type="dpmsolver++")
pipe = pipe.to(dev); pipe.set_progress_bar_config(disable=True)

def repintar(img, masc, prompt, forca, seed):
    h = 1216; w = round(img.width * h / img.height / 8) * 8
    g = torch.Generator().manual_seed(seed)
    out = pipe(prompt=ESTILO + prompt, negative_prompt=NEG, image=img.resize((w, h), Image.LANCZOS),
               mask_image=masc.resize((w, h)), width=w, height=h, strength=forca,
               num_inference_steps=32, guidance_scale=6.0, generator=g).images[0]
    out = out.resize(img.size, Image.LANCZOS)
    suave = masc.filter(ImageFilter.GaussianBlur(10))
    return Image.composite(out, img, suave)

for nome, img, masc, prompt, forca in [("carta-20", c20, m20, p20, 1.0)]:
    img.save(PASTA / f"{nome}-antes.png")
    repintar(img, masc, prompt, forca, 36).save(PASTA / f"{nome}.png")
    print("ok", nome, flush=True)

