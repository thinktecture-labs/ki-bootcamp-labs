# KI-Bootcamp Labs – Angular Days 2026

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/thinktecture-labs/ki-bootcamp-labs?quickstart=1)

Alle Übungen des Workshops **„KI-Bootcamp: Generative AI für Angular-Entwickler:innen"**
an einem Ort: Python-Labs, Colab-Notebooks und die Links zu den Angular-/JavaScript-Labs auf
StackBlitz. Dazu ein Dev Container, damit alles auch in **GitHub Codespaces** läuft – der
Fallback, falls euer Firmen-VPN oder -Proxy Google Colab blockiert.

Landingpage mit Zeitplan und allen Links: <https://angular-days-2026.brick.do/>

## Voraussetzungen

- **Google-Account** und Zugang zu [colab.research.google.com](https://colab.research.google.com/)
- Zugang zu [stackblitz.com](https://stackblitz.com/)
- **Langfuse-Account** auf [cloud.langfuse.com](https://cloud.langfuse.com/) mit einem Projekt
  (Public Key `pk-lf-…` und Secret Key `sk-lf-…`)
- **OVH-AI-Endpoints-Key**: wird im Workshop ausgegeben
- Optional für den Fallback: GitHub-Account (Codespaces ist im Free-Kontingent enthalten)

### Pre-Flight-Check: bitte vor dem Workshop

Öffnet [`python/notebooks/00-preflight.ipynb`](python/notebooks/00-preflight.ipynb) in Colab und
führt es aus. Erwartet wird am Ende `OK ✅`.

> Bitte vorab vom Firmenlaptop aus ausführen. Bleibt die Zelle bei „Verbinden" hängen,
> blockiert vermutlich VPN/Proxy: VPN trennen oder Hotspot nutzen; Fallback: dieses Repo in
> GitHub Codespaces öffnen.

## Labs

Reihenfolge wie im Workshop. Die Notebooks werden nach und nach aus Google Drive exportiert,
siehe [`python/notebooks/README.md`](python/notebooks/README.md).

| Lab                         | Wo                                                                                                                                                                     | Pfad im Repo                                                                                      | Tag/Zeit |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | -------- |
| Pre-Flight-Check            | Colab                                                                                                                                                                  | [`python/notebooks/00-preflight.ipynb`](python/notebooks/00-preflight.ipynb)                      | vorab    |
| LangChainJS Chat            | [StackBlitz](https://stackblitz.com/edit/ki-bootcamp-simple-chat?file=index.js)                                                                                        | [`angular/`](angular/README.md)                                                                   | ?        |
| LangChain Chat              | [Colab](https://colab.research.google.com/drive/1qIYradSffWokv6jaf-bKGcR9atIlquEC)                                                                                     | `python/notebooks/01-langchain-chat-lab.ipynb` (folgt)                                            | ?        |
| Smart Form Filler           | [StackBlitz](https://stackblitz.com/edit/ki-bootcamp-smart-form-filler-lab)                                                                                            | [`angular/`](angular/README.md)                                                                   | ?        |
| Embeddings & Vector DB      | [Colab](https://colab.research.google.com/drive/1jL5Hs32tsz9vFXK_7FUCWnqNBG4DRSf3?usp=sharing)                                                                         | [`python/notebooks/02-embeddings-vector-db-lab.ipynb`](python/notebooks/02-embeddings-vector-db-lab.ipynb) | ?        |
| Simple RAG                  | [Colab](https://colab.research.google.com/drive/1LTkYobIbHRYF6A4g4ZFnGzgZTx5rURXa?usp=sharing)                                                                         | `python/notebooks/03-simple-rag-lab.ipynb` (folgt)                                                | ?        |
| Simple RAG mit LangChain    | Codespaces / lokal                                                                                                                                                     | [`python/simple-rag-langchain/`](python/simple-rag-langchain/)                                    | ?        |
| Simple RAG mit LangGraph    | Codespaces / lokal                                                                                                                                                     | [`python/simple-rag-langgraph/`](python/simple-rag-langgraph/)                                    | ?        |
| Structured Outputs          | [Colab](https://colab.research.google.com/drive/1UeilbVoQ0PF6EfJ9yq6mw2PNisLMYZuN?usp=sharing)                                                                         | `python/notebooks/04-structured-outputs-lab.ipynb` (folgt)                                        | ?        |
| Tool Calling                | [Colab](https://colab.research.google.com/drive/1S6GZd5Jn6g_a8zviF8xCsx9I2hSahGk0?usp=sharing)                                                                         | `python/notebooks/05-tool-calling-lab.ipynb` (folgt)                                              | ?        |
| MCP mit JS                  | [StackBlitz](https://stackblitz.com/edit/ki-bootcamp-mcp-client?file=index.js)                                                                                         | [`angular/`](angular/README.md)                                                                   | ?        |

Die Lösungen stehen jeweils daneben: Colab-Lösungen in
[`python/notebooks/README.md`](python/notebooks/README.md), StackBlitz-Lösungen in
[`angular/README.md`](angular/README.md).

## Modelle

Alle Python-Labs nutzen die OpenAI-kompatible API der **OVH AI Endpoints**:

```text
https://oai.endpoints.kepler.ai.cloud.ovh.net/v1
```

| Zweck      | Modell                               | genutzt in                                   |
| ---------- | ------------------------------------ | -------------------------------------------- |
| Chat       | `Mistral-Small-3.2-24B-Instruct-2506` | beiden RAG-Labs                              |
| Chat       | `Qwen3.8-27B`                        | `simple-rag-langchain` (Vergleich zu Mistral) |
| Embeddings | `bge-m3`                             | beiden RAG-Labs, Notebook Embeddings & Vector DB |

## In GitHub Codespaces arbeiten

1. **Secrets hinterlegen**, bevor ihr den Codespace startet: auf github.com unter
   *Settings → Codespaces → Secrets* (für euren Account) diese Secrets anlegen und für das Repo
   `thinktecture-labs/ki-bootcamp-labs` freigeben:

   | Secret                | Wert                                                                 |
   | --------------------- | -------------------------------------------------------------------- |
   | `OVH_API_KEY`         | OVH-Key aus dem Workshop                                             |
   | `LANGFUSE_PUBLIC_KEY` | `pk-lf-…` aus eurem Langfuse-Projekt                                 |
   | `LANGFUSE_SECRET_KEY` | `sk-lf-…` aus eurem Langfuse-Projekt                                 |
   | `LANGFUSE_BASE_URL`   | optional, nur für die US-Region: `https://us.cloud.langfuse.com`     |

   Beim Start über den Badge fragt Codespaces fehlende Secrets auch direkt ab. Secrets, die ihr
   erst bei laufendem Codespace anlegt, greifen nach einem Neustart des Codespaces.
2. **Codespace öffnen** über den Badge oben oder *Code → Codespaces → Create codespace on main*.
   Beim ersten Start installiert der Container alle Abhängigkeiten (`.devcontainer/post-create.sh`).
3. **Lab starten** im Terminal:

   ```bash
   cd python/simple-rag-langgraph && uv run main.py
   ```

   bzw. `cd python/simple-rag-langchain && uv run main.py`.
4. **Notebooks** öffnen und oben rechts den Kernel *Python (notebooks)* wählen. Details in
   [`python/notebooks/README.md`](python/notebooks/README.md).

Der Dev Container enthält Python 3.14 mit [uv](https://docs.astral.sh/uv/), Node 22, Jupyter
und die VS-Code-Erweiterungen für Python, Ruff und Jupyter. Jedes Python-Projekt hat eine
eigene virtuelle Umgebung und einen eigenen Jupyter-Kernel.

**Für die Trainer:** Codespaces-Prebuilds für `main` im Repo aktivieren (*Settings → Codespaces →
Set up prebuild*), sonst dauert der erste Start mehrere Minuten statt Sekunden.

## Lokal arbeiten

Ohne Container reicht [uv](https://docs.astral.sh/uv/getting-started/installation/):

```bash
cd python/simple-rag-langgraph
cp .env.example .env   # Keys eintragen
uv sync --frozen
uv run main.py
```

Mit VS Code und der Erweiterung *Dev Containers* öffnet *Reopen in Container* denselben
Container wie Codespaces; die Keys kommen dann aus der `.env` im jeweiligen Lab-Ordner.

## Aufbau

```text
.devcontainer/              Dev Container für Codespaces und VS Code
python/
  simple-rag-langchain/     RAG über Bond-Filme mit LangChain, Mistral vs. Qwen, Langfuse-Tracing
  simple-rag-langgraph/     RAG mit LangGraph: Router zwischen Bond und Star Wars, Langfuse-Feedback
  notebooks/                Colab-Notebooks (Export aus Google Drive) und Pre-Flight-Check
angular/                    Links zu den Angular- und JavaScript-Labs auf StackBlitz
```
