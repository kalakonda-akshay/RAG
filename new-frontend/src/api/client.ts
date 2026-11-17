import type { EP } from './endpoints';

const BASE: string = (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? '/api';

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) { super(message); this.status = status; }
}

type Route = { method: string; path: string };
type Opts = { json?: unknown; form?: FormData; signal?: AbortSignal; retries?: number };

async function raw(route: Route, opts: Opts = {}): Promise<Response> {
  const headers: Record<string, string> = {};
  let body: BodyInit | undefined;
  if (opts.json !== undefined) { headers['Content-Type'] = 'application/json'; body = JSON.stringify(opts.json); }
  if (opts.form) body = opts.form;
  const idempotent = route.method === 'GET';
  const attempts = idempotent ? (opts.retries ?? 1) + 1 : 1;
  let lastErr: unknown;
  for (let i = 0; i < attempts; i++) {
    try {
      const res = await fetch(BASE + route.path, { method: route.method, headers, body, signal: opts.signal });
      if (!res.ok) {
        let msg = `${res.status} ${res.statusText}`;
        try { const j = await res.json(); msg = j.detail || j.error || j.message || msg; } catch { /* non-JSON body */ }
        throw new ApiError(typeof msg === 'string' ? msg : JSON.stringify(msg), res.status);
      }
      return res;
    } catch (e) {
      lastErr = e;
      if (e instanceof ApiError && e.status < 500) break;
      if ((e as Error).name === 'AbortError') break;
    }
  }
  if (lastErr instanceof ApiError) throw lastErr;
  throw new ApiError('Cannot reach the Archive backend. Is it running?', 0);
}

export async function api<T>(route: Route, opts?: Opts): Promise<T> {
  const res = await raw(route, opts);
  return (await res.json()) as T;
}
export async function apiBlob(route: Route, opts?: Opts): Promise<Blob> {
  return (await raw(route, opts)).blob();
}
export type { Route };
export type _Ep = typeof EP;
