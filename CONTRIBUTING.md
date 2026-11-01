# Contributing measurements

We want your numbers, not your opinions — bring a record.

## Record template

Create `benchmarks/<archetype>/YYYY-MM-DD_<tools>.md` containing:

1. **Archetype** — one of `pdf-academic / pdf-scanned / pdf-cjk / office-html / perf`, or propose a new one with a failure-mode table.
2. **Contestants & form** — exact tool versions, tiers/backends, precision, deployment form (CLI/API/serve).
3. **Environment** — CPU, GPU, RAM class, OS class. Consumer hardware names are fine; **no employer-internal identifiers** (hostnames, internal IPs, internal paths, internal service names).
4. **Protocol** — follow [METHOD](benchmarks/METHOD.md); state deviations explicitly.
5. **Results** — per-dimension verdicts with evidence lines; timing in the three conventions (cold wall / inference / warm service); VRAM peak + resident.
6. **Reproduction** — public sample (link or upstream repo path), prompts, judge model + settings.

## Hard rules

- **No PII in samples or transcripts.** Certificates/IDs/forms with real personal data stay local; report field-matching results computed locally. Never paste ID numbers into issues, records, or judge APIs.
- **Blind + swapped judging** for any LLM-judged claim; include the defect-side-swap validation result.
- **Truncations are results**: report `finish_reason=length` events, don't silently rerun with bigger caps.
- Public documents only, or a local-equivalent description precise enough to reproduce.

## Tool matrix additions

One row in the README matrix + (encouraged) a dossier page under `tools/` with deployment forms and gotchas. Commercial tools welcome under the same protocol.

## What we're explicitly looking for

- Complex CJK benchmarks (tables, multi-column) — our CJK record is parity-on-simple-print only.
- Office formats (DOCX/XLSX/PPTX) records — the matrix lists capability, we have no measured record yet.
- Long-document behavior (>50 pages): ordering drift, memory growth, mid-document degradation.
- Serving concurrency curves, not just single-stream latency.
