from backend.citation_analyzer import extract_references, author_statistics, citation_analysis

def test_extract_references():
    text = "Introduction ... results. References\n1. Author A, Title A, 2020.\n2. Author B, Title B, 2021."
    refs = extract_references(text)
    assert len(refs) == 2
    assert "1. Author A, Title A, 2020." in refs
    assert "2. Author B, Title B, 2021." in refs

def test_author_statistics():
    refs = [
        "1. Smith J, Title A, 2020.",
        "2. Smith J, Title B, 2021.",
        "3. Doe J, Title C, 2022."
    ]
    stats = author_statistics(refs)
    assert len(stats) > 0
    # Smith appears twice, Doe appears once
    assert stats[0] == ("Smith", 2)
    assert stats[1] == ("Doe", 1)

def test_citation_analysis():
    text = "Details ... Bibliography\nSmith J, Title A, 2020.\nDoe J, Title B, 2021."
    res = citation_analysis(text)
    assert res["total_references"] == 2
    assert len(res["references"]) == 2
    assert len(res["top_authors"]) == 2
