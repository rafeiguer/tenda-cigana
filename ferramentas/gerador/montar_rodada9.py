"""Rodada 9: a entrada da tenda como num filme (câmera na altura dos olhos do cliente).
- fora: a entrada da tenda à noite, com as abas fechadas e luz escapando pela fresta;
- dentro: o interior visto de quem acabou de entrar, com a mesa e os objetos que levam às páginas.
Pedidos curtos (o SDXL só lê 77 tokens)."""
import json
from pathlib import Path

NEG = "people, person, woman, man, face, hands, text, letters, watermark, logo, cartoon, anime, illustration, 3d render, lowres, blurry, deformed"
FORA = ("eye level view of the closed entrance of a romani fortune teller tent at night, burgundy and gold striped canvas, "
        "two closed door flaps in the center, brass lanterns on both sides, warm candlelight glowing through the gap, starry sky, photorealistic, cinematic")
DENTRO = ("eye level view inside a cozy romani fortune teller tent, round table with burgundy velvet cloth, crystal ball, "
          "fortune cards, porcelain coffee cup, lit candles, hanging lanterns, purple and red silk draped walls, oriental rugs, photorealistic, cinematic")
DENTRO_PAREDE = ("eye level view inside a romani fortune teller tent, round velvet table with crystal ball and cards, "
                 "a big wooden wheel of fortune on the back wall, colorful ribbons, lanterns, candles, silk drapes, photorealistic, cinematic")
t = []
for s in (151, 152, 153, 154):
    t.append({"nome": f"fora-{s}", "w": 1344, "h": 768, "seed": s, "prompt": FORA, "neg": NEG + ", open door, interior"})
for s in (161, 162, 163):
    t.append({"nome": f"dentro-{s}", "w": 1344, "h": 768, "seed": s, "prompt": DENTRO, "neg": NEG})
for s in (171, 172, 173):
    t.append({"nome": f"dentro-parede-{s}", "w": 1344, "h": 768, "seed": s, "prompt": DENTRO_PAREDE, "neg": NEG})
Path(__file__).with_name("rodada9.json").write_text(json.dumps(t, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(t), "trabalhos")
