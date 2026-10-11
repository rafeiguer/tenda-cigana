"""Rodada 6: cortinas abertas presas no meio (bordas da primeira página) e carroça cigana puxada por cavalos (de lado).
Pedidos curtos: o SDXL só lê os primeiros 77 tokens; o resto era cortado."""
import json
from pathlib import Path

NEG = ("people, face, hands, text, watermark, logo, cartoon, illustration, 3d render, lowres, blurry, "
       "window, wall, floor, furniture, valance, curtain rod, two curtains")
PRESA = ("full length {tecido} curtain tied back at the middle with a gold rope tassel tieback, "
         "graceful hourglass drape, isolated on black background, photorealistic, detailed fabric")
ROXO = "purple velvet brocade with gold paisley embroidery"
VERMELHO = "crimson red silk with gold embroidery"

VARDO = ("side view of an ornate golden romani vardo wagon pulled by two brown horses walking, "
         "big spoked wheels, flower garlands, brass lantern, whole horses visible, "
         "isolated on white background, photorealistic")
VARDO_NEG = ("people, rider, driver, three quarter view, scenery, grass, road, sky, text, watermark, "
             "cartoon, illustration, blurry, cropped, extra legs, deformed horse")

t = []
for s in (101, 102, 103):
    t.append({"nome": f"presa-roxa-{s}", "w": 832, "h": 1216, "seed": s, "prompt": PRESA.format(tecido=ROXO), "neg": NEG})
    t.append({"nome": f"presa-vermelha-{s}", "w": 832, "h": 1216, "seed": s, "prompt": PRESA.format(tecido=VERMELHO), "neg": NEG})
for s in (111, 112, 113, 114):
    t.append({"nome": f"vardo-cavalos-{s}", "w": 1536, "h": 640, "seed": s, "prompt": VARDO, "neg": VARDO_NEG})
Path(__file__).with_name("rodada6.json").write_text(json.dumps(t, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(t), "trabalhos")
