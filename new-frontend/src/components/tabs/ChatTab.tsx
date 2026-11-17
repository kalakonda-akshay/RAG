import { Fragment, useEffect, useRef, useState } from 'react';
import { Api } from '../../api';
import type { Message } from '../../api/types';
import { useApp } from '../../state/AppContext';
import { Button, Empty, ErrorNote, Expander, Spinner } from '../ui';

function Answer({ m }: { m: Message }) {
  const { setActiveCite, showSources } = useApp();
  const n = m.sources?.length ?? 0;
  const parts = m.text.split(/(\[\d+\])/g);
  return (
    <>
      <div className="a-text-ui">
        {parts.map((p, i) => {
          const c = p.match(/^\[(\d+)\]$/);
          if (c) {
            const id = Number(c[1]);
            return <button key={i} type="button" className="cite-ui" aria-label={`Citation ${id}`} onClick={() => { showSources(m); setTimeout(() => setActiveCite(id), 0); }}>{id}</button>;
          }
          return <Fragment key={i}>{p}</Fragment>;
        })}
      </div>
      <div className="meter" aria-label="Grounding confidence">
        <span className="meter-label">GROUNDING</span>
        <div className="meter-track"><div className="meter-fill" style={{ width: `${Math.min(100, 30 + n * 20)}%` }} /></div>
        <span className="meter-text">{n} source{n === 1 ? '' : 's'} · {m.verified === false ? 'unverified' : 'verified'}</span>
      </div>
    </>
  );
}

function Actions({ m }: { m: Message }) {
  const { setActiveCite, showSources, toast } = useApp();
  const [chunksBusy, setBusy] = useState(false);
  const [audio, setAudio] = useState<string | null>(null);
  const read = async () => {
    setBusy(true);
    try { const b = await Api.tts(m.text); setAudio(URL.createObjectURL(b)); } catch (e) { toast('err', (e as Error).message); } finally { setBusy(false); }
  };
  const src = m.sources ?? [];
  return (
    <>
      {src.length > 0 && (
        <div className="pills">
          {src.map((s) => (
            <button key={s.id} type="button" className="src-pill" onClick={() => { showSources(m); setTimeout(() => setActiveCite(s.id), 0); }}>
              📄 [{s.id}] {s.filename}{s.page != null ? ` (p.${s.page})` : ''}
            </button>
          ))}
        </div>
      )}
      {src.length > 0 && (
        <Expander title="📚 View Retrieved Document Chunks & Source Passages">
          {src.map((s) => <div key={s.id} className="chunk"><b>[{s.id}] {s.filename}</b><p>{s.text}</p></div>)}
        </Expander>
      )}
      <div className="msg-actions">
        <Button variant="ghost" busy={chunksBusy} onClick={read}>🔊 Read Aloud</Button>
        {audio && <audio controls autoPlay src={audio} />}
      </div>
    </>
  );
}

export function ChatTab() {
  const { messages, ask, busy, active, files } = useApp();
  const [draft, setDraft] = useState('');
  const end = useRef<HTMLDivElement>(null);
  useEffect(() => { end.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages]);

  const send = () => { const q = draft; if (!q.trim() || busy) return; setDraft(''); void ask(q); };

  return (
    <div className="chat">
      <div className="thread" role="log" aria-live="polite">
        {messages.length === 0 && <Empty>{files.length ? `Ask anything about the ${files.length} file(s) in “${active}”.` : 'Upload files in the left rail, then ask a grounded question.'}</Empty>}
        {messages.map((m) => m.role === 'user' ? (
          <div key={m.id} className="msg user"><div className="q-text-ui">{m.text}</div></div>
        ) : (
          <div key={m.id} className="msg assistant">
            {m.pending && <div className="a-text-ui typing"><Spinner /> Retrieving & reasoning…</div>}
            {m.error && <ErrorNote text={m.error} />}
            {!m.pending && !m.error && <><Answer m={m} /><Actions m={m} /></>}
          </div>
        ))}
        <div ref={end} />
      </div>
      <form className="chatbar" onSubmit={(e) => { e.preventDefault(); send(); }}>
        <input className="chat-input" value={draft} onChange={(e) => setDraft(e.target.value)} placeholder="Ask something grounded in your documents…" aria-label="Ask a question" />
        <button className="send" type="submit" disabled={busy || !draft.trim()} aria-label="Send">{busy ? <Spinner /> : '➤'}</button>
      </form>
    </div>
  );
}
