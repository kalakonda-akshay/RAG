import { useEffect, useId, useRef, useState } from 'react';
import { Api } from '../../api';
import type { Cluster, DocChunk, SqlResult } from '../../api/types';
import { ALL_DOCS, LANGUAGES } from '../../constants';
import { useApp } from '../../state/AppContext';
import { Button, Empty, ErrorNote, Field, Select } from '../ui';
import { useAction } from './useAction';

export function WebArchiverTab() {
  const { active, refresh, toast } = useApp();
  const [url, setUrl] = useState('https://docs.python.org/3/');
  const [busy, setBusy] = useState(false); const [err, setErr] = useState('');
  const go = async () => {
    try { new URL(url); } catch { return setErr('Enter a valid URL including https://'); }
    setBusy(true); setErr('');
    try { const r = await Api.crawl(url, active); toast('ok', r.message || 'Page crawled and indexed'); await refresh(); }
    catch (e) { setErr((e as Error).message); } finally { setBusy(false); }
  };
  return (
    <div className="panel">
      <Field label="Enter Webpage URL:"><input className="input" value={url} onChange={(e) => setUrl(e.target.value)} /></Field>
      <Button variant="primary" busy={busy} onClick={go}>Crawl & Index Webpage</Button>
      {err && <ErrorNote text={err} />}
    </div>
  );
}

let mermaidReady: Promise<typeof import('mermaid').default> | null = null;
function loadMermaid() {
  mermaidReady ??= import('mermaid').then((m) => { m.default.initialize({ startOnLoad: false, theme: 'dark', securityLevel: 'strict' }); return m.default; });
  return mermaidReady;
}

export function MindMapTab() {
  const { active, settings } = useApp();
  const a = useAction(Api.mindmap);
  const [svg, setSvg] = useState(''); const [rerr, setRerr] = useState('');
  const id = 'mm' + useId().replace(/:/g, '');
  const go = async () => {
    setSvg(''); setRerr('');
    const r = await a.run(active, settings.focusFile === ALL_DOCS ? null : settings.focusFile);
    if (!r) return;
    try { const m = await loadMermaid(); const out = await m.render(id, r.mermaid); setSvg(out.svg); }
    catch { setRerr('The backend returned a diagram Mermaid could not render.'); }
  };
  return (
    <div className="panel">
      <Button variant="primary" busy={a.busy} onClick={go}>Generate Document Mind Map</Button>
      {(a.error || rerr) && <ErrorNote text={a.error || rerr} />}
      {svg && <div className="mermaid-box" dangerouslySetInnerHTML={{ __html: svg }} />}
    </div>
  );
}

export function TopicsTab() {
  const { active } = useApp();
  const a = useAction(Api.topics);
  const cl: Cluster[] = a.data?.clusters ?? [];
  return (
    <div className="panel">
      <Button variant="primary" busy={a.busy} onClick={() => a.run(active)}>Discover Topic Clusters</Button>
      {a.error && <ErrorNote text={a.error} />}
      <div className="grid2">
        {cl.map((c, i) => <div key={i} className="result-card"><b>Cluster {i + 1}: {c.title}</b> — <span className="muted">{c.description}</span></div>)}
      </div>
      {a.data && cl.length === 0 && <Empty>No clusters found.</Empty>}
    </div>
  );
}

export function TranslateTab() {
  const [text, setText] = useState(''); const [lang, setLang] = useState(LANGUAGES[0]);
  const a = useAction(Api.translate);
  return (
    <div className="panel">
      <Field label="Text to translate:"><textarea className="input" rows={5} value={text} onChange={(e) => setText(e.target.value)} /></Field>
      <Select label="Target Language:" value={lang} onChange={setLang} options={LANGUAGES} />
      <Button variant="primary" busy={a.busy} disabled={!text.trim()} onClick={() => a.run(text, lang)}>Translate Text</Button>
      {a.error && <ErrorNote text={a.error} />}
      {a.data && <div className="result-card pre">{a.data.translation}</div>}
    </div>
  );
}

export function BattleTab() {
  const { models, active } = useApp();
  const [ma, setMa] = useState(''); const [mb, setMb] = useState(''); const [q, setQ] = useState('');
  useEffect(() => { if (models.length) { setMa((v) => v || models[0]); setMb((v) => v || models[1] || models[0]); } }, [models]);
  const a = useAction(Api.battle);
  return (
    <div className="panel">
      <div className="grid2">
        <Select label="Model A:" value={ma} onChange={setMa} options={models} />
        <Select label="Model B:" value={mb} onChange={setMb} options={models} />
      </div>
      <Field label="Battle Question:"><input className="input" value={q} onChange={(e) => setQ(e.target.value)} /></Field>
      <Button variant="primary" busy={a.busy} disabled={!q.trim() || !ma || !mb} onClick={() => a.run({ model_a: ma, model_b: mb, question: q, workspace: active })}>Run Model Battle</Button>
      {a.error && <ErrorNote text={a.error} />}
      {a.data && (
        <div className="battle">
          <div className="result-card"><div className="badge">{ma}</div><div className="pre">{a.data.a}</div></div>
          <div className="result-card"><div className="badge">{mb}</div><div className="pre">{a.data.b}</div></div>
        </div>
      )}
    </div>
  );
}

export function QuizTab() {
  const { active } = useApp();
  const a = useAction(Api.quiz);
  return (
    <div className="panel">
      <Button variant="primary" busy={a.busy} onClick={() => a.run(active)}>Generate Quiz Questions</Button>
      {a.error && <ErrorNote text={a.error} />}
      <div className="stack">{a.data?.questions.map((qq, i) => <div key={i} className="result-card"><b>Q{i + 1}:</b> {qq}</div>)}</div>
    </div>
  );
}

export function SqlTab() {
  const { files, active } = useApp();
  const dbs = files.map((f) => f.name).filter((n) => /\.(sqlite|db)$/i.test(n));
  const [db, setDb] = useState(''); const [q, setQ] = useState('');
  useEffect(() => { setDb((v) => (dbs.includes(v) ? v : dbs[0] ?? '')); }, [dbs.join('|')]); // eslint-disable-line react-hooks/exhaustive-deps
  const a = useAction(Api.sql);
  const r: SqlResult | null = a.data;
  return (
    <div className="panel">
      {dbs.length === 0 ? <Empty>Index a .sqlite or .db file in this workspace to query it.</Empty> : (
        <>
          <Select label="Select SQLite database:" value={db} onChange={setDb} options={dbs} />
          <Field label="Ask a question about database:"><input className="input" value={q} onChange={(e) => setQ(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && q.trim() && a.run(db, q, active)} /></Field>
          <Button variant="primary" busy={a.busy} disabled={!q.trim() || !db} onClick={() => a.run(db, q, active)}>Execute SQL Query</Button>
        </>
      )}
      {a.error && <ErrorNote text={a.error} />}
      {r && (
        <>
          <pre className="code"><code>{r.sql}</code></pre>
          <div className="table-wrap">
            <table className="grid"><thead><tr>{r.columns.map((c) => <th key={c}>{c}</th>)}</tr></thead>
              <tbody>{r.rows.map((row, i) => <tr key={i}>{row.map((v, j) => <td key={j}>{v == null ? '' : String(v)}</td>)}</tr>)}</tbody></table>
          </div>
          {r.rows.length === 0 && <Empty>Query returned no rows.</Empty>}
        </>
      )}
    </div>
  );
}

export function PiiTab() {
  const [text, setText] = useState('');
  const a = useAction(Api.redact);
  return (
    <div className="panel">
      <Field label="Paste text to redact PII:"><textarea className="input" rows={7} value={text} onChange={(e) => setText(e.target.value)} /></Field>
      <Button variant="primary" busy={a.busy} disabled={!text.trim()} onClick={() => a.run(text)}>Redact PII</Button>
      {a.error && <ErrorNote text={a.error} />}
      {a.data && <div className="result-card pre redacted">{a.data.redacted}</div>}
    </div>
  );
}

export function InspectorTab() {
  const { files, active } = useApp();
  const names = files.map((f) => f.name);
  const [doc, setDoc] = useState('');
  const seq = useRef(0);
  const [chunks, setChunks] = useState<DocChunk[] | null>(null); const [busy, setBusy] = useState(false); const [err, setErr] = useState('');
  useEffect(() => { setDoc((v) => (names.includes(v) ? v : names[0] ?? '')); }, [names.join('|')]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => {
    if (!doc) { setChunks(null); return; }
    const my = ++seq.current; setBusy(true); setErr('');
    Api.inspect(active, doc).then((r) => { if (my === seq.current) setChunks(r.chunks); })
      .catch((e: Error) => { if (my === seq.current) setErr(e.message); })
      .finally(() => { if (my === seq.current) setBusy(false); });
  }, [doc, active]);
  return (
    <div className="panel">
      {names.length === 0 ? <Empty>No indexed documents to inspect.</Empty> : <Select label="Select document:" value={doc} onChange={setDoc} options={names} />}
      {busy && <div className="muted">Loading chunks…</div>}
      {err && <ErrorNote text={err} />}
      <div className="stack">
        {chunks?.map((c) => (
          <div key={String(c.chunk_id)} className="result-card">
            <div className="meta-row"><span className="badge">chunk {c.chunk_id}</span><span className="badge">{c.tokens} tokens</span>
              {c.metadata && Object.entries(c.metadata).map(([k, v]) => <span key={k} className="badge dim">{k}: {String(v)}</span>)}</div>
            <div className="pre">{c.text}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

export function CompareTab() {
  const { files, active } = useApp();
  const names = files.map((f) => f.name);
  const [a, setA] = useState(''); const [b, setB] = useState('');
  useEffect(() => { setA((v) => (names.includes(v) ? v : names[0] ?? '')); setB((v) => (names.includes(v) ? v : names[1] ?? names[0] ?? '')); }, [names.join('|')]); // eslint-disable-line react-hooks/exhaustive-deps
  const act = useAction(Api.compare);
  return (
    <div className="panel">
      {names.length < 2 ? <Empty>Index at least two documents to compare them.</Empty> : (
        <>
          <div className="grid2"><Select label="Document A:" value={a} onChange={setA} options={names} /><Select label="Document B:" value={b} onChange={setB} options={names} /></div>
          <Button variant="primary" busy={act.busy} disabled={a === b} onClick={() => act.run(active, a, b)}>Compare Documents</Button>
          {a === b && <div className="muted">Pick two different documents.</div>}
        </>
      )}
      {act.error && <ErrorNote text={act.error} />}
      {act.data && <div className="result-card pre">{act.data.summary}</div>}
    </div>
  );
}
