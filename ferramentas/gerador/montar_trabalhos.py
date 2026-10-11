import json
from pathlib import Path

ESTILO = ("classical oil painting, 19th century romantic realism, full bleed canvas, warm golden hour light, "
          "rich burgundy and gold tones, soft dark vignette, fine detail, museum quality, realistic, the subject fills the frame: ")
NEG_CARTA = ("picture frame, gilded frame, border, table, candle, candles, tarot cards, playing cards, still life, room interior, "
             "text, letters, words, numbers, watermark, signature, cartoon, anime, 3d render, lowres, blurry, deformed")
COM_GENTE = {13, 28, 29}

CARTAS = {
    1: "a gentleman rider in black coat and top hat on a white horse galloping on a country road at dusk",
    2: "a four leaf clover with dew drops growing among wild grass and tiny flowers",
    3: "a tall wooden sailing ship with full sails on a golden sea at sunset",
    4: "a charming old stone cottage with warm lit windows and a garden path",
    5: "a large majestic old oak tree with deep roots in a green meadow",
    6: "dark dramatic storm clouds over a hill, rays of light breaking through",
    7: "a coiled green and brown serpent on a mossy stone, menacing gaze",
    8: "an ornate antique wooden coffin with carved details and dried roses, solemn mood",
    9: "a beautiful bouquet of pink and red roses tied with a silk ribbon",
    10: "an old scythe with curved steel blade leaning against a wheat field",
    11: "a coiled leather horse whip on a rustic wooden table",
    12: "two small songbirds perched together on a flowering branch",
    13: "a sweet little child in a lace dress holding a teddy bear, victorian portrait",
    14: "a red fox standing alert in an autumn forest, cunning eyes",
    15: "a large brown bear standing in a pine forest, powerful",
    16: "a deep blue night sky full of bright stars over silhouetted hills",
    17: "an elegant white stork standing by a pond in tall reeds",
    18: "a loyal golden retriever dog sitting, gentle eyes, warm light",
    19: "a tall medieval stone tower on a hill under a dramatic sky",
    20: "a romantic garden park with a rose arch, bench and flowering trees",
    21: "a rugged snow capped mountain peak with rocky cliffs",
    22: "a dirt road forking into two paths through a green countryside",
    23: "two grey mice nibbling on bread crumbs in a dark old cellar",
    24: "a red heart made of velvet surrounded by red roses and gold filigree",
    25: "an antique gold ring with a sparkling diamond on red velvet",
    26: "an old leather bound book with gold ornaments and a brass clasp, closed",
    27: "an old letter envelope sealed with red wax and a quill pen",
    28: "portrait of an elegant gypsy man with dark beard, embroidered vest, earring, candlelight",
    29: "portrait of a beautiful gypsy woman with long dark hair, red headscarf, gold earrings, candlelight",
    30: "white lilies in full bloom with green leaves, serene",
    31: "a radiant golden sun shining over a peaceful landscape with sunflowers",
    32: "a full moon glowing over a calm lake at night with reflections",
    33: "an ornate antique golden key on dark velvet",
    34: "two colorful koi fish swimming in clear water",
    35: "an old iron ship anchor resting on a sandy shore with rope",
    36: "a simple wooden cross on a hill at golden sunset, spiritual light",
}

trabalhos = [{
    "nome": "verso", "w": 832, "h": 1216, "seed": 7,
    "prompt": "ornate antique playing card back design, deep burgundy velvet with intricate gold filigree, "
              "a golden gypsy wagon wheel mandala in the center, symmetrical, luxurious, photorealistic, top view, flat lay",
    "neg": "text, letters, words, numbers, watermark, cartoon, blurry, lowres, people",
}]
for n, cena in CARTAS.items():
    neg = NEG_CARTA if n in COM_GENTE or n == 1 else NEG_CARTA + ", person, woman, man, people, human"
    trabalhos.append({"nome": f"carta-{n:02d}", "w": 832, "h": 1216, "seed": 100 + n, "prompt": ESTILO + cena, "neg": neg})
trabalhos += [
    {"nome": "interior", "w": 1344, "h": 768, "seed": 11,
     "prompt": "interior of a luxurious romani gypsy wagon vardo at night, curved wooden ceiling, purple and burgundy silk drapes, "
               "hanging moroccan mosaic lanterns glowing, a round table with velvet tablecloth, crystal ball, tarot cards, candles, "
               "gold coins, shelves with herb jars, embroidered cushions, warm candlelight, cinematic, photorealistic, highly detailed"},
    {"nome": "bola", "w": 1024, "h": 1024, "seed": 12,
     "prompt": "a glowing crystal ball on an ornate antique gold stand on a burgundy velvet table, mystical pink and violet mist inside, "
               "candles around, dark background, cinematic lighting, photorealistic, highly detailed, centered"},
    {"nome": "logo-bola", "w": 1024, "h": 1024, "seed": 13,
     "prompt": "a crystal ball on an ornate gold filigree stand with red roses around it, isolated on pure black background, "
               "magical rim light, luxurious, photorealistic, centered, product photo"},
]
Path(__file__).with_name("trabalhos.json").write_text(json.dumps(trabalhos, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(trabalhos), "trabalhos")
