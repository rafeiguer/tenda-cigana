"""Repinta a frente da carroça da vardo-cavalos-112.png sem os cavalos (inpainting do Juggernaut XL na RX 7900 XTX).
Os cavalos são recortados à parte (contorno em cavalos_contorno.py) e vão à frente dos varais no site.

Uso: python separar_cavalos.py pasta_r6 pasta_saida
Saída: carroca-sem-cavalos-<seed>.png (algumas sementes, para escolher).
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import torch, torch_directml
from diffusers import StableDiffusionXLInpaintPipeline, DPMSolverMultistepScheduler
from cavalos_contorno import CAVALOS, PERNA_SOLTA

ORIGEM, SAIDA = Path(sys.argv[1]), Path(sys.argv[2])
SAIDA.mkdir(parents=True, exist_ok=True)
MODELO = r"C:\Users\Rafa\Desktop\foocus_novo\Fooocus\models\checkpoints\juggernautXL_v8Rundiffusion.safetensors"
PROMPT = ("side view of an ornate golden carved romani vardo wagon with red roses on the roof, golden carved panels, "
          "big golden spoked wooden wheels, plain light gray studio background, photorealistic")
NEG = "horse, animal, legs, hooves, harness, people, text, watermark, cartoon, blurry"

img = Image.open(ORIGEM / "vardo-cavalos-112.png").convert("RGB")
m = Image.new("L", img.size, 0)
d = ImageDraw.Draw(m)
d.polygon(CAVALOS, fill=255)
d.polygon(PERNA_SOLTA, fill=255)
m = m.filter(ImageFilter.MaxFilter(17))  # folga em volta do contorno

i = next(i for i in range(torch_directml.device_count()) if "7900" in torch_directml.device_name(i))
dev = torch_directml.device(i)
print("usando", torch_directml.device_name(i), flush=True)
pipe = StableDiffusionXLInpaintPipeline.from_single_file(MODELO, torch_dtype=torch.float32, use_safetensors=True)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config, use_karras_sigmas=True, algorithm_type="dpmsolver++")
pipe = pipe.to(dev); pipe.set_progress_bar_config(disable=True)
for seed in (141, 142, 143):
    g = torch.Generator().manual_seed(seed)
    out = pipe(prompt=PROMPT, negative_prompt=NEG, image=img, mask_image=m, width=img.width, height=img.height,
               strength=1.0, num_inference_steps=32, guidance_scale=6.0, generator=g).images[0]
    suave = m.filter(ImageFilter.GaussianBlur(6))
    Image.composite(out, img, suave).save(SAIDA / f"carroca-sem-cavalos-{seed}.png")
    print("ok", seed, flush=True)
