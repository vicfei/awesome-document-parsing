# MinerU 4.1.3 hardware scaling — GPU vs CPU images

Archetype: performance · Date: 2026-11-01 · Protocol: [METHOD](../METHOD.md)

Same 13-page academic PDF through two official offline image forms.

## GPU form (`mineru:4.1.3-cu129`, vLLM 0.21 backend, Qwen2VL-1.2B VLM bf16)

Hardware: RTX 4060 Laptop 8GB (Ada, CC 8.9) — deliberately near the floor of supported GPUs.

| Metric | Value |
|---|---|
| Cold CLI wall time | 115s / 113s (two runs) = engine init 66.7s + inference 23.8s |
| Cold inference speed | 0.546 page/s |
| Warm API latency (model resident) | 9s / 13 pages = **1.51 page/s** |
| VRAM peak (1 Hz sampling) | 7738 MiB / 8188 MiB = **94.5%**, stock `gpu-memory-utilization=0.75`, zero OOM |
| Post-task resident (API form) | ~6.0–6.3 GB (model stays loaded — a serving behavior) |
| Model residency budget | weights 2.16 GB + KV cache 2.28 GB + CUDA graphs 0.25 GB, max_len 8192, ~24× concurrency headroom |

An 8GB card runs it with default settings but at the ceiling; the peak is vLLM budget + small-model pipeline + CUDA context stacked. On 96GB-class datacenter GPUs this workload sits below 10%.

## CPU form (`mineru:4.1.3-cpu`, ONNX small models + llama.cpp GGUF VLM, zero torch/vllm)

Hardware: i7-13650HX (14C/20T laptop CPU).

| Tier | Per page | 13-page wall |
|---|---|---|
| standard | **5.95 s/page** | 88.6s (77.3s inference + ~11s model load) |
| basic | **2.60 s/page** | 40.5s |

Reference baseline (2 vCPU / 3.6GB small VM, upstream measurement): standard 25.7 s/page, basic 8.5 s/page → the 14-core desktop-class CPU delivers **4.3× / 3.3×**.

## Reading for capacity planning

- CPU-only deployment of standard tier at ~6 s/page on a desktop-class core count is viable for batch ingestion (≈600 pages/hour/core-set); a 32–64 core server scales from there.
- GPU serving amortizes the 67s cold start only under residency — prefer the API/router form over per-file CLI spawns.
- Image size economics: GPU image 45.6GB (vLLM+CUDA structural weight) vs CPU image 5.7GB — the CPU form is the right default where a GPU is not already provisioned.
