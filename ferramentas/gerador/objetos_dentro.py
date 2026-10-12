"""Põe na cena de dentro (dentro-162.png) os objetos que levam às páginas e que a imagem não trouxe:
a bola de cristal e as cartas na mesa do centro e a xícara na mesinha da direita (inpainting na RX 7900 XTX).

Uso: python objetos_dentro.py pasta_r9 semente
Saída: dentro-objetos-<semente>.png. Uma semente por processo (o inpainting estoura a memória na 2ª imagem).
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import torch, torch_directml
from diffusers import StableDiffusionXLInpaintPipeline, DPMSolverMultistepScheduler

PASTA, SEED = Path(sys.argv[1]), int(sys.argv[2])
MODELO = r"C:\Users\Rafa\Desktop\foocus_novo\Fooocus\models\checkpoints\juggernautXL_v8Rundiffusion.safetensors"
PROMPT = ("a glowing crystal ball on a golden stand in the middle of a round burgundy velvet table, old fortune cards spread "
          "in front of it, a porcelain coffee cup on the small side table, candlelight, photorealistic")
NEG = "people, hands, text, watermark, cartoon, blurry, deformed"
# medidas na dentro-162.png (1344x768)
BOLA = (585, 370, 705, 478)          # no meio da mesa, entre as velas
CARTAS = (500, 462, 790, 505)        # a frente do tampo da mesa
XICARA = (1222, 455, 1292, 505)      # o tampo da mesinha, à direita do abajur

img = Image.open(PASTA / "dentro-162.png").convert("RGB")
m = Image.new("L", img.size, 0)
d = ImageDraw.Draw(m)
d.ellipse(BOLA, fill=255)
d.ellipse(CARTAS, fill=255)
d.ellipse(XICARA, fill=255)

i = next(i for i in range(torch_directml.device_count()) if "7900" in torch_directml.device_name(i))
dev = torch_directml.device(i)
print("usando", torch_directml.device_name(i), flush=True)
pipe = StableDiffusionXLInpaintPipeline.from_single_file(MODELO, torch_dtype=torch.float32, use_safetensors=True)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config, use_karras_sigmas=True, algorithm_type="dpmsolver++")
pipe = pipe.to(dev); pipe.set_progress_bar_config(disable=True)
g = torch.Generator().manual_seed(SEED)
out = pipe(prompt=PROMPT, negative_prompt=NEG, image=img, mask_image=m, width=img.width, height=img.height,
           strength=.98, num_inference_steps=32, guidance_scale=6.5, generator=g).images[0]
Image.composite(out, img, m.filter(ImageFilter.GaussianBlur(5))).save(PASTA / f"dentro-objetos-{SEED}.png")
print("ok", SEED, flush=True)
