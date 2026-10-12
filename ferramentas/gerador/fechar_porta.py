"""Repinta a entrada da tenda (fora-152.png) com as abas fechadas, para a abertura do filme.
As abas fechadas são recortadas dessa repintura e, ao entrar, giram e revelam a entrada original, aberta.

Uso: python fechar_porta.py pasta_r9 semente
Saída: fora-fechada-<semente>.png. Uma semente por vez: na rodada 7 o inpainting estourou a memória da placa
na segunda imagem do mesmo processo (o VAE fica na placa neste pipeline).
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import torch, torch_directml
from diffusers import StableDiffusionXLInpaintPipeline, DPMSolverMultistepScheduler

PASTA, SEED = Path(sys.argv[1]), int(sys.argv[2])
MODELO = r"C:\Users\Rafa\Desktop\foocus_novo\Fooocus\models\checkpoints\juggernautXL_v8Rundiffusion.safetensors"
PROMPT = ("closed entrance of a red tent at night, two heavy crimson velvet door flaps hanging closed and meeting in the middle, "
          "gold trim on the edges, warm candlelight glowing through the narrow gap, photorealistic")
NEG = "open door, bed, cushions, interior, people, text, watermark, cartoon, blurry"
from porta_medidas import PORTA, LANTERNAS  # vão da entrada e as lanternas da frente (ficam como estão)

img = Image.open(PASTA / "fora-152.png").convert("RGB")
m = Image.new("L", img.size, 0)
d = ImageDraw.Draw(m)
d.polygon(PORTA, fill=255)
for r in LANTERNAS:
    d.rectangle(r, fill=0)
m.save(PASTA / "porta-mascara.png")

i = next(i for i in range(torch_directml.device_count()) if "7900" in torch_directml.device_name(i))
dev = torch_directml.device(i)
print("usando", torch_directml.device_name(i), flush=True)
pipe = StableDiffusionXLInpaintPipeline.from_single_file(MODELO, torch_dtype=torch.float32, use_safetensors=True)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config, use_karras_sigmas=True, algorithm_type="dpmsolver++")
pipe = pipe.to(dev); pipe.set_progress_bar_config(disable=True)
g = torch.Generator().manual_seed(SEED)
out = pipe(prompt=PROMPT, negative_prompt=NEG, image=img, mask_image=m, width=img.width, height=img.height,
           strength=1.0, num_inference_steps=32, guidance_scale=6.0, generator=g).images[0]
Image.composite(out, img, m.filter(ImageFilter.GaussianBlur(4))).save(PASTA / f"fora-fechada-{SEED}.png")
print("ok", SEED, flush=True)
