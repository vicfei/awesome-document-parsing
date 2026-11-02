# Tool dossier: MinerU

[opendatalab/MinerU](https://github.com/opendatalab/MinerU) · measured at **4.1.3** (2026-11) · AGPL-3.0

## Forms

| Form | Notes |
|---|---|
| CLI `mineru-kit parse` | one-shot; pays full engine cold start (~67s GPU) per invocation |
| API `api-server` | async task API (`POST /v1/tasks` → upload → poll → fetch ZIP of md+json+images); model stays resident ~6GB after first task |
| `vlm-server` / `router` / `webui` | compose profiles shipped in-repo |

Tiers: `flash / basic / standard / advanced`. Quality/speed trade per tier; `standard` is the default.

## Offline images (weights baked in, `MINERU_MODEL_SOURCE=local` in entrypoint)

| Image | Stack | Size | Use |
|---|---|---|---|
| GPU cu129 | vLLM 0.21 + torch, VLM bf16 | 45.6GB | throughput serving |
| CPU | ONNX small models + llama.cpp GGUF VLM, zero torch/vllm | 5.67GB | CPU-only boxes |

Deploy note: the shipped `compose.yaml` references `mineru:4` — tag your loaded image to the reference name (`docker tag mineru:4.1.3-cu129 mineru:4`) rather than editing compose.

## Measured behavior

See [perf record](../benchmarks/perf/2026-11-01_mineru41-hardware.md) and [academic record](../benchmarks/pdf-academic/2026-11-01_mineru41-vs-qwen35-08b.md). Headlines: 1.51 page/s warm on a laptop GPU at 94.5% of 8GB VRAM; 5.95 s/page standard tier on a 14C/20T CPU.

## Version drift observations (2.2.x → 4.1.3, from enterprise deployments)

| Dimension | Impact of the gap |
|---|---|
| Plain text extraction | small |
| Tables / formulas | large (VLM backend generation-over-generation gains) |
| OCR / scans | large (3.4-line OCR engine change, upstream +11% claim) |
| API contract | breaking across majors: 2.x single `/file_parse` endpoint vs 4.x async task API (`files[].bytes` required when no URL) — integration rework, not a drop-in upgrade |

VLM-tier activation checklist (silent gaps are common): (1) engine package actually in the image (`backend=engine` errors "not installed" = image missing pkg); (2) client mode has a `server_url` channel; (3) weights in the same container/pod — a co-located inference container that nothing wires to is the classic silent failure; (4) **resource-side cross-check** to prove whether a "running" inference container actually serves: compare GPU-Util vs resident VRAM, and the **detokenizer process's cumulative CPU time** — a scheduler at 100% CPU (busy-wait) with a detokenizer that has consumed ~2 minutes over 8 months is a service that has never answered a single request, while holding a full GPU's memory ([measured case](../benchmarks/perf/2026-11-01_mineru41-hardware.md): one H20 96GB held for months at zero traffic; the wiring gap in (2) was the cause).

## Gotchas

- API `POST /v1/tasks` rejects file entries without `bytes` when no `url` given (pydantic).
- CLI inside docker: sample files must be mounted into the container path you pass.
- 8GB GPUs: stock `gpu-memory-utilization=0.75` runs but at 94.5% ceiling; headroom lives in lowering it or trimming tiers.
- First start after version bump may log extended chown (entrypoint data-dir fix) — waiting, not hanging.
