# RAG Interview Prep

Interview prep material for the RAG portion of ML/AI engineering interviews: Q&A by pipeline stage, system-design scenarios, debugging exercises, and comparison cheat sheets.

## Contents

| File | What's in it |
|---|---|
| [qa-by-stage.md](qa-by-stage.md) | Interview questions + answers, organized by RAG pipeline stage: chunking, embeddings, indexing, retrieval, reranking, generation, evaluation |
| [system-design-scenarios.md](system-design-scenarios.md) | Whiteboard-style "design a RAG system for X" prompts with answer sketches |
| [debug-scenarios.md](debug-scenarios.md) | "Here's a broken RAG system, diagnose it" exercises |
| [cheatsheets.md](cheatsheets.md) | Quick comparison tables: chunking strategies, vector DBs, rerankers, distance metrics |

## How to use this

- Prepping for an interview: read `qa-by-stage.md` top to bottom, then test yourself on `debug-scenarios.md` without peeking at the diagnosis.
- Brushing up before a whiteboard round: skim `system-design-scenarios.md` and practice sketching the architecture out loud in under 5 minutes.
- Quick reference during study: `cheatsheets.md`.

Some examples reference implementations elsewhere in this repo ([`Docling-Qdrant-RAG`](../Docling-Qdrant-RAG), [`Agentic-Qdrant-RAG`](../Agentic-Qdrant-RAG)), worth having open side by side.

## Contributing

Found a question worth adding, or a better answer to one that's here? PRs welcome, see [CONTRIBUTING.md](../CONTRIBUTING.md).
