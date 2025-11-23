import os
import glob
from typing import List, Dict
from rank_bm25 import BM25Okapi
import re

class Retriever:
    def __init__(self, docs_dir: str = "docs"):
        self.docs_dir = docs_dir
        self.chunks: List[Dict] = []
        self.bm25 = None
        self.corpus_tokenized = []
        self._load_and_chunk_docs()
        self._build_index()

    def _load_and_chunk_docs(self):
        """Loads markdown files and chunks them by paragraphs/headers."""
        md_files = glob.glob(os.path.join(self.docs_dir, "*.md"))
        
        for file_path in md_files:
            filename = os.path.basename(file_path).replace(".md", "")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Simple chunking by double newline (paragraphs)
            # Also keeping headers with the content could be useful, but for now simple paragraph split
            raw_chunks = re.split(r'\n\s*\n', content)
            
            for i, chunk in enumerate(raw_chunks):
                if chunk.strip():
                    self.chunks.append({
                        "id": f"{filename}::chunk{i}",
                        "content": chunk.strip(),
                        "source": filename
                    })

    def _build_index(self):
        """Builds the BM25 index."""
        self.corpus_tokenized = [self._tokenize(chunk["content"]) for chunk in self.chunks]
        self.bm25 = BM25Okapi(self.corpus_tokenized)

    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization."""
        return text.lower().split()

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        """Retrieves top-k chunks for a query."""
        if not self.bm25:
            return []
            
        tokenized_query = self._tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)
        
        # Get top-k indices
        top_n_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        
        results = []
        for idx in top_n_indices:
            # Filter out very low scores if needed, but for now return top k
            results.append({
                **self.chunks[idx],
                "score": float(scores[idx])
            })
            
        return results
