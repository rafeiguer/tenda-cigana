"""Rodada 7: carroça e cavalos separados, para os cavalos irem à frente dos varais (e mexerem as pernas).
Pedidos curtos (o SDXL só lê 77 tokens). Mesmo estilo da vardo-cavalos-112, que o Rafa gostou."""
import json
from pathlib import Path

CARROCA = ("side view of an ornate golden carved romani vardo wagon with red roses on the curved roof, "
           "two long golden shafts sticking out at the front, big golden spoked wheels, isolated on white background, photorealistic")
CARROCA_NEG = "horse, animal, people, rider, three quarter view, scenery, grass, road, text, watermark, cartoon, blurry, cropped"
CAVALOS = ("side view of two chestnut horses walking side by side facing right, golden harness collars, red flower headpieces, "
           "whole bodies and legs visible, isolated on white background, photorealistic")
CAVALOS_NEG = ("wagon, carriage, cart, people, rider, saddle, three quarter view, scenery, grass, text, watermark, cartoon, "
               "blurry, cropped, extra legs, deformed horse")
t = []
for s in (121, 122, 123):
    t.append({"nome": f"carroca-so-{s}", "w": 1344, "h": 768, "seed": s, "prompt": CARROCA, "neg": CARROCA_NEG})
for s in (131, 132, 133, 134):
    t.append({"nome": f"cavalos-so-{s}", "w": 1344, "h": 768, "seed": s, "prompt": CAVALOS, "neg": CAVALOS_NEG})
Path(__file__).with_name("rodada7.json").write_text(json.dumps(t, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(t), "trabalhos")
