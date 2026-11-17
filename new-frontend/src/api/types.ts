export interface Workspace { name: string; doc_count: number; custom: boolean }
export interface IndexedFile { name: string; type: string }
export interface SourcePassage {
  id: number;            // citation number [n]
  filename: string;
  page?: number | null;
  chunk_id: string | number;
  score: number;
  text: string;
}
export interface ChatAnswer { answer: string; sources: SourcePassage[]; verified?: boolean }
export interface Message {
  id: string;
  role: 'user' | 'assistant';
  text: string;
  sources?: SourcePassage[];
  verified?: boolean;
  query?: string;
  pending?: boolean;
  error?: string;
}
export interface EngineStatus { cpu_percent: number; ram_percent: number }
export interface Cluster { title: string; description: string }
export interface DocChunk { chunk_id: string | number; text: string; tokens: number; metadata?: Record<string, unknown> }
export interface SqlResult { sql: string; columns: string[]; rows: unknown[][] }
export interface VoiceResult { transcript: string; answer: string; audio_url?: string; audio_b64?: string }
export interface BattleResult { a: string; b: string }
export interface Settings {
  persona: string; model: string; multiHop: boolean; selfRag: boolean; focusFile: string;
}
