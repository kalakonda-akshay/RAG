/**
 * ─────────────────────────────────────────────────────────────────────────
 *  BACKEND CONTRACT — SINGLE SOURCE OF TRUTH
 * ─────────────────────────────────────────────────────────────────────────
 *  The backend source/API docs were NOT supplied when this frontend was built,
 *  so these routes and payload shapes are an ASSUMED contract (nothing else in
 *  the app hardcodes a URL). Compare each line to your real backend routes and
 *  edit ONLY this file (and src/api/types.ts if field names differ).
 *  Every call is relative to VITE_API_BASE_URL (default "/api").
 */
export const EP = {
  workspaces:        { method: 'GET',    path: '/workspaces' },                 // -> Workspace[]
  createWorkspace:   { method: 'POST',   path: '/workspaces' },                 // {name}
  deleteWorkspace:   (n: string) => ({ method: 'DELETE', path: `/workspaces/${encodeURIComponent(n)}` }),
  files:             (ws: string) => ({ method: 'GET', path: `/workspaces/${encodeURIComponent(ws)}/files` }), // -> IndexedFile[]
  ingest:            { method: 'POST',   path: '/ingest' },                     // multipart: workspace, clear, files[]
  models:            { method: 'GET',    path: '/models' },                      // -> string[] (Ollama)
  status:            { method: 'GET',    path: '/status' },                      // -> {cpu_percent, ram_percent}
  chat:              { method: 'POST',   path: '/chat' },                        // -> ChatAnswer
  tts:               { method: 'POST',   path: '/tts' },                         // {text} -> audio/wav
  voice:             { method: 'POST',   path: '/voice' },                       // multipart audio -> VoiceResult
  crawl:             { method: 'POST',   path: '/crawl' },                       // {url, workspace}
  mindmap:           { method: 'POST',   path: '/mindmap' },                     // -> {mermaid}
  topics:            { method: 'POST',   path: '/topics' },                      // -> {clusters: Cluster[]}
  translate:         { method: 'POST',   path: '/translate' },                   // {text, language} -> {translation}
  battle:            { method: 'POST',   path: '/battle' },                      // {model_a, model_b, question, workspace}
  quiz:              { method: 'POST',   path: '/quiz' },                        // -> {questions: string[]}
  sql:               { method: 'POST',   path: '/sql' },                         // {database, question} -> SqlResult
  redact:            { method: 'POST',   path: '/redact' },                      // {text} -> {redacted}
  inspect:           { method: 'POST',   path: '/inspect' },                     // {workspace, file} -> {chunks}
  compare:           { method: 'POST',   path: '/compare' },                     // {workspace, file_a, file_b} -> {summary}
  sessions:          (ws: string) => ({ method: 'GET', path: `/sessions?workspace=${encodeURIComponent(ws)}` }), // -> string[]
  saveSession:       { method: 'POST',   path: '/sessions' },                    // {workspace, name, messages}
  loadSession:       (ws: string, name: string) => ({ method: 'GET', path: `/sessions/${encodeURIComponent(name)}?workspace=${encodeURIComponent(ws)}` }), // -> {messages}
  briefExport:       { method: 'POST',   path: '/export/brief' },                // -> {markdown}
  deckExport:        { method: 'POST',   path: '/export/deck' },                 // -> .pptx blob
} as const;
