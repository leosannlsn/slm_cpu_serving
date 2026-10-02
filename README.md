# SLM CPU Serving — Workshop Repo

**Beyond ChatGPT: Real-Time AI Inference on Your Laptop**

This repo is currently in **Phase 1: Codespaces Validation** — the goal is to
prove that GitHub Codespaces is a viable, low-friction environment for running
quantized small language models (SLMs) on CPU with
[llama-cpp-python](https://github.com/abetlen/llama-cpp-python).

Dependencies are managed with [uv](https://docs.astral.sh/uv/) via
`pyproject.toml` / `uv.lock` — no `requirements.txt`.

## Quick start (GitHub Codespaces — recommended)

1. Click **Code → Codespaces → Create codespace on main**.
2. Wait for the container to build. `postCreateCommand` runs `uv sync`
   automatically, creating `.venv` with all dependencies.
3. Download a quantized model (one-time, ~1 GB):

   ```bash
   mkdir -p models
   curl -L -o models/qwen2.5-1.5b-instruct-q4_k_m.gguf \
     "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf"
   ```

4. Run the example:

   ```bash
   uv run python examples/01_local_inference.py \
     --model-path models/qwen2.5-1.5b-instruct-q4_k_m.gguf
   ```

## Local fallback

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
uv sync
uv run python examples/01_local_inference.py --model-path <path-to-gguf>
```

## Validation metrics

Fill in after running in Codespaces:

| Metric              | Value |
|----------------------|-------|
| Model size           | ~1 GB (Q4_K_M) |
| RAM usage            |       |
| CPU usage            |       |
| Load time            | 7.43s |
| First-token latency  |       |
| Total latency        | 6.09s |
| Tokens/sec           | 7.72  |
