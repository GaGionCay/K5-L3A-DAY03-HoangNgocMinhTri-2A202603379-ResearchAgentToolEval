---
name: keyword_extract
track: core
kind: local_formatter
requires_env: []
inputs: [text, max_keywords]
outputs: [keywords, top_keywords]
side_effect: false
---
# keyword_extract

Extracts frequently occurring terms from text already provided by the user or
another tool. Use it to prepare search terms; it does not search the web or
social media and should not be used to discover facts.
