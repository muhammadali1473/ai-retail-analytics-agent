# MyBrain AI (Personal Knowledge Agent)

## Overview
MyBrain AI is a personal knowledge agent that captures your notes, chats, and ideas, then answers questions using only your private data. It focuses on building a durable memory layer and returning concise, context-aware responses.

## Core capabilities
- **Personal memory vault**: Store notes, chats, and ideas with metadata (source, timestamp, tags).
- **User-based indexing**: Build per-user embeddings and keyword indexes to keep data isolated.
- **Context filtering**: Retrieve only the most relevant memories for each query.
- **Grounded answers**: Generate responses with citations to the original memory items.

## Why it’s trending
- Personal AI assistants are the next step after general chatbots.
- Users want answers from **their own data**, not public sources.
- Long-term memory unlocks personalized productivity and creativity.

## Suggested architecture
1. **Ingestion**
   - Accept notes via web/mobile, email, or chat integrations.
   - Normalize content into a common schema.

2. **Storage**
   - Document store for raw items.
   - Vector index for semantic retrieval.
   - Metadata store for tags, topics, and access control.

3. **Retrieval & filtering**
   - Hybrid search (keyword + vector).
   - Recency and relevance scoring.
   - User-based access control at query time.

4. **Answering**
   - Prompt with retrieved memories.
   - Require citations for each claim.
   - Offer follow-up questions and memory updates.

## Example memory schema
```json
{
  "id": "note_123",
  "user_id": "user_abc",
  "content": "Idea: build a knowledge agent called MyBrain AI",
  "source": "mobile",
  "tags": ["idea", "product"],
  "created_at": "2024-01-10T12:00:00Z"
}
```

## Next steps to build
- Define MVP ingestion sources (notes + chat imports).
- Choose storage (SQLite or Postgres + vector extension).
- Implement retrieval pipeline with filters and scoring.
- Add a simple UI for capture and Q&A.
