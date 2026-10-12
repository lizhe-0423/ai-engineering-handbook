"""Ollama native non-streaming Chat API; localhost only, stdlib only."""
import http.client
import json
import urllib.request

MAX_BYTES = 2 * 1024 * 1024


def complete(model, messages, schema):
    body = {"model": model, "messages": messages, "stream": False,
            "format": schema, "options": {"temperature": 0}}
    request = urllib.request.Request(
        "http://localhost:11434/api/chat", method="POST",
        headers={"Content-Type": "application/json"},
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"))
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read(MAX_BYTES + 1)
    except http.client.HTTPException as exc:
        raise ValueError("Ollama HTTP response was interrupted or malformed") from exc
    if len(raw) > MAX_BYTES:
        raise ValueError("Ollama response exceeds the demo size limit")
    try:
        value = json.loads(raw)
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError("Ollama returned invalid outer JSON") from exc
    if not isinstance(value, dict) or value.get("done") is not True:
        raise ValueError("Ollama did not return a completed non-streaming response")
    message = value.get("message")
    if not isinstance(message, dict) or not isinstance(message.get("content"), str) or not message["content"].strip():
        raise ValueError("Ollama message.content must be non-empty text")
    return message["content"]
