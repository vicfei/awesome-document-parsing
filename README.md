# Awesome Document Parsing — a measured registry

> Document parsing sets the ceiling of RAG quality. This is **not another link list** — it is a registry of **measured results**: tools × file types × accuracy × speed × resource cost, from a RAG-ingestion perspective. Every entry links to a reproducible benchmark record.

**Why this repo exists**: the parsing space is on fire (PaddleOCR 92k⭐, docling 70k⭐, OpenDataLoader 30k⭐), yet public knowledge is either vendor benchmarks ([ParseBench](https://github.com/run-llama/ParseBench)), small single-dimension shootouts ([pdf-to-markdown-benchmark](https://github.com/pdfmarkdownapp/pdf-to-markdown-benchmark)), or static feature lists. What's missing — and what we seed here — is **community-measured data across file types with a shared methodology**.

## Contents

- [Tool matrix](#tool-matrix) — the landscape, last-surveyed 2026-11
- [Benchmark records](benchmarks/) — measured results by file type
  - [`pdf-academic/`](benchmarks/pdf-academic/) — two-column papers, tables, formulas
  - [`pdf-scanned/`](benchmarks/pdf-scanned/) — image-only scans (OCR path)
  - [`pdf-cjk/`](benchmarks/pdf-cjk/) — Chinese printed documents
  - [`perf/`](benchmarks/perf/) — throughput / VRAM / hardware scaling
- [Methodology](benchmarks/METHOD.md) — blind LLM-judge with position swap, VRAM sampling, timing conventions
- [Tool dossiers](tools/) — one page per tool: deployment forms, tiers, gotchas
- [Contribute your measurements](CONTRIBUTING.md)

## Community leaderboard

Open-source tools registered in this repo, ranked two ways. Refreshed by [`scripts/leaderboard.py`](scripts/leaderboard.py) (snapshots under [`snapshots/`](snapshots/)).

**By total stars** (as of 2026-11-02)

| # | Repo | Stars | Weekly gain* |
|---|---|---|---|
| 1 | [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) | 92,082 | — |
| 2 | [MinerU](https://github.com/opendatalab/MinerU) | 82,947 | — |
| 3 | [docling](https://github.com/docling-project/docling) | 69,970 | — |
| 4 | [Marker](https://github.com/datalab-to/marker) | 40,742 | — |
| 5 | [OpenDataLoader](https://github.com/opendataloader-project/opendataloader-pdf) | 30,139 | — |
| 6 | [unstructured](https://github.com/Unstructured-IO/unstructured) | 15,659 | — |
| 7 | [doctr](https://github.com/mindee/doctr) | 6,405 | — |
| 8 | [docstrange](https://github.com/NanoNets/docstrange) | 1,585 | — |
| 9 | [indra](https://github.com/datalab-to/indra) | 1,578 | — |
| 10 | [OpenOCR](https://github.com/Topdu/OpenOCR) | 1,491 | — |

**By weekly gain\*** — *appears from the second refresh (see note)*

| # | Repo | Weekly gain* | Stars |
|---|---|---|---|
| — | _run `scripts/leaderboard.py` after ≥7 days to populate_ | — | — |

\* **Why weekly gains need two refreshes**: GitHub has closed stargazer-timeline access to third-party tokens (REST `/stargazers` → 404, GraphQL `stargazers` edges → empty, `star+json` preview → removed), so "stars this week" cannot be queried directly. The script therefore snapshots totals and reports the **snapshot-diff normalized to 7 days** — run it weekly (or add it to a cron) and the second table fills in with real gains. First snapshot: 2026-11-02.

## Tool matrix

### Open-source parsing pipelines

| Tool | Focus | Formats | Deployment | License |
|---|---|---|---|---|
| [MinerU](https://github.com/opendatalab/MinerU) | PDF→MD/JSON, hybrid pipeline (layout+OCR+formula small models + 1.2B VLM), weights baked into offline image | PDF | CLI / API / self-host GPU or CPU | AGPL-3.0 |
| [docling](https://github.com/docling-project/docling) | "Documents ready for gen AI", broad format coverage | PDF/DOCX/PPTX/XLSX/HTML | lib / CLI | MIT |
| [OpenDataLoader](https://github.com/opendataloader-project/opendataloader-pdf) | AI-ready PDF parsing, speed-first | PDF | lib / CLI | Apache-2.0 |
| [Marker](https://github.com/datalab-to/marker) | PDF→MD, strong self-host story | PDF/EPUB | CLI / API | GPL-3.0(weights CC-BY) |
| [unstructured](https://github.com/Unstructured-IO/unstructured) | ETL for LLMs, partitioning across dozens of formats | many | lib / platform | Apache-2.0 |
| [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) | OCR toolkit, 100+ languages, layout analysis | images / PDF | lib / service | Apache-2.0 |
| [docstrange](https://github.com/NanoNets/docstrange) | Documents→MD/JSON/CSV/HTML | PDF/img/URL | lib | MIT |
| [doctr](https://github.com/mindee/doctr) | DL OCR, detection+recognition+layout | images / PDF | lib | Apache-2.0 |
| [OpenOCR](https://github.com/Topdu/OpenOCR) | General OCR research toolkit | images / PDF | lib | Apache-2.0 |
| [indra](https://github.com/datalab-to/indra) | 1M-param OCR on CPU, claims 15× tesseract | images | lib | GPL-3.0 |

### Commercial / API

| Service | Notes |
|---|---|
| LlamaParse | LlamaIndex's managed parser |
| Mistral OCR | API OCR; head-to-head vs MinerU in third-party scoring ([faun.dev](https://faun.dev/toolbox/mineru-vs-mistral-ocr)) |
| Mathpix | Formula-first extraction |
| Azure Document Intelligence | Enterprise DOCX/PDF/forms |
| LandingAI ade-cli | Agentic schema-shaped extraction |

### General-purpose VLMs as parsers (the "just ask a VLM" route)

Qwen-VL family, GPT-4o-class, Gemini-class models can transcribe page images end-to-end. **Our measured verdict** ([record](benchmarks/pdf-academic/2026-11-01_mineru41-vs-qwen35-08b.md)): on complex layouts a general 0.8B VLM loses 4/4 blind-judged rounds to a dedicated pipeline (missing sections, broken tables, truncated formulas, 4096-token output caps), while on simple single-page CJK prints it matches field-level accuracy. Route VLMs to "look and answer", not to document transcription.

## Headline numbers (from our records)

| Scenario | Tool | Result |
|---|---|---|
| 13-page academic PDF, cold CLI (RTX 4060 8GB) | MinerU 4.1.3 GPU | 115s wall (67s engine start + 23.8s infer = 0.55 page/s), VRAM peak 94.5% of 8GB |
| Same, warm API (model resident) | MinerU 4.1.3 GPU | 9s / 13 pages = **1.51 page/s**; resident ~6.2GB |
| 13-page academic PDF, CPU-only (i7-13650HX, 14C/20T) | MinerU 4.1.3 CPU | standard 5.95 s/page, basic 2.60 s/page |
| Page transcription, general VLM | Qwen3.5-0.8B bf16 | 4–9 s/page, 2/13 dense pages truncated at 4096 tokens |

Full records with methodology, raw outputs and judge transcripts under [`benchmarks/`](benchmarks/).

## Repository principles

1. **Measured over marketed** — every claim links to a record with environment, inputs and protocol.
2. **File-type first** — accuracy is not one number; a parser is scored per document archetype.
3. **Reproducible** — records carry prompts, versions, hardware, and judge settings.
4. **No vendor pay-to-play** — commercial tools welcome, but with the same protocol as open source.

License: CC-BY-4.0 for content. Each tool keeps its own license; this repo ships no tool code.
