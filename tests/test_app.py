import app


def test_safe_load_pdf_missing_file_returns_empty_text():
    result = app.safe_load_pdf("me/does_not_exist.pdf")
    assert result == ""


def test_record_user_details_rejects_invalid_email():
    result = app.record_user_details(email="invalid-email")
    assert result["recorded"] == "error"
    assert result["reason"] == "invalid_email"


def test_chat_returns_demo_message_without_openai_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    me = app.Me()
    response = me.chat("hello", [])
    assert "demo mode" in response.lower()


def test_create_chat_interface_builds_without_openai_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    interface = app.create_chat_interface()
    assert interface is not None
