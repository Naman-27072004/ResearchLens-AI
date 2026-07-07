from backend.chunker import split_text

def test_split_text():
    text = "This is a sentence. " * 100
    chunks = split_text(text)
    assert len(chunks) > 0
    for chunk in chunks:
        assert len(chunk) <= 1000
