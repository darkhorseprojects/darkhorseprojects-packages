# openai-responses

Self-contained model adapter package with an OpenAI Responses-shaped contract.

The package manifest exposes named path assets. Zinc resolves `short-answer` as a shape when a Circuitry document uses it in `shape:` context, and resolves `responses` as the adapter program when a model uses it in `adapter:` context.

## Install with `zn`

From a local clone of this package collection:

macOS/Linux:

```bash
git clone https://github.com/darkhorseprojects/darkhorseprojects-packages.git
cd darkhorseprojects-packages
zn pkg install "$PWD/openai-responses" --global
zn pkg check openai-responses
```

Windows PowerShell:

```powershell
git clone https://github.com/darkhorseprojects/darkhorseprojects-packages.git
Set-Location darkhorseprojects-packages
zn pkg install (Resolve-Path openai-responses) --global
zn pkg check openai-responses
```

The install registers `openai-responses`, runs the package setup script where declared, and makes these references available:

```yaml
zinc:
  packages:
    responses: openai-responses@0.1.8

uses:
  answer:
    shape: responses.shapes.short_answer
```

```yaml
models:
  default: local-llama
  local-llama:
    adapter: responses.adapter
```

Guided `setup`, `check`, and `remove` scripts are included for local configuration on macOS/Linux. On Windows, `zn pkg install` still registers the package; configure `~/.zinc/config.yaml` from `config/zinc.models.yaml` if no platform script runs.

## Adapter contract

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
    text: |
      What is this package?

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
  answer: |
    A concise answer.
```

`config/zinc.models.yaml` points at a local llama.cpp-compatible server on `127.0.0.1:30000` with a 16k context window and a 512-token reasoning budget.
