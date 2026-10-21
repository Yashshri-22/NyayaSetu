# Architecture
User → React frontend → FastAPI → document extraction and clause segmentation → ChromaDB retrieval → Gemini generation (when configured) → evidence-referenced response. PostgreSQL stores users/documents/clauses. Retrieval filters by document and user IDs. The prototype uses heuristic fallbacks for risk and notice-period conflict screening.
