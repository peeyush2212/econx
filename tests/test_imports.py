def test_import_and_about():
    import econx

    assert hasattr(econx, "about")
    text = econx.about()
    assert "econx" in text.lower()
