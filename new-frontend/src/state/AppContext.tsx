import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState, type ReactNode } from 'react';
import { Api } from '../api';
import type { EngineStatus, IndexedFile, Message, Settings, SourcePassage, Workspace } from '../api/types';
import { ALL_DOCS, PERSONAS, PRESET_WORKSPACES } from '../constants';

export interface Toast { id: number; kind: 'ok' | 'err' | 'info'; text: string }

interface Ctx {
  workspaces: Workspace[]; active: string; setActive: (w: string) => void;
  files: IndexedFile[]; models: string[]; status: EngineStatus | null; backendUp: boolean | null;
  settings: Settings; setSettings: (p: Partial<Settings>) => void;
  messages: Message[]; setMessages: (m: Message[]) => void; busy: boolean;
  ask: (q: string) => Promise<void>;
  railSources: SourcePassage[]; railQuery: string; activeCite: number | null; setActiveCite: (n: number | null) => void;
  showSources: (m: Message) => void;
  refresh: () => Promise<void>;
  toasts: Toast[]; toast: (kind: Toast['kind'], text: string) => void;
}

const C = createContext<Ctx | null>(null);
export const useApp = () => { const c = useContext(C); if (!c) throw new Error('useApp outside provider'); return c; };

const msg = (e: unknown) => (e instanceof Error ? e.message : String(e));
let uid = 0;

export function AppProvider({ children }: { children: ReactNode }) {
  const [workspaces, setWorkspaces] = useState<Workspace[]>([]);
  const [active, setActiveWs] = useState(PRESET_WORKSPACES[0]);
  const [files, setFiles] = useState<IndexedFile[]>([]);
  const [models, setModels] = useState<string[]>([]);
  const [status, setStatus] = useState<EngineStatus | null>(null);
  const [backendUp, setBackendUp] = useState<boolean | null>(null);
  const [settings, setS] = useState<Settings>({ persona: PERSONAS[0], model: '', multiHop: true, selfRag: true, focusFile: ALL_DOCS });
  const [messages, setMessages] = useState<Message[]>([]);
  const [busy, setBusy] = useState(false);
  const [railSources, setRailSources] = useState<SourcePassage[]>([]);
  const [railQuery, setRailQuery] = useState('');
  const [activeCite, setActiveCite] = useState<number | null>(null);
  const [toasts, setToasts] = useState<Toast[]>([]);
  const wsRef = useRef(active); wsRef.current = active;

  const toast = useCallback((kind: Toast['kind'], text: string) => {
    const id = ++uid;
    setToasts((t) => [...t, { id, kind, text }]);
    setTimeout(() => setToasts((t) => t.filter((x) => x.id !== id)), 4500);
  }, []);

  const setSettings = useCallback((p: Partial<Settings>) => setS((s) => ({ ...s, ...p })), []);

  const loadWorkspaces = useCallback(async () => {
    try {
      const list = await Api.workspaces();
      const names = new Set(list.map((w) => w.name));
      const merged = [...PRESET_WORKSPACES.filter((p) => !names.has(p)).map((p) => ({ name: p, doc_count: 0, custom: false })), ...list];
      setWorkspaces(merged); setBackendUp(true);
    } catch (e) {
      setBackendUp(false);
      setWorkspaces(PRESET_WORKSPACES.map((p) => ({ name: p, doc_count: 0, custom: false })));
      toast('err', msg(e));
    }
  }, [toast]);

  const loadFiles = useCallback(async (ws: string) => {
    try { setFiles(await Api.files(ws)); } catch { setFiles([]); }
  }, []);

  const refresh = useCallback(async () => { await loadWorkspaces(); await loadFiles(wsRef.current); }, [loadWorkspaces, loadFiles]);

  useEffect(() => { void loadWorkspaces(); }, [loadWorkspaces]);
  useEffect(() => { void loadFiles(active); setSettings({ focusFile: ALL_DOCS }); setMessages([]); setRailSources([]); setActiveCite(null); }, [active, loadFiles, setSettings]);
  useEffect(() => {
    Api.models().then((m) => { setModels(m); setS((s) => ({ ...s, model: s.model || m[0] || '' })); }).catch(() => setModels([]));
  }, []);
  useEffect(() => {
    let live = true;
    const tick = () => Api.status().then((s) => live && setStatus(s)).catch(() => live && setStatus(null));
    tick(); const id = setInterval(tick, 5000);
    return () => { live = false; clearInterval(id); };
  }, []);

  const showSources = useCallback((m: Message) => { setRailSources(m.sources ?? []); setRailQuery(m.query ?? ''); setActiveCite(null); }, []);

  const ask = useCallback(async (q: string) => {
    const text = q.trim(); if (!text || busy) return;
    const user: Message = { id: `u${++uid}`, role: 'user', text };
    const pid = `a${++uid}`;
    setMessages((m) => [...m, user, { id: pid, role: 'assistant', text: '', pending: true, query: text }]);
    setBusy(true);
    try {
      const r = await Api.chat({
        query: text, workspace: wsRef.current,
        focus_file: settings.focusFile === ALL_DOCS ? null : settings.focusFile,
        persona: settings.persona, model: settings.model, multi_hop: settings.multiHop, self_rag: settings.selfRag,
      });
      const done: Message = { id: pid, role: 'assistant', text: r.answer, sources: r.sources, verified: r.verified, query: text };
      setMessages((m) => m.map((x) => (x.id === pid ? done : x)));
      showSources(done);
    } catch (e) {
      setMessages((m) => m.map((x) => (x.id === pid ? { ...x, pending: false, text: '', error: msg(e) } : x)));
    } finally { setBusy(false); }
  }, [busy, settings, showSources]);

  const value = useMemo<Ctx>(() => ({
    workspaces, active, setActive: setActiveWs, files, models, status, backendUp, settings, setSettings,
    messages, setMessages, busy, ask, railSources, railQuery, activeCite, setActiveCite, showSources, refresh, toasts, toast,
  }), [workspaces, active, files, models, status, backendUp, settings, setSettings, messages, busy, ask, railSources, railQuery, activeCite, showSources, refresh, toasts, toast]);

  return <C.Provider value={value}>{children}</C.Provider>;
}
