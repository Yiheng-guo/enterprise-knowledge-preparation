---
name: open-knowledge-format
description: Use when creating, reviewing, or exporting Open Knowledge Format (OKF) files, OKF-compatible Markdown, knowledge bundles, run indexes, research reports, source-linked summaries, or files named index.md, summary.md, or ai_summary.md.
compatibility: opencode
metadata:
  audience: researchers
  category: knowledge-management
  workflow: evidence-packaging
---

# Open Knowledge Format

Use this skill when the user asks for Open Knowledge Format, OKF, knowledge bundles, research run folders, source-linked Markdown reports, structured summaries, or machine-readable Markdown for LLM follow-up.

## Purpose

OKF packages research so both humans and AI systems can inspect it without losing provenance. A good OKF document is:

- Structured enough to parse.
- Readable enough to review manually.
- Source-linked wherever claims depend on evidence.
- Deterministic where possible, especially for generated pipeline exports.
- Small enough that another agent or LLM can use it as context.

## Canonical Definition

Use the [official Open Knowledge Format specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) as the normative source. It currently specifies OKF v0.2. When this skill's workflow conventions differ from the specification, label them as local conventions and follow the specification for conformance questions.

## When To Use

Load this skill for tasks such as:

- Creating `index.md`, `summary.md`, `ai_summary.md`, or similar files for a run folder.
- Converting CSV, JSON, Excel, database rows, or scrape results into Markdown knowledge bundles.
- Reviewing whether a research export has enough provenance and structure.
- Designing schemas for evidence packs, prospecting reports, market maps, vendor research, or account intelligence.
- Writing deterministic summaries meant to be pasted into another LLM, CRM, or research notebook.

Do not use this skill for normal prose unless the output is meant to become structured knowledge.

## Frontmatter

Every OKF Markdown file should start with YAML frontmatter:

```yaml
---
type: research_report
title: Descriptive Title
description: One sentence explaining what this document contains.
tags: [tag-one, tag-two]
timestamp: 2026-08-07T00:00:00+00:00
---
```

The specification requires only:

- `type`: A non-empty concept type.

Recommended fields include:

- `title`: Human-readable title.
- `description`: One sentence describing the content and scope.
- `resource`: Canonical URI for the underlying asset when one exists.
- `tags`: Short lowercase tags in a YAML list.
- `generated` and `verified`: Provenance and trust metadata when applicable.
- `status` and `stale_after`: Lifecycle metadata when applicable.
- `sources`: Materials from which the concept was derived.

For OKF v0.2, prefer `generated.at` for the last meaningful content change. Treat `timestamp` as a legacy or local compatibility field unless a workflow explicitly targets v0.1.

Useful `type` values:

- `knowledge_bundle_index`
- `research_report`
- `research_synthesis`
- `evidence_table`
- `source_inventory`
- `decision_record`
- `workflow_map`
- `account_intelligence`
- `signal_dictionary`

## Bundle Structure

For a folder-level OKF bundle, prefer this layout:

```text
run-or-topic-folder/
  index.md
  summary.md
  ai_summary.md
  sources.csv
  evidence.csv
  artifacts...
```

`index.md` should contain:

- Bundle purpose.
- Contents with relative links.
- Counts or coverage notes.
- Generation timestamp.
- Any major caveats.

`summary.md` should contain:

- Main findings.
- Evidence tables or source-linked excerpts.
- Methodology notes.
- Caveats and open questions.

`ai_summary.md` should contain:

- Concise deterministic synthesis.
- Key facts with source pointers.
- Recommended follow-up questions.
- No unsupported claims.

## Evidence Rules

Use evidence rows whenever a claim can be traced to a source.

Minimum evidence fields:

- `source`: URL, file path, database table, or artifact name.
- `claim`: The factual assertion being supported.
- `excerpt`: The smallest useful quoted or paraphrased span.
- `confidence`: `high`, `medium`, or `low`.
- `observed_at`: ISO timestamp or date.

For prospecting or account research, add:

- `company` or `domain`.
- `signal`.
- `evidence_type`, such as `job_post`, `homepage`, `platform_fingerprint`, `search_result`, or `manual_review`.
- `source_url` when available.

## Writing Rules

- Prefer plain Markdown tables for compact evidence.
- Keep headings stable and predictable.
- Use relative links inside a bundle.
- Include counts when summarizing tables.
- Separate findings from interpretation.
- Mark uncertain claims explicitly.
- Do not invent provenance. If a source is missing, write `source unavailable` or omit the claim.
- Avoid hidden reasoning. State the observable basis for each recommendation.

## Markdown Template

Use this for a single OKF report:

```markdown
---
type: research_report
title: <Title>
description: <One sentence description.>
tags: [okf, research]
timestamp: <ISO 8601 timestamp>
---

# <Title>

## Scope

<What this artifact covers and what it does not cover.>

## Counts

- sources: <n>
- evidence_rows: <n>
- entities: <n>

## Findings

| Finding | Evidence | Source | Confidence |
|---|---|---|---|
| <finding> | <excerpt or basis> | <link or path> | <high/medium/low> |

## Interpretation

<What the findings suggest. Keep this separate from observed facts.>

## Caveats

- <Known limitation or missing source.>

## Files

- [<artifact>](<relative-path>)
```

## AI Summary Template

Use this for context meant to be pasted into another model:

```markdown
---
type: research_synthesis
title: AI Summary
description: Concise source-linked synthesis for LLM follow-up.
tags: [okf, synthesis]
timestamp: <ISO 8601 timestamp>
---

# AI Summary

## What This Contains

<One short paragraph describing the dataset or run.>

## Strongest Facts

- <fact> Source: <relative link, URL, or row identifier>.

## Patterns

- <pattern with count or representative evidence>.

## Open Questions

- <question that needs more data or human review>.

## Use This Context To

- <safe downstream task>.
```

## Review Checklist

Before shipping an OKF artifact, check:

- Frontmatter exists and uses stable field names.
- `type`, `title`, `description`, `tags`, and `timestamp` are present.
- Every major factual claim has a source, excerpt, or table row.
- Relative links work from the bundle folder.
- Counts match the referenced tables or files.
- Interpretation is separated from evidence.
- Caveats are documented.
- The output is deterministic if generated by a pipeline.

## Marketing Pipeline Convention

In the `marketing-pipeline` repo, current OKF-compatible exports use:

- `index.md` with `type: knowledge_bundle_index`.
- `summary.md` with `type: research_report`.
- `ai_summary.md` with `type: research_synthesis`.
- CSV files for accounts, jobs, job signals, and platform signals.

When extending that repo, preserve this convention unless the user asks for a schema change.
