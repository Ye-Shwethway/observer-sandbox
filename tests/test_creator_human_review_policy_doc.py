from pathlib import Path


def test_human_review_policy_documents_refs_and_export_names():
    text = Path("docs/CREATOR_STUDIO_HUMAN_REVIEW_UI_V1.md").read_text(encoding="utf-8")
    assert "Resolve batch-local references" in text
    assert "Hide internal definition keys and batch refs" in text
    assert "creator-studio-item-batch-<first-item-name>-plus-<remaining-count>-rN.txt" in text
    assert "creator-studio-character-<character-name>-rN.txt" in text
