import contextlib
import http.client
import io
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ollama_client
import run


class RuntimeTests(unittest.TestCase):
    def call_cli(self, args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = run.main(args)
        self.assertEqual(code, 0)
        return json.loads(output.getvalue())

    def test_all_default_cases_run_without_network_or_model(self):
        with patch("ollama_client.complete", side_effect=AssertionError("unexpected model call")):
            for case, route, state in [("math_bank", "curated", "answered"),
                                       ("physics_rag", "rag", "model_required"),
                                       ("math_direct", "direct", "model_required")]:
                with self.subTest(case=case):
                    result = self.call_cli(["--case", case])
                    self.assertEqual((result["route"], result["state"]), (route, state))
                    self.assertFalse(result["model_call_performed"])

    def test_explicit_model_does_not_replace_curated_answer(self):
        with patch("ollama_client.complete", side_effect=AssertionError("unexpected model call")):
            result = self.call_cli(["--case", "math_bank", "--level", "solution", "--model", "local-model"])
        self.assertIn("x>2", result["reply"])

    def test_explicit_model_response_is_validated_and_recorded(self):
        answer = json.dumps({"reply": "S=πr²=9π cm²。", "next_action": "explain", "citations": []})
        with patch("ollama_client.complete", return_value=answer) as provider:
            result = self.call_cli(["--case", "math_direct", "--model", "local-model"])
        provider.assert_called_once()
        self.assertEqual(result["state"], "validated_draft")
        self.assertTrue(result["model_call_performed"])
        self.assertTrue(result["requires_content_review"])

    def test_model_failure_returns_nonzero_without_fake_answer(self):
        for result in ["[]", "not-json"]:
            with self.subTest(result=result), patch("ollama_client.complete", return_value=result):
                with contextlib.redirect_stdout(io.StringIO()) as out, contextlib.redirect_stderr(io.StringIO()):
                    code = run.main(["--case", "math_direct", "--model", "local-model"])
                self.assertEqual(code, 1)
                self.assertEqual(out.getvalue(), "")

    def test_local_provider_failure_returns_nonzero(self):
        with patch("ollama_client.complete", side_effect=OSError("offline")):
            with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()) as out:
                code = run.main(["--case", "physics_rag", "--model", "local-model"])
            self.assertEqual(code, 1)
            self.assertEqual(out.getvalue(), "")

    def test_missing_or_broken_fixture_returns_nonzero(self):
        for failure in [FileNotFoundError("missing cases.json"), ValueError("invalid JSON")]:
            with self.subTest(failure=failure), patch("pathlib.Path.read_text", side_effect=failure):
                with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()) as out:
                    code = run.main([])
                self.assertEqual(code, 1)
                self.assertEqual(out.getvalue(), "")

    def test_provider_unpacks_nonstreamed_content_and_sends_schema(self):
        response = io.BytesIO(json.dumps({"done": True, "message": {"content": '{"reply":"hi"}'}}).encode())
        with patch("urllib.request.urlopen", return_value=response) as http:
            result = ollama_client.complete("local-model", [{"role": "user", "content": "question"}], {"type": "object"})
        self.assertEqual(result, '{"reply":"hi"}')
        request = http.call_args.args[0]
        payload = json.loads(request.data)
        self.assertEqual(request.full_url, "http://localhost:11434/api/chat")
        self.assertFalse(payload["stream"])
        self.assertEqual(payload["format"], {"type": "object"})
        self.assertEqual(payload["options"]["temperature"], 0)

    def test_provider_rejects_incomplete_or_malformed_outer_response(self):
        for raw in [b"[]", b"not-json", b'{"done":false,"message":{"content":"x"}}',
                    b'{"done":true,"message":{"content":42}}']:
            with self.subTest(raw=raw), patch("urllib.request.urlopen", return_value=io.BytesIO(raw)):
                with self.assertRaises(ValueError):
                    ollama_client.complete("local-model", [], {})

    def test_interrupted_http_response_becomes_reportable_error(self):
        with patch("urllib.request.urlopen", side_effect=http.client.IncompleteRead(b"partial")):
            with self.assertRaises(ValueError):
                ollama_client.complete("local-model", [], {})


if __name__ == "__main__":
    unittest.main()
