from app.core import settings
_client=None;_col=None
def col():
    global _client,_col
    if _col is not None:return _col
    try:
        import chromadb
        _client=chromadb.PersistentClient(path=settings.chroma_persist_dir)
        _col=_client.get_or_create_collection("nyayasetu_clauses")
        return _col
    except Exception:return None
def index(doc_id,uid,clauses):
    c=col()
    if c is None or not clauses:return
    try:c.delete(where={"$and":[{"document_id":doc_id},{"user_id":uid}]})
    except Exception:pass
    c.add(ids=[f"u{uid}-d{doc_id}-c{i}" for i in range(len(clauses))],documents=[x["text"] for x in clauses],
      metadatas=[{"document_id":doc_id,"user_id":uid,"page_number":x["page_number"],"clause_number":x["clause_number"] or "Unnumbered"} for x in clauses])
def retrieve(query,doc_id,uid,k=5):
    c=col()
    if c is None:return []
    try:
        r=c.query(query_texts=[query],n_results=k,where={"$and":[{"document_id":doc_id},{"user_id":uid}]})
        return [{"text":t,**(r["metadatas"][0][i] or {})} for i,t in enumerate(r["documents"][0])]
    except Exception:return []
