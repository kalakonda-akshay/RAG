import { Fragment } from 'react';

/** Tiny, safe markdown renderer (headings, bullets, bold, inline code, paragraphs). No HTML injection. */
function inline(s: string) {
  return s.split(/(\*\*[^*]+\*\*|`[^`]+`)/g).map((p, i) =>
    p.startsWith('**') ? <strong key={i}>{p.slice(2, -2)}</strong> : p.startsWith('`') ? <code key={i}>{p.slice(1, -1)}</code> : <Fragment key={i}>{p}</Fragment>);
}
export function Markdown({ text }: { text: string }) {
  const lines = text.split('\n');
  const out: JSX.Element[] = []; let list: string[] = [];
  const flush = () => { if (list.length) { out.push(<ul key={out.length}>{list.map((l, i) => <li key={i}>{inline(l)}</li>)}</ul>); list = []; } };
  lines.forEach((l) => {
    if (/^\s*[-*]\s+/.test(l)) { list.push(l.replace(/^\s*[-*]\s+/, '')); return; }
    flush();
    const h = l.match(/^(#{1,4})\s+(.*)/);
    if (h) out.push(<div key={out.length} className={`md-h md-h${h[1].length}`}>{inline(h[2])}</div>);
    else if (l.trim()) out.push(<p key={out.length}>{inline(l)}</p>);
  });
  flush();
  return <div className="md">{out}</div>;
}
