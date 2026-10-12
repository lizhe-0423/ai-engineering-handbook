"""Run a synthetic confirmed-text case; model calls require explicit --model."""
import argparse
import json
import sys
from pathlib import Path

import ollama_client
from qa_core import RESPONSE_SCHEMA, compose_messages, plan_answer, validate_response


def main(argv=None):
    try:
        data = json.loads((Path(__file__).parent / "data" / "cases.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"案例数据读取失败：{exc}", file=sys.stderr)
        return 1
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=sorted(data["cases"]), default="math_bank")
    parser.add_argument("--level", choices=["hint", "solution"], default="hint")
    parser.add_argument("--model", help="existing local Ollama model; no automatic download")
    parser.add_argument("--unconfirmed", action="store_true", help="simulate uncertain input")
    args = parser.parse_args(argv)
    if args.model is not None and not args.model.strip():
        parser.error("--model must name an existing local model")
    case = data["cases"][args.case]
    try:
        plan = plan_answer(case["question"], case["course_id"], data, args.level,
                           input_confirmed=not args.unconfirmed)
        if plan["state"] == "model_required":
            messages = compose_messages(plan)
            if args.model:
                raw = ollama_client.complete(args.model, messages, RESPONSE_SCHEMA)
                plan["model_call_performed"] = True
                plan = validate_response(plan, raw)
                plan["model"] = args.model
            else:
                plan["prepared_request"] = {"messages": messages, "format": RESPONSE_SCHEMA}
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError) as exc:
        print(f"答疑失败：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
