"""Explicitly enabled local Ollama adapter. No automatic downloads or cloud calls."""
import json
from urllib.request import Request, urlopen


def parse_model_object(content):
    if not isinstance(content, str):
        raise ValueError('model content must be JSON text')
    try:
        value = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError('model returned invalid JSON') from exc
    if not isinstance(value, dict):
        raise ValueError('model response must be a JSON object')
    return value


def ollama_object(model, system, user, schema, images=None):
    message = {'role': 'user', 'content': user}
    if images:
        message['images'] = images
    body = {'model': model, 'stream': False, 'format': schema,
            'messages': [{'role': 'system', 'content': system}, message],
            'options': {'temperature': 0}}
    request = Request('http://localhost:11434/api/chat',
                      data=json.dumps(body, ensure_ascii=False).encode(),
                      headers={'Content-Type': 'application/json'}, method='POST')
    with urlopen(request, timeout=60) as response:
        payload = json.loads(response.read(2 * 1024 * 1024))
    try:
        content = payload['message']['content']
    except (KeyError, TypeError) as exc:
        raise ValueError('missing Ollama message.content') from exc
    return parse_model_object(content)
