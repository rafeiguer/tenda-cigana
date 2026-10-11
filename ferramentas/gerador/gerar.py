"""Gera imagens com o Juggernaut XL (SDXL) na placa AMD via DirectML, em modo leve.

Uso: python gerar.py trabalhos.json pasta_saida [quantos]
Gera no máximo `quantos` imagens pendentes (padrão 6) e sai.
Cada trabalho: {"nome", "prompt", "w", "h", "seed", "neg"?, "passos"?, "cfg"?}
"""
import json, sys, time, gc
from pathlib import Path
import torch, torch_directml
from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler, AutoencoderKL

MODELO = r"C:\Users\Rafa\Desktop\foocus_novo\Fooocus\models\checkpoints\juggernautXL_v8Rundiffusion.safetensors"
NEG_PADRAO = ("cartoon, anime, illustration for kids, childish, 3d render, cgi, flat colors, lowres, blurry, "
              "deformed, bad anatomy, extra fingers, watermark, signature, logo, text, letters, words, numbers, border, frame")

trabalhos = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
saida = Path(sys.argv[2]); saida.mkdir(parents=True, exist_ok=True)
quantos = int(sys.argv[3]) if len(sys.argv) > 3 else 6
pendentes = [t for t in trabalhos if not (saida / f"{t['nome']}.png").exists()][:quantos]
faltam = sum(not (saida / (t["nome"] + ".png")).exists() for t in trabalhos)
print(f"lote de {len(pendentes)} (faltam {faltam})", flush=True)
if not pendentes:
    sys.exit(0)

# O padrão (0) é o vídeo integrado do Ryzen, que trava o Windows com um modelo deste tamanho.
# Procura a RX 7900 XTX pelo nome e para se não achar.
indice = next((i for i in range(torch_directml.device_count()) if "7900" in torch_directml.device_name(i)), None)
if indice is None:
    sys.exit("RX 7900 XTX não encontrada no DirectML; não vou usar o vídeo integrado.")
dev = torch_directml.device(indice)
print("usando", torch_directml.device_name(indice), flush=True)
# Precisão cheia: em meia precisão o DirectML devolve imagem cinza. A RX 7900 XTX tem 24 GB, cabe.
pipe = StableDiffusionXLPipeline.from_single_file(MODELO, torch_dtype=torch.float32, use_safetensors=True)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config, use_karras_sigmas=True, algorithm_type="dpmsolver++")
pipe.enable_attention_slicing()
# o VAE (latente -> imagem) fica no processador: na placa ele estourava a memória em 1344x768
vae = pipe.vae
pipe.vae = None
pipe = pipe.to(dev)
pipe.vae = vae.to("cpu")
# com o VAE no processador o diffusers pode concluir que o pipeline roda no processador; força a placa
type(pipe)._execution_device = property(lambda self: dev)
pipe.set_progress_bar_config(disable=True)
print("modelo carregado", flush=True)

for t in pendentes:
    t0 = time.time()
    g = torch.Generator().manual_seed(t.get("seed", 1))
    lat = pipe(prompt=t["prompt"], negative_prompt=t.get("neg", NEG_PADRAO), width=t["w"], height=t["h"],
               num_inference_steps=t.get("passos", 28), guidance_scale=t.get("cfg", 5.0), generator=g,
               output_type="latent").images
    with torch.no_grad():
        px = vae.decode(lat.to("cpu", torch.float32) / vae.config.scaling_factor).sample
    img = pipe.image_processor.postprocess(px, output_type="pil")[0]
    img.save(saida / f"{t['nome']}.png")
    print(f"ok {t['nome']} ({time.time() - t0:.0f}s)", flush=True)
    gc.collect()
    time.sleep(5)  # respiro para a placa entre uma imagem e outra
