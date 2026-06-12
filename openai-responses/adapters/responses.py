#!/usr/bin/env python3
import json
import sys
import urllib.request
import urllib.error

import yaml


def main() -> int:
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as handle:
            request = yaml.safe_load(handle.read()) or {}
    else:
        request = yaml.safe_load(sys.stdin.read()) or {}
    params = request.get("params") or {}
    endpoint = str(params.get("endpoint") or "").rstrip("/")
    endpoint_kind = params.get("endpoint_kind") or "responses"
    if not endpoint:
        raise SystemExit("missing params.endpoint")

    if endpoint_kind == "responses":
        response = call_responses(endpoint, request, params)
    elif endpoint_kind == "chat_completions":
        response = call_chat_completions(endpoint, request, params)
    else:
        raise SystemExit(f"unsupported endpoint_kind: {endpoint_kind}")

    sys.stdout.write(render_response_yaml(response))
    return 0


def call_responses(endpoint: str, request: dict, params: dict) -> dict:
    payload = {
        "model": params.get("model"),
        "input": build_prompt(request),
        "temperature": params.get("temperature", 0.2),
        "max_output_tokens": params.get("max_output_tokens", 512),
    }
    if "reasoning" in params:
        payload["reasoning"] = params["reasoning"]
    data = post_json(f"{endpoint}/v1/responses", payload)
    text = extract_responses_text(data)
    return shape_response(request, text, data)


def call_chat_completions(endpoint: str, request: dict, params: dict) -> dict:
    payload = {
        "model": params.get("model", "local"),
        "messages": [
            {"role": "system", "content": "You are a Zinc model adapter. Return exactly the requested YAML."},
            {"role": "user", "content": build_prompt(request)},
        ],
        "temperature": params.get("temperature", 0.2),
        "max_tokens": params.get("max_output_tokens", 512),
    }
    reasoning = params.get("reasoning") or {}
    if "max_tokens" in reasoning:
        payload["reasoning_budget"] = reasoning["max_tokens"]
    data = post_json(f"{endpoint}/v1/chat/completions", payload)
    text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    return shape_response(request, text, data)


def build_prompt(request: dict) -> str:
    gives = request.get("gives") or {}
    takes = request.get("takes") or {}
    lines = [
        "Execute this Zinc action-part.",
        "Return YAML with top-level keys: text, reasoning, gives.",
        "Each requested give must appear under gives with type and value.",
        "Do not include markdown fences.",
        "",
        f"part: {request.get('part', '')}",
        "instructions: |",
    ]
    for line in str(request.get("instructions") or "").splitlines() or [""]:
        lines.append(f"  {line}")
    lines.append("takes:")
    for name, item in takes.items():
        value = item.get("value", "") if isinstance(item, dict) else item
        type_label = item.get("type", "value") if isinstance(item, dict) else "value"
        lines.append(f"  {name}:")
        lines.append(f"    type: {type_label}")
        lines.append("    value: |")
        for line in str(value).splitlines() or [""]:
            lines.append(f"      {line}")
    lines.append("gives:")
    for name, type_label in gives.items():
        lines.append(f"  {name}: {type_label}")
    return "\n".join(lines) + "\n"


def shape_response(request: dict, text: str, raw: dict) -> dict:
    parsed = parse_yaml_text(text)
    requested = request.get("gives") or {}
    parsed_gives = parsed.get("gives") if isinstance(parsed, dict) else None
    gives = {}
    for name, type_label in requested.items():
        value = text.strip()
        item = parsed_gives.get(name) if isinstance(parsed_gives, dict) else None
        if isinstance(item, dict):
            value = item.get("value", value)
            type_label = item.get("type", type_label)
        elif item is not None:
            value = item
        elif isinstance(parsed, dict) and isinstance(parsed.get(name), str):
            value = parsed[name]
        if str(value).strip() == str(type_label).strip() and text.strip():
            value = text.strip()
        gives[name] = {"type": type_label, "value": str(value)}

    visible = parsed.get("text") if isinstance(parsed, dict) and isinstance(parsed.get("text"), str) else text.strip()
    reasoning = parsed.get("reasoning") if isinstance(parsed, dict) and isinstance(parsed.get("reasoning"), str) else extract_reasoning(raw)
    return {"text": visible, "reasoning": reasoning, "gives": gives}


def parse_yaml_text(text: str):
    try:
        return yaml.safe_load(text)
    except Exception:
        return None


def extract_responses_text(data: dict) -> str:
    if "output_text" in data:
        return data["output_text"] or ""
    chunks = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in ("output_text", "text"):
                chunks.append(content.get("text", ""))
    return "\n".join(chunks)


def extract_reasoning(data: dict) -> str:
    chunks = []
    for item in data.get("output", []):
        if item.get("type") == "reasoning":
            summary = item.get("summary")
            if isinstance(summary, list):
                chunks.extend(str(x.get("text", x)) for x in summary)
            elif summary:
                chunks.append(str(summary))
    usage = data.get("usage")
    if usage:
        chunks.append("usage: " + json.dumps(usage, sort_keys=True))
    return "\n".join(chunks)


def render_response_yaml(response: dict) -> str:
    lines = []
    lines.append("text: |")
    for line in str(response.get("text", "")).splitlines() or [""]:
        lines.append(f"  {line}")
    lines.append("reasoning: |")
    for line in str(response.get("reasoning", "")).splitlines() or [""]:
        lines.append(f"  {line}")
    lines.append("gives:")
    for name, item in (response.get("gives") or {}).items():
        lines.append(f"  {name}:")
        lines.append(f"    type: {item.get('type', 'text')}")
        lines.append("    value: |")
        for line in str(item.get("value", "")).splitlines() or [""]:
            lines.append(f"      {line}")
    return "\n".join(lines) + "\n"


def post_json(url: str, payload: dict) -> dict:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers={"content-type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        raise SystemExit(f"provider request failed: {exc.code} {detail}") from exc


if __name__ == "__main__":
    raise SystemExit(main())
