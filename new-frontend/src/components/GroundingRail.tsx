import { useEffect, useRef } from 'react';
import { useApp } from '../state/AppContext';
import { Empty, Highlight } from './ui';

export function GroundingRail() {
  const { railSources, railQuery, activeCite, setActiveCite } = useApp();
  const refs = useRef<Record<number, HTMLElement | null>>({});
  useEffect(() => { if (activeCite != null) refs.current[activeCite]?.scrollIntoView({ behavior: 'smooth', block: 'center' }); }, [activeCite]);

  return (
    <aside className="rail right" aria-label="Grounding and citations">
      <header className="rail-head"><h2>Grounding</h2><p>sources cited in this answer</p></header>
      <div className="right-scroll">
        {railSources.length === 0 && <Empty>Ask a question — the passages behind each answer appear here.</Empty>}
        {railSources.map((s) => (
          <article key={s.id} ref={(el) => { refs.current[s.id] = el; }} id={`src-${s.id}`}
            className={`gcard${activeCite === s.id ? ' active' : ''}`} onClick={() => setActiveCite(s.id)}>
            <div className="gcard-top">
              <span className="gnum">{s.id}</span>
              <span className="gname" title={s.filename}>📄 {s.filename}</span>
              <span className="score">{s.score.toFixed(2)}</span>
            </div>
            <blockquote className="snippet"><Highlight text={s.text} query={railQuery} /></blockquote>
            <footer className="gfoot">{s.page != null ? `p.${s.page}` : 'p.–'} · chunk {s.chunk_id}</footer>
          </article>
        ))}
      </div>
    </aside>
  );
}
