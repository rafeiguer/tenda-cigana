import json
from pathlib import Path

NEG = "people, person, hands, text, letters, watermark, logo, cartoon, anime, illustration, 3d render, lowres, blurry, deformed"
ISOLADO = ", isolated on pure black background, studio product photo, photorealistic, highly detailed, sharp focus"

VARDO = ("perfect side view profile of a golden wooden romani vardo wagon with a rounded barrel roof of polished golden wood planks, "
         "ornate carved gold baroque trim on the roof edge, two arched windows with cream curtains, pink and purple flower garlands and flower boxes, "
         "a brass lantern hanging by the front door, four large wooden spoked wheels with golden rims, two wheels fully visible, warm golden wood tones, "
         "isolated on plain white background, photorealistic product photo, sharp")
VARDO_NEG = "horse, people, perspective view, three quarter view, background scenery, grass, road, purple fabric roof, canopy, text, watermark, cartoon, blurry, cropped"

VELAS = {
    "branca": "white", "vermelha": "deep red", "rosa": "soft pink", "amarela": "golden yellow",
    "laranja": "orange", "verde": "emerald green", "azul": "royal blue", "lilas": "lilac purple",
}

t = [
    {"nome": "cortina", "w": 832, "h": 1216, "seed": 51,
     "prompt": "luxurious heavy deep red velvet theater curtain, closed, front view filling the whole frame, rich vertical folds, "
               "soft warm light from above, gold fringe trim at the bottom, photorealistic, highly detailed fabric texture",
     "neg": NEG + ", stage, floor, room, people"},
    {"nome": "rosa", "w": 1024, "h": 1024, "seed": 52,
     "prompt": "a single perfect deep red rose in full bloom with a short stem and two green leaves, velvety petals with dew drops" + ISOLADO, "neg": NEG},
    {"nome": "gramofone", "w": 1024, "h": 1024, "seed": 53,
     "prompt": "antique brass gramophone with a large golden flower shaped horn and a carved dark wooden base, side view, no record on the turntable" + ISOLADO,
     "neg": NEG + ", record, vinyl disc"},
]
for i, s in enumerate([61, 62, 63]):
    t.append({"nome": f"vardo-ouro-{i + 1}", "w": 1344, "h": 768, "seed": s, "prompt": VARDO, "neg": VARDO_NEG})
for nome, cor in VELAS.items():
    t.append({"nome": f"vela-{nome}", "w": 768, "h": 1024, "seed": 70,
              "prompt": f"a single tall {cor} wax pillar candle, lit, with a soft warm flame and a little melted wax, on a small antique brass holder, "
                        "centered, dark moody background, cinematic candlelight, photorealistic, highly detailed",
              "neg": NEG + ", multiple candles"})
Path(__file__).with_name("rodada2.json").write_text(json.dumps(t, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(t), "trabalhos")
