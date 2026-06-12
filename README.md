# darkhorseprojects-packages

Package collection for Dark Horse Projects.

Each package lives in its own directory and owns a `zinc.pkg.yaml` manifest. Packages are independently versioned and released with package-specific tags.

Current packages:

- `openai-responses` — self-contained OpenAI Responses-shaped adapter package.

Manifest assets use one namespace:

```yaml
assets:
  responses:
    path: adapters/responses.py
    does:
      - zinc.adapter
      - openai.responses
```

Soft dependencies are declared by package name and version, reported during inspect/install, and never installed automatically.
