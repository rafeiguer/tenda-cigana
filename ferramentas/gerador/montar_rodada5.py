"""Cortinas da abertura no tom do fundo da foto 734a6773...jpg: roxa bordada com franja dourada (esquerda) e vermelha de seda (direita)."""
import json
from pathlib import Path

NEG = ("people, person, woman, face, hands, text, letters, watermark, logo, cartoon, anime, illustration, 3d render, lowres, blurry, deformed, "
       "window, room, floor, wall, furniture, valance, pelmet, swag, tieback, tassels, medallion, rod")
ROXA = ("close-up of a hanging deep purple and violet velvet brocade curtain covered all over with gold and magenta paisley embroidery, "
        "soft deep vertical folds filling the entire frame edge to edge from top to bottom, a thin golden fringe trim running straight down its right edge, "
        "warm candlelight from the right, faint wisps of blue incense smoke, photorealistic, highly detailed fabric texture")
VERMELHA = ("close-up of a hanging crimson and rose red silk curtain with small scattered gold embroidered ornaments, "
            "soft deep vertical folds filling the entire frame edge to edge from top to bottom, glowing with warm golden candlelight, dark moody shadows, "
            "photorealistic, highly detailed fabric texture")
t = []
for s in (91, 92, 93, 94):
    t.append({"nome": f"roxa-{s}", "w": 896, "h": 1152, "seed": s, "prompt": ROXA, "neg": NEG})
    t.append({"nome": f"vermelha-{s}", "w": 896, "h": 1152, "seed": s, "prompt": VERMELHA, "neg": NEG})
Path(__file__).with_name("rodada5.json").write_text(json.dumps(t, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(t), "trabalhos")
