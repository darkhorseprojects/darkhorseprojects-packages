# darkhorseprojects-packages

Zinc package monorepo for Dark Horse Projects packages.

Each package lives in its own directory and owns a `zinc.pkg.yaml` manifest.

Current packages:

- `openai-responses` — OpenAI Responses-shaped model adapter package for Zinc.

Package manifests may declare `soft_dependencies`. Zinc reports these during inspect/install, but never installs them automatically.
