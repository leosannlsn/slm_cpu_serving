# SLM CPU Serving — Workshop Repo

**Beyond ChatGPT: Real-Time AI Inference on Your Laptop**

This repo validates that GitHub Codespaces is a viable, low-friction
environment for running quantized small language models (SLMs) on CPU with
[llama-cpp-python](https://github.com/abetlen/llama-cpp-python), both for
direct local inference (**Phase 1**) and for OpenAI-compatible API serving
(**Phase 2**).

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

   Optionally, the preferred (larger) model instead (one-time, ~2 GB):

   ```bash
   mkdir -p models
   curl -L -o models/qwen2.5-3b-instruct-q4_k_m.gguf \
     "https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf"
   ```

4. Run the example:

   ```bash
   uv run python examples/01_local_inference.py \
     --model-path models/qwen2.5-1.5b-instruct-q4_k_m.gguf
   ```

   Or, with the 3B model:

   ```bash
   uv run python examples/01_local_inference.py \
     --model-path models/qwen2.5-3b-instruct-q4_k_m.gguf \
     --n-threads $(nproc)
   ```

## Local fallback

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
uv sync
uv run python examples/01_local_inference.py --model-path <path-to-gguf>
```

## Phase 1 validation metrics

Fallback model (Qwen2.5-1.5B-Instruct Q4_K_M, ~1 GB), validated in Codespaces:

| Metric              | Value |
|----------------------|-------|
| Model size           | ~1 GB (Q4_K_M) |
| RAM usage            | 1834.3 MB (peak) |
| CPU usage            | 165.0% (n_threads=2) |
| Load time            | 1.24s |
| First-token latency  | 1.93s |
| Total latency        | 6.39s |
| Tokens/sec           | 7.36  |

Preferred model (Qwen2.5-3B-Instruct Q4_K_M, ~2 GB), validated locally
(Windows, 2 threads):

| Metric              | Value |
|----------------------|-------|
| Model size           | ~2 GB (Q4_K_M) |
| RAM usage            | 3292.2 MB (peak) |
| CPU usage            | 245.1% (n_threads=2) |
| Load time            | 1.83s |
| First-token latency  | 0.68s |
| Total latency        | 5.78s |
| Tokens/sec           | 7.96  |

Preferred model (Qwen2.5-3B-Instruct Q4_K_M, ~2 GB), validated in Codespaces
(2 threads):

| Metric              | Value |
|----------------------|-------|
| Model size           | ~2 GB (Q4_K_M) |
| RAM usage            | 3464.2 MB (peak) |
| CPU usage            | 99.1% (n_threads=2) |
| First-token latency  | 2.90s |
| Total latency        | 13.71s |
| Tokens/sec           | 4.16  |

The 3B model roughly doubles RAM usage (~1.8 GB → ~3.3 GB peak) but fits
comfortably within the default Codespaces machine type (2-core/8GB), with
room to spare for a classroom setting.

## Phase 2: OpenAI-compatible API serving

See [examples/02_start_server.md](examples/02_start_server.md) to start a
local OpenAI-compatible server (`llama_cpp.server`), then run
[examples/03_api_client.py](examples/03_api_client.py) against it using the
`openai` SDK.

Validated locally (Windows, 2 threads, same 1.5B Q4_K_M model):

| Metric       | Value |
|--------------|-------|
| Total time   | 2.78s |
| Tokens       | 30    |
| Tokens/sec   | 10.80 |

Validated in Codespaces (same 1.5B Q4_K_M model):

| Metric       | Value |
|--------------|-------|
| Total time   | 7.21s |
| Tokens       | 48    |
| Tokens/sec   | 6.65  |

## Phase 3: Benchmarking exercise

See [examples/05_benchmark.md](examples/05_benchmark.md) to run
[examples/04_benchmark.py](examples/04_benchmark.py), which sweeps thread
counts, context sizes, and model files and writes the results to a CSV for
classroom discussion.

```bash
uv run python examples/04_benchmark.py \
  --model-path models/qwen2.5-1.5b-instruct-q4_k_m.gguf models/qwen2.5-3b-instruct-q4_k_m.gguf \
  --n-threads 1 2 \
  --n-ctx 512 2048 \
  --max-tokens 64 \
  --output benchmark_results.csv
```

