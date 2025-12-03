import json
from rank_bm25 import BM25Okapi
import gzip
import requests





def load_bm25_corpus(limit: int = 20):   # choose a size that fits in memory
    bm25_corpus = []
    vocab = []

    count = 0

    with gzip.open("el-extract.jsonl.gz", "rb") as f:
        for line in f:
            if count >= limit:
                break

            entry = json.loads(line.strip())
            if entry.get("lang") == "Greek" and entry.get("pos") and "senses" in entry:
                lemma = entry["word"]
                for sense in entry["senses"]:
                    glosses = sense.get("glosses", [])
                    examples = sense.get("examples", [])

                    text_parts = [lemma]
                    if glosses:
                        text_parts.append(glosses[0])
                    if examples:
                        text_parts.append(examples[0].get("text", ""))

                    full_text = ". ".join(text_parts)
                    bm25_corpus.append(full_text)
                    vocab.append(lemma)

                    count += 1
                    if count >= limit:
                        break

    return bm25_corpus, vocab


# Build corpus and index at import time
bm25_corpus, vocab = load_bm25_corpus()
bm25 = BM25Okapi(bm25_corpus)

word2index = {}
for i, word in enumerate(vocab):
    word2index.setdefault(word, []).append(i)

def search_word(query, k=5):
    q = query.strip()
    if not q:
        return []

    # Exact lemma match
    if q in word2index:
        results = []
        for idx in word2index[q]:
            results.append(
                {
                    "word": vocab[idx],
                    "definition": bm25_corpus[idx],
                    "score": float("inf"),
                    "source": "exact_title",
                }
            )
        return results

    # BM25 fallback
    tokens = q.lower().split()
    scores = bm25.get_scores(tokens)
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]

    results = []
    for idx in top_indices:
        results.append(
            {
                "word": vocab[idx],
                "definition": bm25_corpus[idx],
                "score": float(scores[idx]),
                "source": "bm25",
            }
        )
    return results
