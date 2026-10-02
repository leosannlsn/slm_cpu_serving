# Phase 2: Start an OpenAI-compatible server

`llama-cpp-python` ships a built-in server (`llama_cpp.server`) that exposes an
OpenAI-compatible HTTP API on top of the same GGUF model used in
[01_local_inference.py](01_local_inference.py).

## Start the server

```bash
uv run python -m llama_cpp.server \
  --model models/qwen2.5-1.5b-instruct-q4_k_m.gguf \
  --n_ctx 2048 \
  --n_threads 2 \
  --port 8080
```

Leave this running in its own terminal. In Codespaces, VS Code will
automatically forward port 8080 — open the **Ports** tab to confirm it's
listed, and set its visibility to **Private** (default) unless you intend to
share it.

## Verify it's up

```bash
curl http://127.0.0.1:8080/v1/models
```

This should return a JSON list containing the loaded model.

## Run the client

With the server still running, in a second terminal:

```bash
uv run python examples/03_api_client.py
```

This uses the `openai` SDK pointed at `http://127.0.0.1:8080/v1` to send a
chat completion request, same as talking to the real OpenAI API.
