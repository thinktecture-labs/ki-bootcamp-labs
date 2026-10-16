# Notebooks

Die Notebook-Labs laufen im Codespace dieses Repos in VS Code. Alle Bibliotheken sind
vorinstalliert, die Keys kommen aus euren Codespaces-Secrets (siehe
[README im Repo-Root](../../README.md#in-github-codespaces-arbeiten)).

1. Notebook öffnen. Der Kernel *Python (notebooks)* ist voreingestellt; fragt VS Code trotzdem,
   diesen auswählen.
2. Zellen der Reihe nach ausführen (`Shift+Enter`) und die Stellen mit `...` bzw. `Task:` ergänzen.
3. Die Notebooks lesen den OVH-Key mit `os.environ["OVH_API_KEY"]`. Lokal ohne Codespace legt
   ihr dafür eine `.env` in diesem Ordner an (Vorlage: [`.env.example`](.env.example)).

## Pre-Flight-Check (bitte vor dem Workshop)

[`00-preflight.ipynb`](00-preflight.ipynb) prüft die Umgebung, eure Secrets und den Zugriff auf
die OVH AI Endpoints. Erwartet werden drei Zeilen mit ✅; den OVH-Key bekommt ihr erst im
Workshop, bis dahin wird dieser Check übersprungen.

> Bitte vorab vom Firmenlaptop aus ausführen. Startet der Codespace nicht oder bleibt beim
> Verbinden hängen, blockiert vermutlich VPN/Proxy: VPN trennen oder Hotspot nutzen.

## Notebooks

| Nr. | Notebook                         | Lab                                                                         | Lösung                                     |
| --- | -------------------------------- | --------------------------------------------------------------------------- | ------------------------------------------ |
| 00  | Pre-Flight-Check                 | [`00-preflight.ipynb`](00-preflight.ipynb)                                  | –                                          |
| 01  | LangChain Chat                   | `01-langchain-chat-lab.ipynb` (folgt)                                       | `01-langchain-chat-solution.ipynb`         |
| 02  | Embeddings & Vector DB           | [`02-embeddings-vector-db-lab.ipynb`](02-embeddings-vector-db-lab.ipynb)    | `02-embeddings-vector-db-solution.ipynb`   |
| 03  | Simple RAG                       | [`03-simple-rag-lab.ipynb`](03-simple-rag-lab.ipynb)                        | `03-simple-rag-solution.ipynb`             |
| 04  | Structured Outputs mit LangChain | [`04-structured-outputs-lab.ipynb`](04-structured-outputs-lab.ipynb)        | `04-structured-outputs-solution.ipynb`     |
| 05  | Tool Calling                     | [`05-tool-calling-lab.ipynb`](05-tool-calling-lab.ipynb)                    | `05-tool-calling-solution.ipynb`           |

## Für Trainer: Notebooks aus Colab übernehmen

Die Originale liegen als Colab-Notebooks in Google Drive (Links auf der
[Landingpage](https://angular-days-2026.brick.do/)). Pro Notebook:

1. In Colab `Datei → Herunterladen → .ipynb herunterladen`, unter dem Namen aus der Tabelle hier
   ablegen.
2. `from google.colab import userdata` und `userdata.get("OVH_AI_ENDPOINTS_ACCESS_TOKEN")`
   ersetzen durch `import os`, `from dotenv import load_dotenv`, `load_dotenv()` und
   `os.environ["OVH_API_KEY"]`.
3. `!pip install …`-Zellen löschen; fehlende Pakete stattdessen mit `uv add <paket>` in diesem
   Ordner ergänzen.
4. Ausgaben löschen und als Kernel `notebooks` eintragen (Metadaten `kernelspec`).
5. `uv run pytest` ausführen: Die Tests prüfen genau diese Punkte.

## Tests

```bash
uv run pytest
```

- **Alle Notebooks:** gültiges nbformat, jede Code-Zelle kompiliert (Platzhalter `...` sind
  erlaubt), keine gespeicherten Ausgaben, kein `google.colab`, kein `pip install`, Kernel
  `notebooks`.
- **Embeddings & Vector DB:** Lab behält seine `Task:`-Platzhalter, nutzt LangChain + Qdrant und
  `OVH_API_KEY`, Demo-Daten sind die 17 Bond-Filme. Ein Live-Test baut die Lösung gegen OVH
  (`bge-m3`, Qdrant in-memory) und prüft die Lab-Fragen. Er läuft nur mit `OVH_API_KEY`
  (Codespaces-Secret oder `.env` hier im Ordner) und wird sonst übersprungen.
