from __future__ import annotations

from src.error_utils import safe_error_message


def test_safe_error_message_redacts_urls_and_credentials() -> None:
    error = RuntimeError(
        "GET https://huginn.example/feed/private-secret.xml failed "
        "with token=abc123 and Authorization: Bearer xyz789"
    )

    message = safe_error_message(error)

    assert "https://" not in message
    assert "private-secret" not in message
    assert "abc123" not in message
    assert "xyz789" not in message
    assert "token=<redacted>" in message
    assert "Bearer <redacted>" in message
