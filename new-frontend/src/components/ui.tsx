import { useState, type ReactNode } from 'react';

export function Spinner() { return <span className="spinner" aria-label="Loading" />; }

export function Button({ children, onClick, busy, disabled, variant = 'secondary', full, type = 'button' }:
  { children: ReactNode; onClick?: () => void; busy?: boolean; disabled?: boolean; variant?: 'primary' | 'secondary' | 'ghost'; full?: boolean; type?: 'button' | 'submit' }) {
  return (
    <button type={type} className={`btn btn-${variant}${full ? ' full' : ''}`} onClick={onClick} disabled={disabled || busy}>
      {busy && <Spinner />}{children}
    </button>
  );
}

export function Field({ label, children }: { label: string; children: ReactNode }) {
  return <label className="field"><span className="field-label">{label}</span>{children}</label>;
}

export function Select({ label, value, onChange, options, placeholder }:
  { label: string; value: string; onChange: (v: string) => void; options: string[]; placeholder?: string }) {
  return (
    <Field label={label}>
      <select className="input" value={value} onChange={(e) => onChange(e.target.value)}>
        {placeholder && <option value="">{placeholder}</option>}
        {options.map((o) => <option key={o} value={o}>{o}</option>)}
      </select>
    </Field>
  );
}

export function Toggle({ label, checked, onChange }: { label: string; checked: boolean; onChange: (v: boolean) => void }) {
  return (
    <button type="button" role="switch" aria-checked={checked} className="toggle-row" onClick={() => onChange(!checked)}>
      <span>{label}</span><span className={`switch${checked ? ' on' : ''}`}><i /></span>
    </button>
  );
}

export function Expander({ title, children, defaultOpen = false }: { title: string; children: ReactNode; defaultOpen?: boolean }) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className={`expander${open ? ' open' : ''}`}>
      <button type="button" className="expander-head" aria-expanded={open} onClick={() => setOpen(!open)}>
        <span>{title}</span><span className="chev">▸</span>
      </button>
      {open && <div className="expander-body">{children}</div>}
    </div>
  );
}

export function Empty({ children }: { children: ReactNode }) { return <div className="empty">{children}</div>; }

export function ErrorNote({ text }: { text: string }) { return <div className="errnote" role="alert">⚠ {text}</div>; }

export function ext(name: string) { return (name.split('.').pop() || '').toLowerCase(); }

export function Pill({ name }: { name: string }) {
  const e = ext(name);
  const cls = e === 'pdf' ? 'red' : ['md', 'txt'].includes(e) ? 'green' : ['xlsx', 'csv', 'xls'].includes(e) ? 'emerald' : ['png', 'jpg', 'jpeg', 'webp', 'gif', 'bmp', 'tiff'].includes(e) ? 'amber' : 'gray';
  return <span className={`ftype ${cls}`}>{e.toUpperCase() || 'FILE'}</span>;
}

/** Splits text on query terms and wraps matches in <mark>. */
export function Highlight({ text, query }: { text: string; query: string }) {
  const terms = query.toLowerCase().split(/\W+/).filter((t) => t.length > 3);
  if (!terms.length) return <>{text}</>;
  const re = new RegExp(`(${terms.map((t) => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|')})`, 'gi');
  return <>{text.split(re).map((p, i) => (i % 2 ? <mark key={i}>{p}</mark> : <span key={i}>{p}</span>))}</>;
}

export function downloadBlob(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a'); a.href = url; a.download = filename; a.click();
  setTimeout(() => URL.revokeObjectURL(url), 2000);
}
