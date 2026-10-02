# Copilot Instructions - SLM Inference Workshop

## Purpose

You are assisting in the development of a university workshop repository called **Beyond ChatGPT: Real-Time AI Inference on Your Laptop**.

Your role is not to optimize for maximum model quality. Your role is to optimize for:

1. Reliability in live classroom settings.
2. Minimal attendee setup.
3. Reproducibility.
4. Low hardware requirements.
5. Educational value.

When forced to choose, prefer simplicity over sophistication.

---

## Workshop Constraints

### Infrastructure

- No Azure budget.
- No paid services.
- No GPU requirement.
- Prefer open-source tools.
- Must run on commodity laptops.

### Delivery Options

Primary:
- GitHub Codespaces

Fallback:
- Local Python environment
- VS Code
- Git
- Python 3.12+

Do not make Docker a mandatory dependency.

---

## Workshop Learning Outcomes

Participants should leave understanding:

- What inference is.
- Why SLMs exist.
- Quantization.
- Latency vs throughput.
- Context window impact.
- OpenAI-compatible serving.
- How local inference relates to enterprise AI platforms.

---

# Phase 1: Codespaces Validation

Current objective:

Build the smallest possible proof-of-concept to validate that Codespaces is viable.

Do NOT build the full workshop yet.

Success criteria:

- Codespace starts successfully.
- Python environment is available.
- llama.cpp can run.
- A quantized model loads.
- Inference works.
- Latency can be measured.

---

## Initial Repository Structure

Create only:

```text
.devcontainer/
README.md
requirements.txt
examples/
```

Avoid introducing additional files until a clear need exists.

---

## Minimal Devcontainer

Preferred starting point:

```json
{
  "image": "mcr.microsoft.com/devcontainers/python:3.12",
  "postCreateCommand": "pip install -r requirements.txt"
}
```

Keep the environment intentionally simple.

---

## Phase 1 Dependencies

Prefer:

```text
openai
llama-cpp-python
psutil
jupyter
```

Avoid adding frameworks unless they provide clear workshop value.

---

## Phase 1 Example

Create:

```text
examples/01_local_inference.py
```

Responsibilities:

- Load model path from environment variable or CLI argument.
- Run one prompt.
- Measure elapsed time.
- Print response.
- Print tokens/sec if available.

Focus on observability and benchmarking.

---

## Phase 1 Model Candidates

Preferred:

```text
Qwen2.5-3B-Instruct Q4_K_M
```

Fallback:

```text
Qwen2.5-1.5B-Instruct Q4_K_M
```

Avoid larger models during validation.

---

## Validation Metrics

Capture:

```text
Model size
RAM usage
CPU usage
Load time
First-token latency
Total latency
Tokens/sec
```

Record findings in README.

---

# Phase 2: Local API Serving

Once inference validation succeeds, expand.

Create:

```text
examples/02_start_server.md
examples/03_api_client.py
```

Goal:

Expose an OpenAI-compatible endpoint using llama-server.

Client code should use the OpenAI SDK.

Example pattern:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="dummy"
)
```

---

# Phase 3: Benchmarking Exercise

Create reusable benchmarking scripts.

Students should compare:

```text
Thread counts
Context sizes
Quantization levels
Model sizes
```

Outputs should be easy to discuss in a classroom.

CSV output is preferred.

---

# Phase 4: Full Workshop Material

Only after all validation is complete.

Target structure:

```text
.devcontainer/
README.md
requirements.txt
examples/
notebooks/
data/
assets/
```

---

## Planned Exercises

Exercise 1
- Local inference.

Exercise 2
- Compare quantizations.

Exercise 3
- Measure latency and throughput.

Exercise 4
- Serve model with llama-server.

Exercise 5
- Build a simple application against the endpoint.

---

## Educational Philosophy

Do not present llama.cpp as the objective.

Present it as a vehicle for teaching:

- inference engineering
- performance tradeoffs
- resource constraints
- deployment concepts

---

## Enterprise Context

Whenever examples or explanations are added, connect laptop experiments to real systems.

Conceptual progression:

```text
Laptop
  -> llama.cpp

Single Server
  -> vLLM

Managed Endpoint
  -> Azure ML / Vertex AI

Enterprise Platform
  -> Distributed Inference
```

Students should understand that the same engineering concepts scale from a laptop to production infrastructure.

---

## What To Avoid

Avoid:

- Docker-first designs.
- GPU-only examples.
- Complex orchestration.
- Multi-service architectures.
- Premature optimization.
- Long installation procedures.

The workshop should survive weak Wi-Fi, heterogeneous laptops, and limited student experience.
