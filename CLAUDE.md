# ki-bootcamp-labs

Participant exercises for the KI-Bootcamp at Angular Days 2026 (Thinktecture). Participant-facing
text (READMEs, notebooks) is **German**; code comments and this file are English.

Remote: `git@github.com:thinktecture-labs/ki-bootcamp-labs.git`. Do not push or change repo
settings without asking Felix.

## Structure

- `python/<lab>/`: one uv project per lab (`pyproject.toml`, `uv.lock`, `.python-version` 3.14,
  `.env.example`). Run from the lab's folder.
- `python/notebooks/`: notebook labs (originally Colab notebooks from Google Drive, converted to
  run in Codespaces), plus a uv project that is their kernel ("Python (notebooks)") and runs the
  notebook tests. `00-preflight.ipynb` is the participants' pre-workshop check.
- `angular/`: links only; the Angular/JS labs live on StackBlitz and in their own repos.
- `.devcontainer/`: one container for everything; Codespaces is the participants' primary
  environment. `post-create.sh` syncs every `python/*/pyproject.toml` and registers a kernel each.

## Running and testing

```bash
cd python/simple-rag-langgraph && uv sync --frozen && uv run main.py   # same for the other labs
cd python/notebooks && uv run pytest    # live OVH test skips without OVH_API_KEY
npx --yes @devcontainers/cli@latest up --workspace-folder .            # build the dev container
```

After changing `.devcontainer/` or a lock file, rebuild with the devcontainer CLI and check inside
it (`devcontainer exec --workspace-folder . bash -lc '…'`): `uv run python -m py_compile main.py`
per lab, the imports, `node --version`, the kernels in `~/.local/share/jupyter/kernels`. Remove
the test container and its `vsc-ki-bootcamp-labs-*` image afterwards, and delete the
`python/*/.venv-devcontainer` folders it leaves in the bind-mounted workspace.

## Rules

- **Never commit `.env`** or real keys. Each lab has a `.env.example`; Codespaces gets the keys as
  secrets declared in `devcontainer.json`.
- **Container venvs never use `.venv`.** `UV_PROJECT_ENVIRONMENT=.venv-devcontainer` keeps each
  lab's Linux venv apart from the host's `.venv`, which a local bind mount would otherwise
  overwrite. Do not set it to `.venv` and do not add a venv at the repo root.
- Keep lock files frozen-installable: change dependencies with `uv add`/`uv lock` in the lab's
  folder and commit `uv.lock` with `pyproject.toml`.
- Notebooks are Codespaces-first: keys via `load_dotenv()` + `os.environ["OVH_API_KEY"]`, never
  `google.colab`; no `pip install` cells (add packages with `uv add` in `python/notebooks`);
  kernelspec `notebooks`; no stored outputs. `uv run pytest` there enforces all of this. Keep the
  lab notebooks' `...` placeholders and `Task:` hints intact.
- Models (OVH AI Endpoints, `https://oai.endpoints.kepler.ai.cloud.ovh.net/v1`):
  `Mistral-Small-3.2-24B-Instruct-2506`, `Qwen3.8-27B`, embeddings `bge-m3`. Keep README tables in
  sync when a model changes.
- Conventional commits (`feat:`, `fix:`, `chore:`, `docs:`), small commits, no attribution lines.
  Prettier is not set up; keep Markdown tidy by hand.
