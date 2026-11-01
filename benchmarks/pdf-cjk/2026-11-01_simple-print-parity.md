# Simple Chinese print — where a small VLM matches the pipeline

Archetype: `pdf-cjk` · Date: 2026-11-01 · Protocol: [METHOD](../METHOD.md)

## Setup

Single-page Chinese certificate/form (headline, labeled fields, one photo). Both systems transcribe the page; comparison done **locally by exact field matching** — PII-bearing pages never leave the machine (see METHOD §2.5).

## Result: parity

| Check | MinerU 4.1.3 GPU | Qwen3.5-0.8B |
|---|---|---|
| Headline + form labels present | ✓ | ✓ |
| Two 18-digit ID numbers extracted | complete, exact | complete, exact, identical |
| Typed field values | ✓ | ✓ |

## Reading

On simple, single-column, large-type CJK prints, the difficulty floor is low enough that a general 0.8B VLM is field-level accurate. The pipeline's advantage in the academic/scanned records comes from layout complexity, not from the language itself. **Do not extrapolate "CJK parity" to complex CJK documents** (tables, multi-column) — those need their own records; a public CJK benchmark document contribution is welcome (see CONTRIBUTING).

The source sample contains personal ID data and is intentionally not shipped; use any local equivalent form and the same field-matching protocol to reproduce.
