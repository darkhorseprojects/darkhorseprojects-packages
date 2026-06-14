# darkhorseprojects-packages

Package collection for Dark Horse Projects.

Each package is a self-contained directory with a `zinc.pkg.yaml` manifest. Zinc registers package roots and resolves package paths lazily from the manifest; it does not catalog package files into its database.

Current packages:

- `openai-responses` — model adapter package for OpenAI Responses-compatible and chat-completions-compatible endpoints.

## Install

```bash
zn pkg install "$PWD/openai-responses" --global
zn pkg check openai-responses
```

Package references are manifest paths:

```text
openai-responses.adapter
openai-responses.config.models
openai-responses.shapes.short_answer
```

Example model config:

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

Lifecycle hooks are ordinary manifest paths:

```yaml
setup:
  linux: scripts/setup
check:
  linux: scripts/check
remove:
  linux: scripts/remove
```

Package config remains inside the package unless a human explicitly copies or references it elsewhere.
