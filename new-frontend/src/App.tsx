import { useState } from 'react';
import { Center } from './components/Center';
import { GroundingRail } from './components/GroundingRail';
import { Sidebar } from './components/Sidebar';
import { AppProvider, useApp } from './state/AppContext';

function Toasts() {
  const { toasts } = useApp();
  return <div className="toasts" aria-live="polite">{toasts.map((t) => <div key={t.id} className={`toast ${t.kind}`}>{t.text}</div>)}</div>;
}

function Shell() {
  const { backendUp } = useApp();
  const [nav, setNav] = useState(false);
  const [rail, setRail] = useState(false);
  return (
    <div className={`app${nav ? ' show-left' : ''}${rail ? ' show-right' : ''}`}>
      {backendUp === false && <div className="banner">Backend unreachable — check that the Archive server is running and VITE_BACKEND_URL / endpoints are correct (src/api/endpoints.ts).</div>}
      <div className="mobilebar">
        <button type="button" onClick={() => { setNav(!nav); setRail(false); }} aria-label="Toggle knowledge rail">☰ Knowledge</button>
        <button type="button" onClick={() => { setRail(!rail); setNav(false); }} aria-label="Toggle grounding rail">Grounding ◨</button>
      </div>
      <div className="layout">
        <Sidebar />
        <Center />
        <GroundingRail />
      </div>
      <Toasts />
    </div>
  );
}

export default function App() { return <AppProvider><Shell /></AppProvider>; }
