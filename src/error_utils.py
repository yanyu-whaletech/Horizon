"""Helpers for persisting useful errors without persisting credentials."""

from __future__ import annotations

import re


URL_RE = re.compile(r"https?://[^\s\"'<>]+", re.IGNORECASE)
BEARER_RE = re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]+", re.IGNORECASE)
SECRET_ASSIGNMENT_RE = re.compile(
    r"\b(api[_-]?key|access[_-]?token|token|secret|password)=([^\s&,;]+)",
    re.IGNORECASE,
)


def safe_error_message(error: BaseException, limit: int = 1000) -> str:
    """Return a compact error message with common credential shapes removed."""

    message = str(error).strip() or error.__class__.__name__
    message = URL_RE.sub("<url>", message)
    message = BEARER_RE.sub("Bearer <redacted>", message)
    message = SECRET_ASSIGNMENT_RE.sub(lambda match: f"{match.group(1)}=<redacted>", message)
    return message[:limit]
