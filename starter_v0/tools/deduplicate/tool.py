from typing import Any


def deduplicate(items: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Giữ kết quả đầu tiên của mỗi URL, theo thứ tự đầu vào."""
    try:
        if not isinstance(items, list):
            raise ValueError("items phải là một danh sách.")

        unique_items = []
        seen_urls = set()

        for index, item in enumerate(items):
            if not isinstance(item, dict):
                raise ValueError(f"items[{index}] phải là một object.")

            url = item.get("url")
            if not isinstance(url, str) or not url.strip():
                raise ValueError(f"items[{index}] cần có URL không rỗng.")

            key = url.strip()
            if key not in seen_urls:
                seen_urls.add(key)
                unique_items.append(item.copy())

        return {
            "tool": "deduplicate",
            "items": unique_items,
            "input_count": len(items),
            "item_count": len(unique_items),
            "removed_count": len(items) - len(unique_items),
        }

    except ValueError as exc:
        return {
            "tool": "deduplicate",
            "error": "invalid_input",
            "message": str(exc),
        }