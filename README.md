# darkhorseprojects-packages

Package collection for Dark Horse Projects.

Each package lives in its own directory and owns a `zinc.pkg.yaml` manifest. Packages are independently versioned and released with package-specific tags.

Current packages:

- `openai-responses` — self-contained OpenAI Responses-shaped adapter package.

Manifest assets use one namespace of named paths:

```yaml
assets:
  short-answer: shapes/short-answer.circuitry.yaml
  responses: adapters/responses.py
  runtime-prompt: prompts/runtime.md
```

Zinc resolves asset references from context. A `shape:` reference must load as Circuitry. An `adapter:` reference must be runnable as an adapter program.

Packages can provide guided lifecycle scripts:

```yaml
scripts:
  setup:
    linux: scripts/setup
  check:
    linux: scripts/check
  remove:
    linux: scripts/remove
```

Soft dependencies are declared by package name and version, reported during inspect/install, and never installed automatically.
