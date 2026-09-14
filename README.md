# Writing Samples — Ben Goddard

Documentation engineering and information architecture work, 2020 to 2026.

I build the systems that produce documentation. Some of what follows is writing.
More of it is the structure, tooling, and process underneath the writing, which is
the part I care about and the part I get hired for.

**Every sample states plainly whether I wrote it, directed it, or designed the
system that produced it.** Those are different claims and they should not be blurred.

---

## Start here

Five samples, ranked by what they prove:

1. [Building a documentation system, not writing documentation](systems-and-tooling/documentation-system-forage.md) — a 20-stage AI-assisted pipeline, a full Diátaxis restructure, and a documentation MCP server. The site is public and you can check every claim against it.
2. [Documentation work intake automation](systems-and-tooling/work-intake-automation.md) — a 23-step automation that turned an untracked request queue into routed, acknowledged work.
3. [Scoring documentation pages for freshness](information-architecture/page-freshness-scoring.md) — content lifecycle triage, so maintenance goes where it matters.
4. [Consolidating two intake forms into one](information-architecture/intake-form-consolidation.md) — field-by-field analysis with a recorded reason for every field kept, merged, or cut.
5. [Documentation tooling UX research](information-architecture/documentation-tooling-ux-research.md) — survey research on an internal wiki, with a flaw in its own measurement scale named in the report.

---

## Everything, by type

### Systems and tooling

| Sample | What it shows | My role |
|---|---|---|
| [Documentation system at Forage](systems-and-tooling/documentation-system-forage.md) | AI-assisted pipeline, Diátaxis restructure, llms.txt, MCP server | Directed and built the system |
| [Work intake automation](systems-and-tooling/work-intake-automation.md) | 23-step request-to-ticket automation | Designed and built |

### Information architecture

| Sample | What it shows | My role |
|---|---|---|
| [Documentation tooling UX research](information-architecture/documentation-tooling-ux-research.md) | Survey design, findability analysis, structural recommendations | Wrote |
| [Intake form consolidation](information-architecture/intake-form-consolidation.md) | Content modeling, field-level reasoning | Analyzed and designed |
| [Page freshness scoring](information-architecture/page-freshness-scoring.md) | Content lifecycle triage system | Wrote and built |
| [Documentation lifecycle model](information-architecture/documentation-lifecycle-model.md) | Process model with stage ownership | Built |

### API reference

Published help center documentation. I wrote these.

| Sample | What it shows |
|---|---|
| [Suspend or unsuspend a member](api-reference/suspend-and-unsuspend-a-member.md) | Technical depth, user-facing and backend behavior together |
| [Get company members](api-reference/get-company-members.md) | Parameter tables and worked examples |
| [Audit log examples](api-reference/audit-log-examples.md) | Runnable examples, pagination |

### Style guide

| Sample | What it shows |
|---|---|
| [Formatting keyboard shortcuts](style-guide/formatting-keyboard-shortcuts.md) | Rule-writing that survives many writers, in a deliberately playful house voice |
| [Using graphics in documentation](assets/style-guide-using-graphics.pdf) | Screenshot conventions and accessibility, kept as a PDF because the images are the argument |

---

## On format

Some of these are Markdown and some are not, on purpose.

Where the words are the work, the sample is Markdown. Documentation belongs in
source form: it diffs, it reviews, it ships from a repo.

Where the layout or the diagram carries the meaning, the original is kept. A style
guide about using graphics with no graphics in it is not a style guide. Diagrams
that were originally large collaborative canvases have been rebuilt as Mermaid, so
they are readable as source and render in the browser rather than being a picture
of a decision.

Original source files are in [`assets/`](assets/).

---

## Related

**[context-engineering-toolkit](https://github.com/darthrootbeer/context-engineering-toolkit)** — the working tools: a documentation pipeline, style guides, and the architecture patterns behind them. That repo is the system. This one is the output and the reasoning.

---

## A note on redaction

Former employers appear here by name where the work is already public. Where it was
internal, colleague names, customer identities, internal channels, and product names
have been removed. The reasoning and structure are unchanged.
