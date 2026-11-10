"""Documentation must work on case-sensitive filesystems and match the schema."""
from pathlib import Path

import pytest
import yaml

from tools import load_tool_declarations


ROOT = Path(__file__).resolve().parents[1]
DECLARATIONS = load_tool_declarations(ROOT / "artifacts/tools.yaml")


@pytest.mark.parametrize("declaration", DECLARATIONS, ids=lambda item: item["name"])
def test_tool_documentation_matches_inputs_and_has_usage_boundaries(declaration):
    folder = ROOT / "tools" / declaration["name"]
    assert "TOOL.md" in {path.name for path in folder.iterdir()}
    document = (folder / "TOOL.md").read_text(encoding="utf-8")
    front = yaml.safe_load(document.split("---", 2)[1])
    assert front["name"] == declaration["name"]
    assert set(front["inputs"]) == set(declaration["parameters"]["properties"])
    assert "## Khi dùng" in document
    assert "## Khi không dùng" in document
    if declaration["name"] == "send":
        assert front["requires_confirmation"] is True
        assert front["side_effect"] is True
