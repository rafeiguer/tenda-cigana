# Gerador de imagens (Juggernaut XL na RX 7900 XTX)

Scripts usados para gerar as imagens realistas do site. O ambiente Python não fica no projeto (1,7 GB); para recriar:

```
cd ferramentas\gerador
uv venv --python "C:\Users\Rafa\Desktop\foocus_novo\.venv\Scripts\python.exe" .venv
uv pip install --python .venv\Scripts\python.exe "torch-directml>=0.2.5.dev240914" "diffusers==0.30.3" "transformers==4.42.4" "accelerate==0.32.1" safetensors pillow omegaconf "rembg==2.0.57" "onnxruntime==1.18.1"
```

Uso: `.venv\Scripts\python.exe gerar.py trabalhos.json pasta_saida 6` (gera no máximo 6 por vez).

**Cuidado:** no DirectML o dispositivo 0 é o vídeo integrado do Ryzen e dá tela azul. O `gerar.py` já procura a RX 7900 XTX pelo nome. Rodar em fp32 e com o VAE no processador (já está assim no script). Testar com 1 imagem antes de lotes.
