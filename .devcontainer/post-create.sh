#!/usr/bin/env bash
# postCreateCommand of the dev container (see devcontainer.json). Runs once as user "vscode"
# after the container is created – in GitHub Codespaces ideally during a prebuild.
set -euo pipefail
cd "$(dirname "$0")/.."

# uv manages the Python projects; pipx ships with the Python dev container image.
command -v uv >/dev/null 2>&1 || pipx install uv

# One virtualenv per uv project under python/ (at python/<project>/.venv-devcontainer, see
# UV_PROJECT_ENVIRONMENT in devcontainer.json) plus a Jupyter kernel for each of them.
for dir in python/*/; do
  [ -f "$dir/pyproject.toml" ] || continue
  name=$(basename "$dir")
  echo "==> $name"
  (
    cd "$dir"
    uv sync --frozen
    uv run --frozen python -m ipykernel install --user --name "$name" --display-name "Python ($name)"
  )
done

echo "==> Jupyter kernels:"
ls ~/.local/share/jupyter/kernels
