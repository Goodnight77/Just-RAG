# Debug This RAG System

Each scenario describes symptoms of a broken or underperforming RAG system. Try to diagnose the root cause and fix before reading the answer.

---

## Scenario 1: The answer is confidently wrong, but the right info was retrieved

**Symptom**: You check the logs, the correct passage is in the top-3 retrieved chunks. The LLM still gives a wrong or contradictory answer.

**Diagnosis checklist**:
- Is the correct chunk positioned poorly in context (middle of a long list)? "Lost in the middle" is the most common cause here.
- Are there *other* retrieved chunks that contradict it? A confidently wrong answer often means the model picked the wrong one of two conflicting sources, not that it ignored the right one.
- Is the prompt telling the model to synthesize/summarize instead of quote/cite? Summarization is where models introduce claims not actually in the source.

**Fix**: Reorder context to put highest-rerank-score chunks first and last, not by original retrieval order. Add explicit "cite the chunk you used" instruction. If contradictory chunks are a recurring issue, that's a data quality problem (duplicate/stale docs in the corpus), not a prompting problem.

---

## Scenario 2: Retrieval quality was fine last month, degrading since

**Symptom**: recall@k on your eval set has been slowly dropping over weeks. No code changes to the retrieval pipeline.

**Diagnosis checklist**:
- Has the corpus grown a lot? More documents means more near-neighbor competition: a chunk that used to be the clear top-1 match now has more lookalikes.
- Has an ANN index parameter (e.g. HNSW `ef_search`, quantization) changed, even indirectly through a DB version upgrade default?
- Is there stale/duplicate/junk content accumulating (failed ingestion retries writing duplicates, deleted docs not actually pruned from the index)?
- Has the query distribution shifted (new user segment, new product line) away from what the corpus/eval set covers?

**Fix**: depends on which of the above, but the process is the same: re-run the eval set with a frozen historical corpus snapshot to isolate "did the index/model change" from "did the data change."

---

## Scenario 3: Works great in testing, terrible in production

**Symptom**: Manual QA looks good. Real user metrics (thumbs down rate, escalation rate) are bad.

**Diagnosis checklist**:
- Is your eval set representative of real queries? Internal testers write clean, well-formed questions; real users write typos, fragments, multi-part questions.
- Are production queries longer/shorter than what the retriever or reranker was validated on?
- Is there a latency timeout truncating retrieval (e.g. falling back to fewer chunks or skipping rerank under load) that testing never hit?
- Check whether production traffic includes adversarial or out-of-domain queries the corpus simply doesn't cover. The right answer here is "I don't know," and if the system doesn't have that fallback, it hallucinates instead.

**Fix**: rebuild the eval set from *sampled real production queries*, not synthetic/internal ones. Add an explicit low-confidence refusal path.

---

## Scenario 4: Latency spiked after adding a reranker

**Symptom**: p50 latency fine, p99 latency doubled after introducing a cross-encoder reranking stage.

**Diagnosis checklist**:
- Is the reranker running on the full top-k candidate set (e.g. 100) for every query, including ones where the bi-encoder retrieval was already unambiguous?
- Is reranking batched, or looping one-candidate-at-a-time?
- Is the reranker on CPU when it should be on GPU, or cold-starting per request (model load on every call)?

**Fix**: cap candidate set size sent to reranker (e.g. top 20 not top 100), batch the scoring call, keep the model warm/loaded. Consider skipping rerank entirely when the top bi-encoder result has a large score margin over the rest (cheap confidence heuristic).

---

## Scenario 5: New embedding model made retrieval worse, not better

**Symptom**: Swapped to a higher-MTEB-ranked embedding model. Recall@k on your own eval set dropped.

**Diagnosis checklist**:
- Did you re-embed the *entire* corpus with the new model, or is there a mix of old and new vectors in the same index? (Mixing vector spaces from different models is silently broken: cosine similarity between them is meaningless.)
- Does the new model expect specific query/passage prefixes (e.g. `"query: "` / `"passage: "`) that weren't applied?
- Is the new model actually better on general benchmarks but weaker on your domain's specific vocabulary (jargon, codenames, acronyms)?

**Fix**: full re-embed + reindex, verify prefix conventions match the model's training setup, and always validate against your own labeled eval set rather than trusting a general leaderboard rank.

---

## Scenario 6: Chatbot answers questions using outdated information after a document was updated

**Symptom**: Source doc was edited/corrected, but the bot still cites the old version.

**Diagnosis checklist**:
- Is the ingestion pipeline actually re-triggered on document update, or only on create?
- If re-embedded, was the *old* chunk's vector deleted from the index, or just superseded (both old and new now present, and retrieval sometimes surfaces the stale one)?
- Is there a caching layer (semantic cache, CDN, application-level) serving a stale generated answer from before the update?

**Fix**: ingestion must upsert-and-prune by stable document/chunk id, not append-only. Invalidate any query cache tied to the affected document on update.
