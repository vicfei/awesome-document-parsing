# Benchmark methodology

Shared protocol for all records in this repo. A record is only comparable to another if both followed this page.

## 1. Document archetypes

Accuracy depends on the document, not just the tool. Every record declares its archetype:

| Archetype | Definition | Typical failure modes |
|---|---|---|
| `pdf-academic` | Two-column papers, tables, inline/display math, figures | column-order interleaving, table cell collapse, formula mangle |
| `pdf-scanned` | Image-only pages (no text layer) | OCR errors, dropped regions |
| `pdf-cjk` | Chinese printed matter, certificates, forms | CJK recognition, field alignment |
| `office/html` | (reserved) DOCX/XLSX/PPTX/HTML | structure fidelity |

## 2. Blind LLM judge with position swap

Pairwise comparison (system X vs Y) is judged by an LLM **without knowing which system is which**.

1. Both outputs are normalized: stripped of embedded base64 images (replaced by `[img]`), code fences removed. Embedded images are excluded from quality judging.
2. Judge model: a frontier API model in **no-reasoning mode, temperature 0** (our records: `deepseek-v4-flash`, thinking disabled). Record the model in the record file.
3. Judge rates four dimensions — `text` (accuracy/hallucination), `table`, `formula`, `order` (reading order & layout) — plus `overall`, each as X/Y/tie with one line of evidence.
4. **Position swap**: run the judge twice, X/Y exchanged. A verdict is accepted only if the winner stays the same and the cited defects move with the system (defect side must swap). This kills position bias.
5. Numeric fields (IDs, amounts) on simple documents are compared **locally with exact string matching** — do not send PII-bearing content to any API.

## 3. Timing conventions

Report all three when possible, they answer different questions:

- **Cold wall time**: process start → output written (includes engine/model load).
- **Inference time**: model pipeline only, as reported by the tool (e.g. MinerU logs `cost=…s, speed=N page/s`).
- **Warm service latency**: for API/serve forms, request → result on a model-resident server (first request excluded).

## 4. Resource sampling

- **VRAM**: poll `nvidia-smi --query-gpu=memory.used` at 1 Hz for the whole run; report **peak** and **post-task resident** (a resident model after task completion is a serving behavior worth recording).
- Note allocator settings that dominate the number (e.g. vLLM `gpu-memory-utilization`).
- CPU runs: report CPU model, core/thread count, and whether the tool saturates them.

## 5. Environment disclosure

Every record states: CPU, GPU (if any), RAM class, OS class, tool version + backend tier, model precision (bf16/GGUF/quant). Consumer hardware names are fine; do not include employer-internal identifiers.

## 6. Gotchas we hit (so you don't have to)

- **Docker images without `nvcc`**: flashinfer JIT sampling kernels fail at engine start (`nvcc: not found`). Workaround: `VLLM_USE_FLASHINFER_SAMPLER=0`.
- **VLM transcription output caps**: a 4096-token page cap truncates figure-dense pages — record truncations (`finish_reason=length`) as first-class results.
- **LLM judges emit fragile JSON**: prefer line-based verdict formats (`dim|winner|evidence`) over JSON to avoid escaping failures.
- **Embedded-image markdown inflates 10×**: strip before any text comparison or judging.
- **Dense-page speed ≠ average-page speed**: report per-page distribution or call out dense pages explicitly.
