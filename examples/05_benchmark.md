# Phase 3: Benchmarking exercise

[examples/04_benchmark.py](04_benchmark.py) sweeps combinations of thread
counts, context sizes, and model files, writing one CSV row per combination.
Students can discuss trade-offs by sweeping:

- **Thread counts** — `--n-threads`
- **Context sizes** — `--n-ctx`
- **Quantization levels / model sizes** — pass multiple `--model-path` values
  (e.g. a Q4_K_M and a Q5_K_M/Q8_0 GGUF, or the 1.5B and 3B models)

## Run a sweep

```bash
uv run python examples/04_benchmark.py \
  --model-path models/qwen2.5-1.5b-instruct-q4_k_m.gguf models/qwen2.5-3b-instruct-q4_k_m.gguf \
  --n-threads 1 2 4 \
  --n-ctx 512 2048 \
  --max-tokens 64 \
  --output benchmark_results.csv
```

Each combination runs once by default; use `--repeats 3` to average out
noise before discussing results as a class.

## Output

A CSV with columns: `model, n_threads, n_ctx, load_time_s,
first_token_latency_s, total_time_s, tokens, tokens_per_sec, peak_ram_mb,
cpu_percent` — easy to open in a spreadsheet or plot during the workshop.
