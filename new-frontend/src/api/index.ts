import { api, apiBlob } from './client';
import { EP } from './endpoints';
import type * as T from './types';

export const Api = {
  workspaces: () => api<T.Workspace[]>(EP.workspaces),
  createWorkspace: (name: string) => api<unknown>(EP.createWorkspace, { json: { name } }),
  deleteWorkspace: (name: string) => api<unknown>(EP.deleteWorkspace(name)),
  files: (ws: string) => api<T.IndexedFile[]>(EP.files(ws)),
  ingest: (ws: string, files: File[], clear: boolean) => {
    const f = new FormData();
    f.append('workspace', ws); f.append('clear', String(clear));
    files.forEach((x) => f.append('files', x));
    return api<unknown>(EP.ingest, { form: f });
  },
  models: () => api<string[]>(EP.models),
  status: () => api<T.EngineStatus>(EP.status),
  chat: (p: { query: string; workspace: string; focus_file: string | null; persona: string; model: string; multi_hop: boolean; self_rag: boolean }) =>
    api<T.ChatAnswer>(EP.chat, { json: p }),
  tts: (text: string) => apiBlob(EP.tts, { json: { text } }),
  voice: (audio: Blob, p: { workspace: string; model: string; persona: string }) => {
    const f = new FormData();
    f.append('audio', audio, 'turn.webm');
    Object.entries(p).forEach(([k, v]) => f.append(k, v));
    return api<T.VoiceResult>(EP.voice, { form: f });
  },
  crawl: (url: string, workspace: string) => api<{ message?: string }>(EP.crawl, { json: { url, workspace } }),
  mindmap: (workspace: string, file: string | null) => api<{ mermaid: string }>(EP.mindmap, { json: { workspace, file } }),
  topics: (workspace: string) => api<{ clusters: T.Cluster[] }>(EP.topics, { json: { workspace } }),
  translate: (text: string, language: string) => api<{ translation: string }>(EP.translate, { json: { text, language } }),
  battle: (p: { model_a: string; model_b: string; question: string; workspace: string }) => api<T.BattleResult>(EP.battle, { json: p }),
  quiz: (workspace: string) => api<{ questions: string[] }>(EP.quiz, { json: { workspace } }),
  sql: (database: string, question: string, workspace: string) => api<T.SqlResult>(EP.sql, { json: { database, question, workspace } }),
  redact: (text: string) => api<{ redacted: string }>(EP.redact, { json: { text } }),
  inspect: (workspace: string, file: string) => api<{ chunks: T.DocChunk[] }>(EP.inspect, { json: { workspace, file } }),
  compare: (workspace: string, a: string, b: string) => api<{ summary: string }>(EP.compare, { json: { workspace, file_a: a, file_b: b } }),
  sessions: (ws: string) => api<string[]>(EP.sessions(ws)),
  saveSession: (workspace: string, name: string, messages: T.Message[]) => api<unknown>(EP.saveSession, { json: { workspace, name, messages } }),
  loadSession: (ws: string, name: string) => api<{ messages: T.Message[] }>(EP.loadSession(ws, name)),
  brief: (workspace: string) => api<{ markdown: string }>(EP.briefExport, { json: { workspace } }),
  deck: (workspace: string) => apiBlob(EP.deckExport, { json: { workspace } }),
};
