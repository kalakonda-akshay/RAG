import { useEffect, useRef, useState } from 'react';
import { Api } from '../../api';
import { useApp } from '../../state/AppContext';
import { Button, ErrorNote } from '../ui';

export function VoiceTab() {
  const { active, settings, toast } = useApp();
  const [rec, setRec] = useState(false);
  const [blob, setBlob] = useState<Blob | null>(null);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');
  const [res, setRes] = useState<{ transcript: string; answer: string; audio: string | null } | null>(null);
  const mr = useRef<MediaRecorder | null>(null);
  const chunks = useRef<Blob[]>([]);
  useEffect(() => () => { mr.current?.stream.getTracks().forEach((t) => t.stop()); }, []);

  const toggle = async () => {
    if (rec) { mr.current?.stop(); setRec(false); return; }
    if (!navigator.mediaDevices?.getUserMedia) return toast('err', 'Microphone not available in this browser/context (needs https or localhost).');
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const r = new MediaRecorder(stream); chunks.current = [];
      r.ondataavailable = (e) => chunks.current.push(e.data);
      r.onstop = () => { setBlob(new Blob(chunks.current, { type: r.mimeType })); stream.getTracks().forEach((t) => t.stop()); };
      r.start(); mr.current = r; setRec(true); setBlob(null);
    } catch { toast('err', 'Microphone permission denied'); }
  };

  const go = async () => {
    if (!blob) return toast('info', 'Record something first');
    setBusy(true); setErr('');
    try {
      const r = await Api.voice(blob, { workspace: active, model: settings.model, persona: settings.persona });
      const audio = r.audio_url ?? (r.audio_b64 ? `data:audio/wav;base64,${r.audio_b64}` : null);
      setRes({ transcript: r.transcript, answer: r.answer, audio });
    } catch (e) { setErr((e as Error).message); } finally { setBusy(false); }
  };

  return (
    <div className="panel">
      <div className="mic-wrap">
        <button type="button" className={`mic${rec ? ' rec' : ''}`} onClick={toggle} aria-pressed={rec} aria-label={rec ? 'Stop recording' : 'Start recording'}>🎙️</button>
        <div className="muted">{rec ? 'Recording… tap to stop' : blob ? 'Recording captured' : 'Tap to record your question'}</div>
        {blob && !rec && <audio controls src={URL.createObjectURL(blob)} />}
      </div>
      <Button variant="primary" busy={busy} disabled={!blob} onClick={go}>Start Voice Turn Process</Button>
      {err && <ErrorNote text={err} />}
      {res && (
        <div className="result-card">
          <p><b>You Spoke:</b> “{res.transcript}”</p>
          <p><b>AI Response:</b> {res.answer}</p>
          {res.audio && <audio controls autoPlay src={res.audio} />}
        </div>
      )}
    </div>
  );
}
