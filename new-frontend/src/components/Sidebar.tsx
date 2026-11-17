import { useRef, useState } from 'react';
import { Api } from '../api';
import { ACCEPTED, LANGUAGES as _L, PERSONAS, PRESET_WORKSPACES } from '../constants';
import { useApp } from '../state/AppContext';
import { Button, Expander, Field, Pill, Select, Toggle, downloadBlob } from './ui';
import { Markdown } from './Markdown';

void _L;

export function Sidebar() {
  const { workspaces, active, setActive, files, models, status, settings, setSettings, messages, setMessages, refresh, toast, backendUp } = useApp();
  const [newWs, setNewWs] = useState('');
  const [creating, setCreating] = useState(false);
  const [clear, setClear] = useState(true);
  const [picked, setPicked] = useState<File[]>([]);
  const [drag, setDrag] = useState(false);
  const [progress, setProgress] = useState<{ pct: number; label: string } | null>(null);
  const [sessName, setSessName] = useState('');
  const [sessions, setSessions] = useState<string[]>([]);
  const [sessPick, setSessPick] = useState('');
  const [brief, setBrief] = useState('');
  const [briefBusy, setBriefBusy] = useState(false);
  const [deckBusy, setDeckBusy] = useState(false);
  const [deckBlob, setDeckBlob] = useState<Blob | null>(null);
  const inp = useRef<HTMLInputElement>(null);

  const accept = (list: FileList | File[]) => {
    const ok: File[] = []; const bad: string[] = [];
    Array.from(list).forEach((f) => (ACCEPTED.includes((f.name.split('.').pop() || '').toLowerCase()) ? ok.push(f) : bad.push(f.name)));
    if (bad.length) toast('err', `Unsupported file type: ${bad.join(', ')}`);
    setPicked((p) => [...p, ...ok]);
  };

  const createWs = async () => {
    const name = newWs.trim().toLowerCase().replace(/\s+/g, '_');
    if (!/^[a-z0-9_-]{2,40}$/.test(name)) return toast('err', 'Use 2–40 letters, numbers, _ or -');
    if (workspaces.some((w) => w.name === name)) return toast('err', 'Workspace already exists');
    setCreating(true);
    try { await Api.createWorkspace(name); toast('ok', `Workspace “${name}” created`); setNewWs(''); await refresh(); setActive(name); }
    catch (e) { toast('err', (e as Error).message); } finally { setCreating(false); }
  };

  const delWs = async (name: string) => {
    if (!window.confirm(`Delete workspace “${name}” and all its indexed files?`)) return;
    try { await Api.deleteWorkspace(name); toast('ok', `Deleted “${name}”`); if (active === name) setActive(PRESET_WORKSPACES[0]); await refresh(); }
    catch (e) { toast('err', (e as Error).message); }
  };

  const process = async () => {
    if (!picked.length) return toast('info', 'Choose files first');
    setProgress({ pct: 25, label: 'Uploading…' });
    try {
      const t = setTimeout(() => setProgress({ pct: 65, label: 'Indexing…' }), 800);
      await Api.ingest(active, picked, clear);
      clearTimeout(t); setProgress({ pct: 100, label: 'Done' });
      toast('ok', `Indexed ${picked.length} file(s)`); setPicked([]); await refresh();
    } catch (e) { toast('err', (e as Error).message); setProgress(null); return; }
    setTimeout(() => setProgress(null), 1500);
  };

  const loadSessions = async () => { try { const s = await Api.sessions(active); setSessions(s); if (!sessPick && s[0]) setSessPick(s[0]); } catch { setSessions([]); } };
  const saveSession = async () => {
    const n = sessName.trim(); if (!n) return toast('err', 'Enter a session name');
    try { await Api.saveSession(active, n, messages); toast('ok', `Saved “${n}”`); setSessName(''); await loadSessions(); } catch (e) { toast('err', (e as Error).message); }
  };
  const loadSession = async () => {
    if (!sessPick) return toast('info', 'No session selected');
    try { const r = await Api.loadSession(active, sessPick); setMessages(r.messages); toast('ok', `Loaded “${sessPick}”`); } catch (e) { toast('err', (e as Error).message); }
  };

  const makeBrief = async () => { setBriefBusy(true); try { setBrief((await Api.brief(active)).markdown); } catch (e) { toast('err', (e as Error).message); } finally { setBriefBusy(false); } };
  const makeDeck = async () => { setDeckBusy(true); setDeckBlob(null); try { setDeckBlob(await Api.deck(active)); toast('ok', 'Deck ready'); } catch (e) { toast('err', (e as Error).message); } finally { setDeckBusy(false); } };

  return (
    <aside className="rail left" aria-label="Knowledge and configuration">
      <div className="brand">
        <div className="logo">A</div>
        <div><div className="brand-title">Archive</div><div className="brand-sub">local · offline · grounded</div></div>
      </div>

      <div className="left-scroll">
        <section>
          <h3 className="sec">WORKSPACES</h3>
          <ul className="ws-list">
            {workspaces.map((w) => {
              const on = w.name === active;
              return (
                <li key={w.name} className="ws-item">
                  <button type="button" className={`ws-btn${on ? ' active' : ''}`} onClick={() => setActive(w.name)} aria-current={on}>
                    {on ? '📂' : '📁'} {w.name} <span className="count">({on ? files.length || w.doc_count : w.doc_count})</span>
                  </button>
                  {w.custom && <button type="button" className="icon-btn" aria-label={`Delete ${w.name}`} onClick={() => delWs(w.name)}>🗑️</button>}
                </li>
              );
            })}
          </ul>
          <Expander title="➕ Add Workspace">
            <Field label="Workspace Name:"><input className="input" value={newWs} placeholder="e.g. legal_contracts" onChange={(e) => setNewWs(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && createWs()} /></Field>
            <Button full busy={creating} onClick={createWs}>Create Workspace</Button>
          </Expander>
        </section>

        <section>
          <h3 className="sec">INDEXED SOURCES</h3>
          {files.length === 0 && <div className="empty small">{backendUp === false ? 'Backend unreachable' : 'No files indexed in this workspace'}</div>}
          <div className="src-list">
            {files.map((f) => (
              <div className="src-card" key={f.name} title={f.name}>
                <div className="src-top"><Pill name={f.name} /><span className="src-name">{f.name}</span></div>
                <div className="src-meta">Indexed · workspace '{active}'</div>
              </div>
            ))}
          </div>
        </section>

        <section>
          <h3 className="sec">INGEST FILES</h3>
          <label className="check"><input type="checkbox" checked={clear} onChange={(e) => setClear(e.target.checked)} /> 🧹 Clear previous files on upload</label>
          <div className={`drop${drag ? ' over' : ''}`} role="button" tabIndex={0}
            onClick={() => inp.current?.click()} onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && inp.current?.click()}
            onDragOver={(e) => { e.preventDefault(); setDrag(true); }} onDragLeave={() => setDrag(false)}
            onDrop={(e) => { e.preventDefault(); setDrag(false); accept(e.dataTransfer.files); }}>
            <div className="drop-ic">⬆</div>
            <div>Drag & drop files here</div>
            <div className="drop-sub">or click to browse · {ACCEPTED.length} formats</div>
            <input ref={inp} type="file" multiple hidden accept={ACCEPTED.map((x) => `.${x}`).join(',')} onChange={(e) => { if (e.target.files) accept(e.target.files); e.target.value = ''; }} />
          </div>
          {picked.length > 0 && (
            <ul className="picked">
              {picked.map((f, i) => (
                <li key={f.name + i}><span className="src-name">{f.name}</span>
                  <button type="button" className="icon-btn" aria-label={`Remove ${f.name}`} onClick={() => setPicked(picked.filter((_, j) => j !== i))}>✕</button></li>
              ))}
            </ul>
          )}
          <Button full onClick={process} busy={!!progress && progress.pct < 100}>⚡ Process Files</Button>
          {progress && (
            <div className="progress" role="progressbar" aria-valuenow={progress.pct} aria-valuemin={0} aria-valuemax={100}>
              <div className="progress-bar" style={{ width: `${progress.pct}%` }} /><span>{progress.label}</span>
            </div>
          )}
        </section>

        <section>
          <Expander title="💾 Saved Sessions">
            <Field label="Session Name:"><input className="input" value={sessName} placeholder="e.g. Q3_Review" onChange={(e) => setSessName(e.target.value)} /></Field>
            <Button full onClick={saveSession}>Save</Button>
            <div onFocus={loadSessions} onMouseEnter={loadSessions}>
              <Select label="Saved sessions" value={sessPick} onChange={setSessPick} options={sessions} placeholder={sessions.length ? 'Select…' : 'No saved sessions'} />
            </div>
            <Button full onClick={loadSession}>Load</Button>
          </Expander>
          <Expander title="📤 Export Reports">
            <Button full busy={briefBusy} onClick={makeBrief}>📊 Executive Brief</Button>
            {brief && <div className="brief"><Markdown text={brief} /></div>}
            <Button full busy={deckBusy} onClick={makeDeck}>📈 Pitch Deck (.pptx)</Button>
            {deckBlob && <Button full variant="primary" onClick={() => downloadBlob(deckBlob, 'Executive_Deck.pptx')}>📥 Download Executive_Deck.pptx</Button>}
          </Expander>
        </section>

        <section>
          <h3 className="sec">AI PERSONA & CONTROLS</h3>
          <Select label="Persona Role:" value={settings.persona} onChange={(v) => setSettings({ persona: v })} options={PERSONAS} />
          <Select label="LLM Model:" value={settings.model} onChange={(v) => setSettings({ model: v })} options={models} placeholder={models.length ? undefined : 'No Ollama models found'} />
          <Toggle label="⚡ Multi-Hop RAG" checked={settings.multiHop} onChange={(v) => setSettings({ multiHop: v })} />
          <Toggle label="🛡️ Self-RAG Critic" checked={settings.selfRag} onChange={(v) => setSettings({ selfRag: v })} />
        </section>
      </div>

      <div className="engine">
        <div className="offline"><span className="pulse" />100% OFFLINE</div>
        <dl>
          <div><dt>Model</dt><dd>{settings.model || '—'}</dd></div>
          <div><dt>Retrieval</dt><dd>{settings.multiHop ? 'multi-hop' : 'single-hop'}</dd></div>
          <div><dt>Self-check</dt><dd>{settings.selfRag ? 'on' : 'off'}</dd></div>
          <div><dt>CPU / RAM</dt><dd>{status ? `${Math.round(status.cpu_percent)}% / ${Math.round(status.ram_percent)}%` : '—'}</dd></div>
        </dl>
      </div>
    </aside>
  );
}
