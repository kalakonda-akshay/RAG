# Archive / Orbit — Frontend

React 18 + TypeScript + Vite. 3-rail layout (Knowledge · Q&A workspace · Grounding), 12 feature tabs, exactly per spec.
Only runtime dependencies: `react`, `react-dom`, `mermaid` (lazy-loaded for the Mind Map tab).

## Run
```bash
npm install
cp .env.example .env      # set VITE_BACKEND_URL to your backend (default http://localhost:8000)
npm run dev               # http://localhost:5173  (proxies /api -> backend)
npm run build             # type-check + production build into dist/
```

## ⚠ Backend contract — READ THIS FIRST
The backend source/API docs were not provided, so the HTTP routes and JSON shapes are an **assumed contract**.
**All of them live in one file: `src/api/endpoints.ts`** (field names in `src/api/types.ts`).
Compare each route to your real backend and edit only those two files — no component hardcodes a URL.
Until they match, the UI shows the "Backend unreachable" banner / inline error messages instead of fake data.

If your backend is Streamlit (no REST API), you will need a thin HTTP layer exposing these functions.

## Structure
```
src/api/         endpoints.ts (contract) · client.ts (fetch, errors, GET retry) · index.ts (typed calls)
src/state/       AppContext.tsx (workspace, files, settings, chat, grounding rail, toasts)
src/components/  Sidebar · Center · GroundingRail · ui.tsx · tabs/ (Chat, Voice, + 10 tool tabs)
```
Citation badges `[n]` in an answer highlight and scroll to the matching card in the right rail. Below 900px the side rails become slide-over drawers.
