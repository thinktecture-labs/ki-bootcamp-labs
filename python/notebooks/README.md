# Notebooks (Google Colab)

Die Notebook-Labs laufen im Workshop in [Google Colab](https://colab.research.google.com/).
Dieses Verzeichnis enthält die `.ipynb`-Dateien als Export aus Google Drive, damit sie
versioniert sind und als Fallback in GitHub Codespaces laufen.

## Pre-Flight-Check (bitte vor dem Workshop)

[`00-preflight.ipynb`](00-preflight.ipynb) ist ein winziges Notebook, das ihr vorab in Colab
ausführt. Es installiert LangChain, gibt die Versionen aus und prüft, ob die OVH AI Endpoints
erreichbar sind.

> Bitte vorab vom Firmenlaptop aus ausführen. Bleibt die Zelle bei „Verbinden" hängen,
> blockiert vermutlich VPN/Proxy: VPN trennen oder Hotspot nutzen; Fallback: dieses Repo in
> GitHub Codespaces öffnen.

Öffnen in Colab: `Datei → Notebook öffnen → GitHub` und die Repo-URL eingeben, oder direkt
über `https://colab.research.google.com/github/<org>/ki-bootcamp-labs/blob/main/python/notebooks/00-preflight.ipynb`
(funktioniert, sobald das Repo öffentlich auf GitHub liegt).

## Erwartete Notebooks

Export aus Google Drive: Notebook in Colab öffnen → `Datei → Herunterladen → .ipynb herunterladen`
und hier unter dem angegebenen Namen ablegen. Lab und Lösung jeweils als eigene Datei, Ausgaben
vorher löschen (`Bearbeiten → Alle Ausgaben löschen`). ✅ = liegt bereits im Repo.

| Nr. | Notebook                         | Dateien (Lab / Lösung)                                                       | Colab (Stand Landingpage)                                                                                                                                                                                                 |
| --- | -------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 00  | Pre-Flight-Check                 | `00-preflight.ipynb`                                                         | –                                                                                                                                                                                                                         |
| 01  | LangChain Chat                   | `01-langchain-chat-lab.ipynb` / `01-langchain-chat-solution.ipynb`           | [Lab](https://colab.research.google.com/drive/1qIYradSffWokv6jaf-bKGcR9atIlquEC) / [Lösung](https://colab.research.google.com/drive/1a6QQm5AGzPfLT2WpEWaB03S4e3AbH2ba)                                                   |
| 02  | Embeddings & Vector DB           | `02-embeddings-vector-db-lab.ipynb` ✅ / `02-embeddings-vector-db-solution.ipynb` | [Lab](https://colab.research.google.com/drive/1jL5Hs32tsz9vFXK_7FUCWnqNBG4DRSf3?usp=sharing) / [Lösung](https://colab.research.google.com/drive/1wsxwuYWld4bofdGfRXCgpSYhkATx81QV?usp=sharing)                           |
| 03  | Simple RAG                       | `03-simple-rag-lab.ipynb` / `03-simple-rag-solution.ipynb`                   | [Lab](https://colab.research.google.com/drive/1LTkYobIbHRYF6A4g4ZFnGzgZTx5rURXa?usp=sharing) / [Lösung](https://colab.research.google.com/drive/1RtM86AzXEfVErPYyf9RasHlUcXOj2W6u?usp=sharing)                           |
| 04  | Structured Outputs mit LangChain | `04-structured-outputs-lab.ipynb` / `04-structured-outputs-solution.ipynb`   | [Lab](https://colab.research.google.com/drive/1UeilbVoQ0PF6EfJ9yq6mw2PNisLMYZuN?usp=sharing) / [Lösung](https://colab.research.google.com/drive/1b8qrMBXxKau2R3Xlrkq7v4hPQsXMnjav?usp=sharing)                           |
| 05  | Tool Calling                     | `05-tool-calling-lab.ipynb` / `05-tool-calling-solution.ipynb`               | [Lab](https://colab.research.google.com/drive/1S6GZd5Jn6g_a8zviF8xCsx9I2hSahGk0?usp=sharing) / [Lösung](https://colab.research.google.com/drive/1z3GRLNeuEo07vOB-ZiMX32ApfwcS3uV-?usp=sharing)                           |
| –   | LangChain Chat-Loop (OpenRouter) | `langchain-chat-loop-openrouter.ipynb` (optional, ggf. obsolet: Provider ist OVH) | [Notebook](https://colab.research.google.com/drive/1a_S-SS1bM1PJpz2xVWfZaJRyXzKmzEeJ?usp=sharing)                                                                                                                      |

Die Colab-Links stammen von der [Landingpage](https://angular-days-2026.brick.do/); bitte vor
dem Workshop gegen Google Drive prüfen (die Folien nennen für „Tool Calling“ eine andere Lösung
und für „Simple RAG“ einen zweiten Link).

## In Codespaces statt Colab

Im Dev Container ist ein Jupyter-Kernel **„Python (notebooks)“** registriert, dessen Umgebung
aus [`pyproject.toml`](pyproject.toml) kommt: LangChain, LangGraph, Langfuse und `pip`, damit
die `%pip install …`-Zellen der Colab-Notebooks auch hier funktionieren.

1. Notebook in VS Code öffnen, oben rechts den Kernel „Python (notebooks)“ wählen.
2. Secrets kommen aus den Codespaces-Secrets (`OVH_API_KEY`, Langfuse-Keys), siehe
   [README im Repo-Root](../../README.md). In Colab liegen sie stattdessen unter 🔑 *Secrets*;
   der OVH-Token heißt dort `OVH_AI_ENDPOINTS_ACCESS_TOKEN`.
3. Zellen wie in Colab ausführen. Colab-spezifisches muss ersetzt werden:
   `userdata.get("OVH_AI_ENDPOINTS_ACCESS_TOKEN")` → `os.environ["OVH_API_KEY"]`
   (und `from google.colab import userdata` → `import os`).

Lokal ohne Container: `uv sync --frozen` in diesem Ordner und den Kernel mit
`uv run python -m ipykernel install --user --name notebooks` registrieren.

## Tests

```bash
uv run pytest
```

- **Alle Notebooks:** gültiges nbformat, jede Code-Zelle kompiliert (`%pip`/`!pip` inklusive,
  Platzhalter `...` sind erlaubt), keine gespeicherten Ausgaben.
- **Embeddings & Vector DB:** Lab behält seine `Task:`-Platzhalter, nutzt LangChain + Qdrant und
  den Colab-Secret-Namen, Demo-Daten sind die 17 Bond-Filme. Ein Live-Test baut die Lösung gegen
  OVH (`bge-m3`, Qdrant in-memory) und prüft die Lab-Fragen. Er läuft nur mit `OVH_API_KEY`
  (Codespaces-Secret oder `.env` hier im Ordner, siehe [`.env.example`](.env.example)) und wird
  sonst übersprungen.
