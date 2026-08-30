import {
  FileText,
  Cpu,
  Network,
  BrainCircuit,
  MessageSquare,
  Sparkles,
  Layers,
  Scissors,
  GitBranch,
} from "lucide-react";
import Reveal from "./Reveal";

const ALGORITHMS = [
  {
    step: "01",
    name: "Multimodal Document Ingestion",
    algo: "PyPDF2 + pdfplumber + openpyxl + Tesseract OCR + Whisper STT",
    desc: "Parses text, native tables, scanned PDF images via OCR, and audio voice files 100% locally.",
    icon: FileText,
  },
  {
    step: "02",
    name: "Recursive Text Chunker",
    algo: "Sliding Window Sentence Boundary Chunking (500 Token / 50 Overlap)",
    desc: "Preserves semantic sentence integrity and structural context without phrase truncation.",
    icon: Scissors,
  },
  {
    step: "03",
    name: "Dense Vector Embedding",
    algo: "nomic-embed-text (768-Dimensional Dense Vectors)",
    desc: "Encodes extracted text chunks into high-dimensional vector representations stored in local ChromaDB.",
    icon: Layers,
  },
  {
    step: "04",
    name: "Hybrid Search & Rank Fusion",
    algo: "Dense Cosine Similarity + Sparse Rank-BM25 (Reciprocal Rank Fusion)",
    desc: "Combines exact keyword matching with deep semantic context using RRF score fusion.",
    icon: Network,
  },
  {
    step: "05",
    name: "Agentic Multi-Hop RAG",
    algo: "Multi-Query Splitting & Recursive Context Retrieval",
    desc: "Decomposes complex multi-part queries into targeted sub-searches across indexed files.",
    icon: Sparkles,
  },
  {
    step: "06",
    name: "Local LLM & Self-RAG Critic",
    algo: "Ollama (llama3.2:3b) + Hallucination Verification",
    desc: "Synthesizes grounded answers with exact [1], [2] citations; Self-RAG critic audits fact alignment.",
    icon: BrainCircuit,
  },
  {
    step: "07",
    name: "GraphRAG Entity Extraction",
    algo: "Entity-Relationship Triples (Source -> Relation -> Target)",
    desc: "Extracts knowledge graph relationships for instant entity link inspection.",
    icon: GitBranch,
  },
];

export default function Privacy() {
  return (
    <section className="border-t border-line bg-base-950 py-24 sm:py-28">
      <div className="mx-auto max-w-7xl px-5 sm:px-8">
        <div className="grid grid-cols-1 gap-14 lg:grid-cols-12 lg:items-start">
          
          {/* Left Column: Privacy Description */}
          <div className="lg:col-span-5">
            <Reveal>
              <p className="mb-3 font-mono text-xs uppercase tracking-wide text-accent-soft">
                Privacy & Algorithm Architecture
              </p>
              <h2 className="font-display text-3xl font-semibold tracking-tight text-ink sm:text-4xl">
                Your data stays yours.
              </h2>
              <p className="mt-5 text-base leading-relaxed text-ink-muted">
                Orbit is designed so that your documents, vector indices, and LLM questions
                remain 100% on your local computer — zero cloud transmission, zero tracking.
              </p>
              
              <div className="mt-6 flex flex-col gap-3">
                <div className="inline-flex items-center gap-2.5 rounded-lg border border-line bg-base-900/80 px-4 py-3">
                  <span className="h-2 w-2 rounded-full bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.8)]" />
                  <span className="font-mono text-xs text-ink">
                    100% Air-Gapped Local Processing
                  </span>
                </div>

                <div className="inline-flex items-center gap-2.5 rounded-lg border border-line bg-base-900/80 px-4 py-3">
                  <Cpu className="h-4 w-4 text-accent-soft" />
                  <span className="font-mono text-xs text-ink">
                    Powered by Local GPU / CPU Acceleration
                  </span>
                </div>
              </div>
            </Reveal>
          </div>

          {/* Right Column: Algorithms & System Pipeline Cards */}
          <div className="lg:col-span-7">
            <Reveal delay={0.1}>
              <div className="mb-4">
                <h3 className="font-display text-lg font-semibold text-ink">
                  Algorithmic RAG Pipeline
                </h3>
                <p className="text-xs text-ink-faint">
                  Core machine learning & retrieval algorithms powering Orbit:
                </p>
              </div>

              <div className="flex flex-col gap-3">
                {ALGORITHMS.map(({ step, name, algo, desc, icon: Icon }) => (
                  <div
                    key={step}
                    className="group relative overflow-hidden rounded-xl border border-line bg-base-900/60 p-4.5 transition-all duration-300 hover:border-accent-soft/40 hover:bg-base-900"
                  >
                    <div className="flex items-start gap-4">
                      <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg border border-line bg-base-800 text-accent-soft group-hover:border-accent-soft/50 group-hover:text-accent-soft">
                        <Icon className="h-5 w-5" strokeWidth={1.8} />
                      </div>
                      
                      <div className="flex-1">
                        <div className="flex items-center justify-between gap-2">
                          <h4 className="font-display text-sm font-semibold text-ink">
                            {name}
                          </h4>
                          <span className="font-mono text-[11px] font-semibold text-accent-soft">
                            {step}
                          </span>
                        </div>

                        <div className="mt-1 inline-block rounded border border-line/80 bg-base-950 px-2 py-0.5 font-mono text-[11px] font-medium text-amber-400/90">
                          {algo}
                        </div>

                        <p className="mt-2 text-xs leading-relaxed text-ink-muted">
                          {desc}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </Reveal>
          </div>

        </div>
      </div>
    </section>
  );
}
