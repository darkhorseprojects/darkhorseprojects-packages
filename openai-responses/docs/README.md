# openai-responses Zinc package

This package provides a Zinc model adapter with a Responses-shaped adapter contract.

The adapter accepts YAML on stdin:

```yaml
part: draft
model: local-llama
params:
  provider: llama.cpp
  endpoint: http://127.0.0.1:30000
  endpoint_kind: chat_completions
  model: local-gemma-4-e4b-it
  temperature: 0.2
  max_output_tokens: 512
  context_window: 16384
  reasoning:
    effort: medium
    max_tokens: 512

instructions: |
  Draft the answer.

takes:
  question:
    type: text
    value: What is Zinc?

gives:
  answer: text
```

It returns YAML:

```yaml
text: |
  Visible text if useful.

reasoning: |
  Reasoning summary if the provider returns one.

gives:
  answer:
    type: text
    value: |
      Zinc is a local runtime for Circuitry systems.
```

`config/zinc.models.yaml` is package-provided config for a local llama.cpp server on `127.0.0.1:30000` with a 16k context window and a 512-token reasoning budget.
