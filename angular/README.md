# Angular- und JavaScript-Labs (StackBlitz)

Die Angular- und JavaScript-Labs laufen im Browser auf [StackBlitz](https://stackblitz.com/),
ohne lokale Installation. Die Quellen bleiben vorerst in ihren eigenen Repos; dieses Verzeichnis
sammelt nur die Links.

| Lab                | Lab                                                                                | Lösung                                                                                 | Quellen                                                                         |
| ------------------ | ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| LangChainJS Chat   | [StackBlitz](https://stackblitz.com/edit/ki-bootcamp-simple-chat?file=index.js)    | [StackBlitz](https://stackblitz.com/edit/ki-bootcamp-simple-chat?file=solution.js)     | nur StackBlitz                                                                  |
| Smart Form Filler  | [StackBlitz](https://stackblitz.com/edit/ki-bootcamp-smart-form-filler-lab)        | [StackBlitz](https://stackblitz.com/edit/ki-bootcamp-smart-form-filler)                | [thinktecture-labs/smart-form-filler](https://github.com/thinktecture-labs/smart-form-filler) |
| MCP mit JS         | [StackBlitz](https://stackblitz.com/edit/ki-bootcamp-mcp-client?file=index.js)     | [StackBlitz](https://stackblitz.com/edit/ki-bootcamp-mcp-client?file=solution.js)      | nur StackBlitz                                                                  |

Beim LangChainJS Chat und beim MCP-Client liegen Lab und Lösung im selben StackBlitz-Projekt:
`index.js` ist das Lab, `solution.js` die Lösung.

## Showcase: ACME Coding Guideline Portal (Tag 2)

Das Portal aus der Demo ist kein Lab, die Quellen sind aber öffentlich:

- Backend (LangGraph): [thinktecture-labs/angulardays-2024-langgraph](https://github.com/thinktecture-labs/angulardays-2024-langgraph)
- Frontend (Angular): [thinktecture-labs/rag-client](https://github.com/thinktecture-labs/rag-client)

## Wenn StackBlitz blockiert ist

StackBlitz braucht WebContainers (Service Worker, `*.webcontainer.io`), was manche
Firmen-Proxys blockieren. Fallback: dieses Repo in GitHub Codespaces öffnen (Node 22 ist
installiert), das StackBlitz-Projekt dort herunterladen (`Download Project` in StackBlitz)
oder das Quell-Repo klonen und mit `npm install && npm start` starten.
