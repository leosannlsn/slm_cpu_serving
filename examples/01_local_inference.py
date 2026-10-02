"""Phase 1 validation: load a GGUF model with llama-cpp-python and run one prompt."""

import argparse
import os
import sys
import time

from llama_cpp import Llama

DEFAULT_PROMPT = "Explain what a small language model is in two sentences."


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run one inference pass against a local GGUF model."
    )
    parser.add_argument(
        "--model-path",
        default=os.environ.get("MODEL_PATH"),
        help="Path to a GGUF model file. Defaults to the MODEL_PATH environment variable.",
    )
    parser.add_argument(
        "--prompt", default=DEFAULT_PROMPT, help="Prompt to send to the model."
    )
    parser.add_argument(
        "--max-tokens", type=int, default=128, help="Maximum tokens to generate."
    )
    parser.add_argument(
        "--n-threads", type=int, default=os.cpu_count(), help="CPU threads to use."
    )
    parser.add_argument("--n-ctx", type=int, default=2048, help="Context window size.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not args.model_path:
        print(
            "Error: no model path provided. Set MODEL_PATH or pass --model-path.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Loading model: {args.model_path}")
    load_start = time.perf_counter()
    llm = Llama(
        model_path=args.model_path,
        n_ctx=args.n_ctx,
        n_threads=args.n_threads,
        verbose=False,
    )
    load_elapsed = time.perf_counter() - load_start
    print(f"Model loaded in {load_elapsed:.2f}s")

    print(f"Prompt: {args.prompt!r}")
    infer_start = time.perf_counter()
    result = llm.create_chat_completion(
        messages=[{"role": "user", "content": args.prompt}],
        max_tokens=args.max_tokens,
    )
    infer_elapsed = time.perf_counter() - infer_start

    response = result["choices"][0]["message"]["content"]
    usage = result.get("usage", {})
    completion_tokens = usage.get("completion_tokens")

    print("\n--- Response ---")
    print(response)
    print("\n--- Metrics ---")
    print(f"Load time:    {load_elapsed:.2f}s")
    print(f"Total time:   {infer_elapsed:.2f}s")
    if completion_tokens:
        print(f"Tokens:       {completion_tokens}")
        print(f"Tokens/sec:   {completion_tokens / infer_elapsed:.2f}")
    else:
        print("Tokens/sec:   unavailable (no usage data returned)")


if __name__ == "__main__":
    main()
