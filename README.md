# darkhorseprojects-packages

Package collection for Dark Horse Projects.

Each package lives in its own directory and owns a `zinc.pkg.yaml` manifest. Packages are independently versioned and released with package-specific tags.

Current packages:

- `openai-responses` — self-contained OpenAI Responses-shaped adapter package.

## Quick install with `zn`

Clone this collection once, then install the package directory you want.

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

After installation, package assets are available as `alias.asset` references. For `openai-responses`, the setup config uses the `responses` alias:

```yaml
zinc:
  packages:
    responses: openai-responses@0.1.8

uses:
  answer:
    shape: responses.shapes.short_answer
```

Provider adapters use the same alias style in Zinc config:

```yaml
models:
  default: local-llama
  local-llama:
    adapter: responses.adapter
```

Manifest assets form a navigable tree of package files:

```yaml
assets:
  adapter:
    path: adapters/responses.py
  shapes:
    short_answer:
      path: shapes/short-answer.circuitry.yaml
  prompts:
    runtime:
      path: prompts/runtime.md
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

## Package lifecycle

`zn pkg install` runs the package `setup` script for the current platform when one is declared. `zn pkg check <name>` runs the package check script. `zn pkg remove <name>` runs the remove script, then unregisters the package.
