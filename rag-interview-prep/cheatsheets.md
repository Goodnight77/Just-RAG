# RAG Cheat Sheets

Quick comparison tables for study and quick reference during prep.

---

## Chunking Strategies

| Strategy | How it works | Best for | Watch out for |
|---|---|---|---|
| Fixed-size | Split every N tokens, with overlap | Uniform prose, quick baseline | Splits mid-sentence, mid-table, mid-code-block |
| Recursive character | Split on paragraph → sentence → word, in priority order, to fit size | General-purpose text, better than pure fixed-size | Still ignores document structure |
| Semantic | Split at embedding-similarity breakpoints | Long-form narrative content where topic shifts matter | Slower to compute, unpredictable chunk sizes |
| Structural (headers/sections) | Split on markdown headers, HTML tags, or document layout | Docs with clear structure (manuals, wikis, contracts) | Needs structure to exist and be parsed correctly |
| AST-aware (code) | Split on function/class boundaries | Source code | Requires a language-specific parser |
| Parent-document / hierarchical | Embed small chunks, retrieve, then return the larger parent chunk/section | Precise retrieval without losing surrounding context | Extra bookkeeping to map child chunks to parents |

---

## Vector Database Comparison

| Database | Deployment | Filtering | Notes |
|---|---|---|---|
| Qdrant | Self-hosted or managed | Filtered HNSW (filter pushed into graph traversal) | Strong on payload filtering + hybrid search |
| Weaviate | Self-hosted or managed | Pre/post filtering, GraphQL API | Built-in modules for hybrid search, generative search |
| Pinecone | Managed only | Metadata filtering | Fully managed, less infra control |
| Milvus | Self-hosted or managed | Metadata filtering | Strong at very large scale, more ops overhead |
| pgvector | Postgres extension | Full SQL filtering (joins, transactions) | Best when you already run Postgres and don't need extreme scale |
| FAISS | Library, not a database | None built-in | No persistence/filtering/metadata out of the box; you build that layer yourself |

---

## Reranker Comparison

| Type | Mechanism | Latency | Precision |
|---|---|---|---|
| Cross-encoder (e.g. BGE-reranker, Cohere rerank) | Scores query+doc jointly through one model pass | Higher (one pass per candidate) | Highest |
| ColBERT-style (late interaction) | Token-level embeddings, interaction at scoring time | Medium | High, cheaper than full cross-encoder at scale |
| LLM-as-reranker | Prompt an LLM to score or reorder candidates | Highest, and costs tokens | Can be very high, but slow and expensive for large candidate sets |
| No reranker (bi-encoder score only) | Just use ANN similarity score | Lowest | Lowest, fine when retrieval alone already hits target recall |

---

## Distance Metrics

| Metric | What it measures | When to use |
|---|---|---|
| Cosine similarity | Angle between vectors, ignores magnitude | Default for most text embedding models (they're trained/normalized for it) |
| Dot product | Angle and magnitude | Equivalent to cosine on normalized vectors; faster to compute (no normalization step) |
| Euclidean (L2) | Straight-line distance | Less common for text embeddings; matters when magnitude carries real signal |

Rule of thumb: use whichever metric the embedding model was trained/evaluated with. Mismatching (e.g. Euclidean on a cosine-trained model) silently degrades results without erroring.

---

## Hybrid Search Fusion Methods

| Method | How it combines dense + sparse | Notes |
|---|---|---|
| Reciprocal Rank Fusion (RRF) | Sums `1/(k + rank)` across each ranked list | Score-scale agnostic, simple, works well as a default |
| Weighted score sum | `w1 * dense_score + w2 * sparse_score` | Needs score normalization first; weights need tuning per corpus |
| Cascade | Run one method first, use the other only to filter/boost | Useful when one signal is clearly primary for your domain |
