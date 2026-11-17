import { useCallback, useState } from 'react';

/** Wraps an async call with busy/error state. */
export function useAction<A extends unknown[], R>(fn: (...a: A) => Promise<R>) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [data, setData] = useState<R | null>(null);
  const run = useCallback(async (...a: A) => {
    setBusy(true); setError('');
    try { const r = await fn(...a); setData(r); return r; }
    catch (e) { setError(e instanceof Error ? e.message : String(e)); return null; }
    finally { setBusy(false); }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [fn]);
  return { busy, error, data, run, setData };
}
