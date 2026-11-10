"""The evaluator must grade structured JSON without comparing Python dicts."""
import copy
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

import run_eval
from providers.base import ModelResponse, ToolCall


ROOT = Path(__file__).resolve().parents[1]


def deduplicate_case():
    dataset = json.loads((ROOT / "data/eval_group.json").read_text(encoding="utf-8"))
    return next(case for case in dataset["cases"] if case["id"] == "G01_deduplicate_items")


def test_g01_matching_object_list_is_measured_as_pass():
    case = deduplicate_case()
    calls = copy.deepcopy(case["expect"]["tool_calls"])
    result = run_eval.evaluate_phase_b(case, calls, None)
    assert result["passed"] is True
    assert result["failures"] == []


@pytest.mark.parametrize("change", ["drop_duplicate", "reorder", "wrong_url"])
def test_g01_incorrect_items_fail_arguments_without_crashing(change):
    case = deduplicate_case()
    calls = copy.deepcopy(case["expect"]["tool_calls"])
    items = calls[0]["args"]["items"]
    if change == "drop_duplicate":
        items.pop()
    elif change == "reorder":
        items.reverse()
    else:
        items[0]["url"] = "https://example.com/wrong"
    result = run_eval.evaluate_phase_b(case, calls, None)
    assert result["passed"] is False
    assert result["routing_correct"] is True
    assert result["observed_mismatch"] == "wrong_arg_value"


def test_scalar_list_comparison_preserves_existing_order_insensitive_behavior():
    ok, failures, correct, total = run_eval.compare_subset(
        {"options": ["WEB", "Twitter"]}, {"options": [" twitter ", "web"]}
    )
    assert ok is True
    assert failures == []
    assert correct == total == 1


def test_nested_objects_normalize_values_without_losing_keys():
    ok, failures, _, _ = run_eval.compare_subset(
        {"items": [{"title": "Title", "details": {"tags": ["B", "A"]}}]},
        {"items": [{"details": {"tags": ["a", " b "]}, "title": " title "}]},
    )
    assert ok is True
    assert failures == []


def test_mixed_scalar_types_do_not_crash_sorting():
    assert run_eval.normalize_value([None, 3, "A", True]) == run_eval.normalize_value([True, "a", 3, None])


def test_nested_array_order_remains_significant():
    ok, _, _, _ = run_eval.compare_subset(
        {"items": [[1, 2], [3]]}, {"items": [[3], [1, 2]]}
    )
    assert ok is False


def test_cli_eval_executes_and_scores_deduplicate_offline(monkeypatch):
    case = deduplicate_case()

    class Provider:
        default_model = "offline-test"

        def complete(self, messages, tools=None, **kwargs):
            return ModelResponse(text=None, tool_calls=[
                ToolCall("deduplicate", copy.deepcopy(case["expect"]["tool_calls"][0]["args"]))
            ])

    with TemporaryDirectory(prefix="day03-eval-test-") as directory:
        root = Path(directory)
        cases = root / "cases.json"
        cases.write_text(json.dumps({"cases": [case]}), encoding="utf-8")
        monkeypatch.setattr(run_eval, "make_provider", lambda _: Provider())
        monkeypatch.setattr("sys.argv", [
            "run_eval.py", "--provider", "openrouter", "--version", "offline-test",
            "--suite", "group", "--eval-cases", str(cases), "--runs-dir", str(root / "runs"),
        ])
        run_eval.main()
        saved = json.loads(next((root / "runs").glob("*.json")).read_text(encoding="utf-8"))
        assert saved["summary"]["measured_cases"] == 1
        assert saved["summary"]["passed_cases"] == 1
        assert saved["summary"]["provider_error_cases"] == 0
        assert saved["results"][0]["tool_results"][0]["result"]["item_count"] == 2
