"""Monta o interior visto de cima: apaga o papel e a carta de jogo da imagem gerada (inpainting na RX 7900 XTX)
e deita sobre o veludo 5 cartas do baralho cigano + um monte de cartas viradas, em perspectiva.

Uso (Python do gerador, com diffusers e torch-directml): python ferramentas/montar_mesa.py interior-alto-b.png saida.png
"""
import math, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
import torch, torch_directml
from diffusers import StableDiffusionXLInpaintPipeline, DPMSolverMultistepScheduler

ASSETS = Path(__file__).resolve().parent.parent / "assets"
MODELO = r"C:\Users\Rafa\Desktop\foocus_novo\Fooocus\models\checkpoints\juggernautXL_v8Rundiffusion.safetensors"
base = Image.open(sys.argv[1]).convert("RGB")
W, H = base.size

# ---------- 1. apaga o papel emoldurado e a carta de jogo ----------
masc = Image.new("L", base.size, 0)
d = ImageDraw.Draw(masc)
d.polygon([(90, 395), (330, 355), (495, 520), (480, 600), (250, 655), (95, 600)], fill=255)   # papel
d.polygon([(480, 480), (640, 425), (780, 560), (640, 640), (560, 640)], fill=255)              # carta de jogo
masc = masc.filter(ImageFilter.MaxFilter(15))
# o veludo repintado fica guardado ao lado da saída: os ajustes das cartas não precisam repintar de novo
cache = Path(sys.argv[2]).with_name("veludo-repintado.png")
if cache.exists():
    mesa = Image.open(cache).convert("RGBA"); print("veludo do cache", flush=True)
else:
    i = next(i for i in range(torch_directml.device_count()) if "7900" in torch_directml.device_name(i))
    dev = torch_directml.device(i)
    print("usando", torch_directml.device_name(i), flush=True)
    pipe = StableDiffusionXLInpaintPipeline.from_single_file(MODELO, torch_dtype=torch.float32, use_safetensors=True)
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config, use_karras_sigmas=True, algorithm_type="dpmsolver++")
    pipe.enable_attention_slicing(); pipe.enable_vae_tiling()
    pipe = pipe.to(dev); pipe.set_progress_bar_config(disable=True)
    out = pipe(prompt="burgundy red velvet tablecloth with soft folds, a few scattered dried rose petals, warm candlelight, photorealistic",
               negative_prompt="paper, card, frame, text, letters, book, object, people, cartoon, blurry",
               image=base, mask_image=masc, width=W, height=H, strength=.99, num_inference_steps=32, guidance_scale=6.0,
               generator=torch.Generator().manual_seed(9)).images[0]
    mesa = Image.composite(out, base, masc.filter(ImageFilter.GaussianBlur(8))).convert("RGBA")
    mesa.save(cache)
    print("veludo repintado", flush=True)

# ---------- 2. cartas deitadas na mesa ----------
CW, CH, ACHATA = 118, 276, .62   # tamanho da carta na mesa e o quanto ela "deita" (visão do alto, inclinada)

def deitada(img, ang):
    """Gira a carta no plano da mesa e depois achata e estreita o topo (perspectiva)."""
    c = img.convert("RGBA").resize((CW, CH), Image.LANCZOS)
    # luz de vela: um pouco mais escura e puxada para o laranja, como o resto da cena
    rgb = ImageEnhance.Brightness(c.convert("RGB")).enhance(.78)
    rgb = Image.blend(rgb, Image.new("RGB", rgb.size, (255, 150, 70)), .12)
    c = Image.merge("RGBA", (*rgb.split(), c.getchannel("A")))
    borda = Image.new("RGBA", (CW + 4, CH + 4), (190, 150, 80, 255)); borda.alpha_composite(c, (2, 2)); c = borda
    c = c.rotate(-ang, expand=True, resample=Image.BICUBIC)
    w, h = c.size; nh = round(h * ACHATA)
    c = c.resize((w, nh), Image.LANCZOS)
    # estreita um pouco o topo: o que está mais longe parece menor
    k = .06 * w
    coef = _coef([(0, 0), (w, 0), (w, nh), (0, nh)], [(k, 0), (w - k, 0), (w, nh), (0, nh)])
    return c.transform((w, nh), Image.PERSPECTIVE, coef, Image.BICUBIC)

def _coef(origem, destino):
    import numpy as np
    m = []
    for (x, y), (u, v) in zip(destino, origem):
        m.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); m.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    return np.linalg.solve(np.array(m, float), np.array(origem, float).reshape(8)).tolist()

def pousa(img, cx, cy):
    sombra = Image.new("RGBA", img.size, (0, 0, 0, 0)); sombra.putalpha(img.getchannel("A").point(lambda a: int(a * .55)))
    sombra = sombra.filter(ImageFilter.GaussianBlur(7))
    mesa.alpha_composite(sombra, (int(cx - img.width / 2 + 7), int(cy - img.height / 2 + 9)))
    mesa.alpha_composite(img, (int(cx - img.width / 2), int(cy - img.height / 2)))

# monte de cartas viradas
verso = Image.open(ASSETS / "cartas" / "verso.webp")
for k in range(7):
    pousa(deitada(verso, 14 + k * .6), 860 + k * .8, 585 - k * 1.6)
# a tiragem: 5 cartas abertas em fila, levemente desalinhadas como se tivessem sido postas à mão
TIRAGEM = [(33, 175, 520, -8), (24, 305, 505, -3), (31, 440, 498, 2), (16, 575, 508, 6), (9, 708, 522, 10)]
for n, cx, cy, ang in TIRAGEM:
    pousa(deitada(Image.open(ASSETS / "cartas" / f"carta-{n:02d}.webp"), ang), cx, cy)

mesa.convert("RGB").save(sys.argv[2])
print("ok", sys.argv[2])
