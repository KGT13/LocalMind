# test_vector_store.py
# Run this from your project root with: python -m pytest tests/test_vector_store.py -v
# Or as a plain script: python tests/test_vector_store.py
 
from src.infrastructure.database import (
    add_chunks,
    query,
    get_chunks_by_source,
    document_exists,
    delete_document,
    list_documents,
)
 
# ── Fake data ─────────────────────────────────────────────────────────────────
# Pretend this came from a real PDF. Three chunks, one source file.
FAKE_CHUNKS = [
    "The mitochondria is the powerhouse of the cell.",
    "Photosynthesis converts sunlight into energy in plants.",
    "DNA carries the genetic instructions for all living organisms.",
]
 
FAKE_METADATAS = [
    {"source": "biology_notes.pdf", "page": 1},
    {"source": "biology_notes.pdf", "page": 2},
    {"source": "biology_notes.pdf", "page": 3},
]
 
FAKE_IDS = [
    "biology_notes.pdf_chunk_0",
    "biology_notes.pdf_chunk_1",
    "biology_notes.pdf_chunk_2",
]
 
FAKE_FILENAME = "biology_notes.pdf"
 
 
# ── Tests ─────────────────────────────────────────────────────────────────────
 
def test_add_chunks():
    """After adding, the document should exist in the DB."""
    add_chunks(FAKE_CHUNKS, FAKE_METADATAS, FAKE_IDS)
    assert document_exists(FAKE_FILENAME), "Document should exist after add_chunks()"
    print("PASS  test_add_chunks")
 
 
def test_list_documents():
    """The filename should appear in list_documents()."""
    docs = list_documents()
    assert FAKE_FILENAME in docs, f"{FAKE_FILENAME} should be in list_documents()"
    print("PASS  test_list_documents")
 
 
def test_get_chunks_by_source():
    """Should return exactly 3 chunks for our fake file."""
    results = get_chunks_by_source(FAKE_FILENAME)
    assert len(results["ids"]) == 3, "Should find 3 chunks for biology_notes.pdf"
    print("PASS  test_get_chunks_by_source")
 
 
def test_document_exists_true():
    """Should return True for a file we know is stored."""
    assert document_exists(FAKE_FILENAME) is True
    print("PASS  test_document_exists (True case)")
 
 
def test_document_exists_false():
    """Should return False for a file that was never added."""
    assert document_exists("made_up_file.pdf") is False
    print("PASS  test_document_exists (False case)")
 
 
def test_query():
    """A relevant question should return at least one result."""
    results = query("What is the powerhouse of the cell?", top_k=2)
    assert len(results["documents"][0]) > 0, "Query should return at least one result"
    print("PASS  test_query")
 
 
def test_query_with_filter():
    """Filtering by source should still return results from that file."""
    results = query("genetic instructions", top_k=2, filter_source=FAKE_FILENAME)
    assert len(results["documents"][0]) > 0, "Filtered query should return results"
    print("PASS  test_query_with_filter")
 
 
def test_delete_document():
    """After deleting, the document should no longer exist."""
    delete_document(FAKE_FILENAME)
    assert document_exists(FAKE_FILENAME) is False, "Document should be gone after delete"
    print("PASS  test_delete_document")
 
 
def test_delete_nonexistent_document():
    """Deleting a file that doesn't exist should not crash."""
    try:
        delete_document("never_existed.pdf")
        print("PASS  test_delete_nonexistent_document")
    except Exception as e:
        print(f"FAIL  test_delete_nonexistent_document — crashed with: {e}")
 
 
# ── Runner ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\nRunning LocalMind vector store tests...\n")
 
    # Order matters — add first, then read, then delete last
    test_add_chunks()
    test_list_documents()
    test_get_chunks_by_source()
    test_document_exists_true()
    test_document_exists_false()
    test_query()
    test_query_with_filter()
    test_delete_document()
    test_delete_nonexistent_document()
 
    print("\nAll tests finished.")