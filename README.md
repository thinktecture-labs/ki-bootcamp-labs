# KI-Bootcamp Labs – Angular Days 2026

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/thinktecture-labs/ki-bootcamp-labs?quickstart=1)

Alle Übungen des Workshops **„KI-Bootcamp: Generative AI für Angular-Entwickler:innen"**
an einem Ort: Python-Labs und Notebooks, die ihr in **GitHub Codespaces** bearbeitet, und die
Links zu den Angular- und JavaScript-Labs auf StackBlitz. Ein Codespace ist eine fertig
eingerichtete Entwicklungsumgebung im Browser: nichts installieren, alles läuft.

Landingpage mit Zeitplan und allen Links: <https://angular-days-2026.brick.do/>

## Voraussetzungen

- **GitHub-Account** für Codespaces (das kostenlose Kontingent reicht für den Workshop)
- Zugang zu [stackblitz.com](https://stackblitz.com/)
- **Langfuse-Account** auf [cloud.langfuse.com](https://cloud.langfuse.com/) mit einem Projekt
  (Public Key `pk-lf-…` und Secret Key `sk-lf-…`)
- **OVH-AI-Endpoints-Key**: wird im Workshop ausgegeben

### Pre-Flight-Check: bitte vor dem Workshop

1. Secrets anlegen wie unten beschrieben (der OVH-Key kann bis zum Workshop fehlen).
2. Codespace über den Badge oben starten.
3. [`python/notebooks/00-preflight.ipynb`](python/notebooks/00-preflight.ipynb) öffnen und
   *Run All* klicken.

> Bitte vorab vom Firmenlaptop aus ausführen. Startet der Codespace nicht oder bleibt beim
> Verbinden hängen, blockiert vermutlich VPN/Proxy: VPN trennen oder Hotspot nutzen.

## In GitHub Codespaces arbeiten

1. **Secrets hinterlegen**, am besten vor dem Start: auf github.com unter
   [*Settings → Codespaces → Secrets*](https://github.com/settings/codespaces) diese Secrets
   anlegen und jeweils für das Repo `thinktecture-labs/ki-bootcamp-labs` freigeben:

   | Secret                | Wert                                                             |
   | --------------------- | ---------------------------------------------------------------- |
   | `OVH_API_KEY`         | OVH-Key aus dem Workshop                                         |
   | `LANGFUSE_PUBLIC_KEY` | `pk-lf-…` aus eurem Langfuse-Projekt                             |
   | `LANGFUSE_SECRET_KEY` | `sk-lf-…` aus eurem Langfuse-Projekt                             |
   | `LANGFUSE_BASE_URL`   | optional, nur für die US-Region: `https://us.cloud.langfuse.com` |

   Beim Start über den Badge fragt Codespaces fehlende Secrets auch direkt ab. Secrets, die ihr
   bei laufendem Codespace anlegt oder ändert, greifen erst nach einem Neustart
   (Befehlspalette: *Codespaces: Stop Current Codespace*, dann neu öffnen).
2. **Codespace öffnen** über den Badge oben oder *Code → Codespaces → Create codespace on main*.
   Einen bestehenden Codespace findet ihr unter <https://github.com/codespaces> wieder.
3. **Notebooks** unter [`python/notebooks/`](python/notebooks/) öffnen; der Kernel
   *Python (notebooks)* ist voreingestellt.
4. **Python-Labs** im Terminal starten:

   ```bash
   cd python/simple-rag-langgraph && uv run main.py
   ```

   bzw. `cd python/simple-rag-langchain && uv run main.py`.

Der Codespace enthält Python 3.14 mit [uv](https://docs.astral.sh/uv/), Node 22, Jupyter und
die VS-Code-Erweiterungen für Python, Ruff und Jupyter. Jedes Python-Projekt hat eine eigene
virtuelle Umgebung und einen eigenen Jupyter-Kernel.

## Labs

Reihenfolge wie im Workshop.

| Lab                      | Wo                                                                                         | Tag/Zeit |
| ------------------------ | ------------------------------------------------------------------------------------------ | -------- |
| Pre-Flight-Check         | [`python/notebooks/00-preflight.ipynb`](python/notebooks/00-preflight.ipynb)               | vorab    |
| LangChainJS Chat         | [StackBlitz](https://stackblitz.com/edit/ki-bootcamp-simple-chat?file=index.js)            | ?        |
| Simple Chat              | [`python/notebooks/01-simple-chat-lab.ipynb`](python/notebooks/01-simple-chat-lab.ipynb)   | ?        |
| Smart Form Filler        | [StackBlitz](https://stackblitz.com/edit/ki-bootcamp-smart-form-filler-lab)                | ?        |
| Embeddings & Vector DB   | [`python/notebooks/02-embeddings-vector-db-lab.ipynb`](python/notebooks/02-embeddings-vector-db-lab.ipynb) | ?        |
| Simple RAG               | [`python/notebooks/03-simple-rag-lab.ipynb`](python/notebooks/03-simple-rag-lab.ipynb)     | ?        |
| Simple RAG mit LangChain | [`python/simple-rag-langchain/`](python/simple-rag-langchain/)                             | ?        |
| Simple RAG mit LangGraph | [`python/simple-rag-langgraph/`](python/simple-rag-langgraph/)                             | ?        |
| Structured Outputs       | [`python/notebooks/04-structured-outputs-lab.ipynb`](python/notebooks/04-structured-outputs-lab.ipynb) | ?        |
| Tool Calling             | [`python/notebooks/05-tool-calling-lab.ipynb`](python/notebooks/05-tool-calling-lab.ipynb) | ?        |
| MCP mit JS               | [StackBlitz](https://stackblitz.com/edit/ki-bootcamp-mcp-client?file=index.js)             | ?        |

Lösungen: Notebooks in [`python/notebooks/`](python/notebooks/README.md), StackBlitz-Lösungen
in [`angular/README.md`](angular/README.md).

## Modelle

Alle Python-Labs nutzen die OpenAI-kompatible API der **OVH AI Endpoints**:

```text
https://oai.endpoints.kepler.ai.cloud.ovh.net/v1
```

| Zweck      | Modell                                | genutzt in                                       |
| ---------- | ------------------------------------- | ------------------------------------------------ |
| Chat       | `Mistral-Small-3.2-24B-Instruct-2506` | beiden RAG-Labs                                  |
| Chat       | `Qwen3.8-27B`                         | `simple-rag-langchain` (Vergleich zu Mistral)    |
| Embeddings | `bge-m3`                              | beiden RAG-Labs, Notebook Embeddings & Vector DB |

## Lokal statt Codespaces

Mit VS Code, Docker und der Erweiterung *Dev Containers* öffnet *Reopen in Container* denselben
Container wie Codespaces. Ohne Container reicht [uv](https://docs.astral.sh/uv/getting-started/installation/):

```bash
cd python/simple-rag-langgraph
cp .env.example .env   # Keys eintragen
uv sync --frozen
uv run main.py
```

In beiden Fällen kommen die Keys aus einer `.env` im jeweiligen Ordner (Vorlage `.env.example`).

## Für Trainer

- Codespaces-Prebuilds für `main` sind nötig, damit ein Codespace in Sekunden statt Minuten
  startet (*Settings → Codespaces → Set up prebuild*).
- Konventionen für Änderungen am Repo stehen in [`CLAUDE.md`](CLAUDE.md).

## Aufbau

```text
.devcontainer/              Dev Container für Codespaces und VS Code
python/
  simple-rag-langchain/     RAG über Bond-Filme mit LangChain, Mistral vs. Qwen, Langfuse-Tracing
  simple-rag-langgraph/     RAG mit LangGraph: Router zwischen Bond und Star Wars, Langfuse-Feedback
  notebooks/                Notebook-Labs und Pre-Flight-Check
angular/                    Links zu den Angular- und JavaScript-Labs auf StackBlitz
```
