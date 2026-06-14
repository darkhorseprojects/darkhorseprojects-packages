# openai-responses

Self-contained model adapter package for OpenAI Responses-compatible and chat-completions-compatible endpoints.

Zinc only registers the package root. Everything else stays in this package and is resolved by walking `zinc.pkg.yaml`.

Useful package paths:

```text
openai-responses.adapter
openai-responses.config.models
openai-responses.shapes.short_answer
openai-responses.prompts.runtime
openai-responses.docs.readme
```

## Install

```bash
zn pkg install "$PWD/openai-responses" --global
zn pkg check openai-responses
```

Install does not copy package config into `~/.zinc`. Use or edit this file directly when you want this package's model profile:

```text
openai-responses/config/zinc.models.yaml
```

A Zinc config can point at the adapter like this:

```yaml
models:
  default: local-llama
  local-llama:
    adapter: openai-responses.adapter
    params:
      endpoint: http://127.0.0.1:30000
      endpoint_kind: chat_completions
      model: local-gemma-4-e4b-it
```

## Adapter contract

The adapter receives a YAML request file path as argv[1]. `does` arrives as `instruction`; it is not shell text or Zinc code.

```yaml
model: local-llama
part: answer
part_material: |
  {"part":{"name":"answer"}}
params:
  endpoint: http://127.0.0.1:30000
  endpoint_kind: chat_completions
  model: local-gemma-4-e4b-it
instruction: |
  Answer in one short sentence.
takes:
  question: |
    What is Zinc?
gives:
  answer: text
```

It returns YAML:

```yaml
text: |
  Optional visible text.
reasoning: |
  Optional provider reasoning summary.
gives:
  answer: |
    Zinc coordinates Circuitry execution through package capabilities.
```
