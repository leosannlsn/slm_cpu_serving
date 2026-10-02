"""Phase 1 validation: load a GGUF model with llama-cpp-python and run one prompt."""

import argparse
import os
import sys
import threading
import time

import psutil
from llama_cpp import Llama

DEFAULT_PROMPT = "Explain what a small language model is in two sentences."


class PeakMemorySampler:
    """Background thread that tracks peak RSS (bytes) for the current process."""

    def __init__(self, process: psutil.Process, interval: float = 0.1) -> None:
        self._process = process
        self._interval = interval
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self.peak_rss = process.memory_info().rss

    def _run(self) -> None:
        while not self._stop.is_set():
            self.peak_rss = max(self.peak_rss, self._process.memory_info().rss)
            self._stop.wait(self._interval)

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        self._thread.join()


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

    process = psutil.Process(os.getpid())
    process.cpu_percent(
        interval=None
    )  # prime the counter; first call always returns 0.0

    mem_sampler = PeakMemorySampler(process)
    mem_sampler.start()

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
    first_token_elapsed = None
    chunks = []
    for chunk in llm.create_chat_completion(
        messages=[{"role": "user", "content": args.prompt}],
        max_tokens=args.max_tokens,
        stream=True,
    ):
        delta = chunk["choices"][0]["delta"].get("content")
        if delta:
            if first_token_elapsed is None:
                first_token_elapsed = time.perf_counter() - infer_start
            chunks.append(delta)
    infer_elapsed = time.perf_counter() - infer_start

    mem_sampler.stop()
    cpu_percent = process.cpu_percent(interval=None)

    response = "".join(chunks)
    completion_tokens = len(llm.tokenize(response.encode("utf-8"), add_bos=False))

    print("\n--- Response ---")
    print(response)
    print("\n--- Metrics ---")
    print(f"Load time:           {load_elapsed:.2f}s")
    print(f"Total time:          {infer_elapsed:.2f}s")
    if first_token_elapsed is not None:
        print(f"First-token latency: {first_token_elapsed:.2f}s")
    if completion_tokens:
        print(f"Tokens:              {completion_tokens}")
        print(f"Tokens/sec:          {completion_tokens / infer_elapsed:.2f}")
    else:
        print("Tokens/sec:          unavailable (no tokens generated)")
    print(f"Peak RAM:            {mem_sampler.peak_rss / (1024**2):.1f} MB")
    print(f"CPU usage:           {cpu_percent:.1f}% (n_threads={args.n_threads})")


if __name__ == "__main__":
    main()
