# SLM Inference Workshop - Planning Context

## Working Title

**Beyond ChatGPT: Real-Time AI Inference on Your Laptop**

Alternative title:

**Inference Engineering for Small Language Models**

---

## Workshop Goals

Participants will:

- Run a Small Language Model (SLM) locally on CPU.
- Understand inference fundamentals.
- Learn what quantization is and why it matters.
- Measure latency, throughput, memory, and CPU usage.
- Expose a local OpenAI-compatible API.
- Build a simple application against that API.
- Understand how laptop inference concepts translate to enterprise AI serving.

---

## Target Audience

- University CS students
- Software engineers
- AI enthusiasts

No prior AI experience required.

---

## Key Message

This is NOT a llama.cpp tutorial.

This is an introduction to inference engineering using llama.cpp as the vehicle.

Core question:

> How much useful AI can we run using only commodity CPUs and a few GB of RAM?

---

## Tentative Agenda (2 Hours)

### Part 1 - The Reality Check (15 min)

Topics:

- What is model inference?
- Why Small Language Models exist
- Latency vs throughput
- Quantization basics

Exercise:

Students estimate hardware requirements for different model sizes.

---

### Part 2 - First Local Inference (20 min)

Run a quantized model locally using llama.cpp.

Example:

```bash
llama-cli \
  -m qwen.gguf \
  -p "Explain the TCP handshake"
```

Learning:

- No cloud
- No API key
- No GPU required

---

### Part 3 - Performance Benchmarking (25 min)

Measure:

- First-token latency
- Tokens/sec
- RAM usage
- CPU usage

Compare:

```bash
-t 2
-t 4
-t 8
```

And different quantization levels.

Learning:

- Speed vs quality tradeoffs
- Quantization tradeoffs
- Resource constraints

---

### Part 4 - Build an API Endpoint (20 min)

Run:

```bash
llama-server -m qwen.gguf
```

Consume via OpenAI SDK:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="dummy"
)
```

Learning:

- OpenAI-compatible APIs
- Serving concepts
- Foundation for enterprise inference platforms

---

### Part 5 - Mini Challenge (30 min)

Constraint:

- CPU only
- Response < 3 seconds

Tasks:

- Summarization
- Classification
- Information extraction

Students optimize:

- Threads
- Quantization
- Context size

---

## Enterprise Connection Slide

End workshop with:

```text
Laptop
  ↓
llama.cpp

Single Server
  ↓
vLLM

Managed Endpoint
  ↓
Azure ML

Enterprise Platform
  ↓
Distributed Inference
```

Objective:

Show how the same concepts scale to production environments.

---

## Model Selection

Primary:

```text
Qwen2.5-3B-Instruct
Q4_K_M GGUF
```

Fallback:

```text
Qwen2.5-1.5B-Instruct
Q4_K_M GGUF
```

Reasoning:

- Good instruction following
- Small enough for CPU inference
- Suitable for commodity hardware

---

## Codespaces Strategy

### Recommended Experience

GitHub Codespaces.

Benefits:

- No local installation
- Consistent environment
- Works from browser
- Easier classroom support

Participant requirements:

- GitHub account
- Web browser
- Internet connection

Important:

Every participant uses their own Codespace.
The workshop organizer does not need to provide shared compute.

---

## Local Fallback Strategy

For participants without GitHub accounts.

Required software:

- VS Code
- Python 3.12+
- Git

Workshop package:

```text
workshop.zip
├── llama.cpp binaries
├── model.gguf
├── requirements.txt
├── examples
└── notebooks
```

No Docker required.

---

## Hardware Requirements

### Minimum

```text
4 CPU cores
8 GB RAM
10 GB free disk
```

### Recommended

```text
4+ CPU cores
16 GB RAM
15 GB free disk
```

GPU not required.

---

## Docker Position

Recommendation:

Do not require Docker.

Reason:

- Additional setup burden
- Windows/WSL issues
- Not relevant to workshop learning objectives

Can be offered as an advanced optional path.

---

## Repository Structure Proposal

```text
slm-workshop/
├── .devcontainer/
│   └── devcontainer.json
├── notebooks/
├── examples/
├── models/
├── requirements.txt
└── README.md
```

---

## Minimal Dev Container

```json
{
  "image": "mcr.microsoft.com/devcontainers/python:3.12",
  "postCreateCommand": "pip install -r requirements.txt"
}
```

---

## Validation Tasks Before Event

### Codespaces

Validate using a standard Codespace:

- Environment startup
- Package installation
- Model download
- llama.cpp execution
- llama-server execution
- OpenAI SDK integration

Measure:

- First-token latency
- Tokens/sec
- RAM usage

---

## Success Criteria

### Technical

Cold start to working inference:

```text
< 10 minutes
```

Response latency:

```text
< 5 seconds
```

Target throughput:

```text
> 10 tokens/sec
```

### Learning

Participants leave with:

- A working local LLM
- A local inference API
- Performance benchmarks
- Understanding of inference tradeoffs

---

## Information for Organizers

### Primary Path

- GitHub Codespaces
- Browser only
- GitHub account required

### Fallback Path

- VS Code
- Python 3.12+
- Git
- Prepackaged ZIP

### Bring

- Laptop
- Internet access

### No Requirements

- No GPU
- No Azure subscription
- No paid services
- No cloud budget
