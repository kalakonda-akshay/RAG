import { useRef, useState } from 'react';
import { ALL_DOCS, TABS } from '../constants';
import { useApp } from '../state/AppContext';
import { Select } from './ui';
import { ChatTab } from './tabs/ChatTab';
import { VoiceTab } from './tabs/VoiceTab';
import { BattleTab, CompareTab, InspectorTab, MindMapTab, PiiTab, QuizTab, SqlTab, TopicsTab, TranslateTab, WebArchiverTab } from './tabs/SimpleTabs';

const VIEWS = [ChatTab, VoiceTab, WebArchiverTab, MindMapTab, TopicsTab, TranslateTab, BattleTab, QuizTab, SqlTab, PiiTab, InspectorTab, CompareTab];

export function Center() {
  const { active, files, settings, setSettings } = useApp();
  const [tab, setTab] = useState(0);
  const refs = useRef<(HTMLButtonElement | null)[]>([]);
  const View = VIEWS[tab];

  const onKey = (e: React.KeyboardEvent) => {
    if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
    const n = (tab + (e.key === 'ArrowRight' ? 1 : TABS.length - 1)) % TABS.length;
    setTab(n); refs.current[n]?.focus();
  };

  return (
    <main className="center">
      <header className="topbar">
        <div><h1>Q&A Thread</h1><p>scoped to {active} ({files.length} files)</p></div>
        <div className="focus">
          <Select label="🎯 Focus Search On Specific File:" value={settings.focusFile} onChange={(v) => setSettings({ focusFile: v })} options={[ALL_DOCS, ...files.map((f) => f.name)]} />
        </div>
      </header>
      <div className="tabs" role="tablist" onKeyDown={onKey}>
        {TABS.map((t, i) => (
          <button key={t} ref={(el) => { refs.current[i] = el; }} role="tab" aria-selected={tab === i} tabIndex={tab === i ? 0 : -1}
            className={`tab${tab === i ? ' active' : ''}`} onClick={() => setTab(i)}>{t}</button>
        ))}
      </div>
      <div className="tabpanel" role="tabpanel"><View /></div>
    </main>
  );
}
