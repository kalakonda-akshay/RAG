import { useState } from "react";
import {
  FileText,
  Download,
  BookOpen,
  Terminal,
  Cpu,
  Layers,
  Sparkles,
  CheckCircle2,
  ChevronDown,
  ChevronUp,
  FileCode,
  ShieldCheck,
} from "lucide-react";
import Reveal from "./Reveal";

const GUIDE_SECTIONS = [
  {
    id: "install",
    title: "1. Download & First-Time Installation",
    icon: Terminal,
    content: (
      <div className="space-y-4 text-xs text-ink-muted">
        <p className="leading-relaxed">
          Orbit runs 100% locally on your Windows 10/11 computer with zero cloud data transmission.
        </p>

        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
          <div className="rounded-lg border border-line bg-base-950 p-3">
            <span className="font-mono text-[10px] font-semibold text-accent-soft">STEP 01</span>
            <h4 className="mt-1 font-display text-xs font-semibold text-ink">Download Package</h4>
            <p className="mt-1 text-[11px]">Download <code className="text-amber-400">OfflineRAGAssistant_Setup.zip</code> (1.9 GB) from the top download button.</p>
          </div>

          <div className="rounded-lg border border-line bg-base-950 p-3">
            <span className="font-mono text-[10px] font-semibold text-accent-soft">STEP 02</span>
            <h4 className="mt-1 font-display text-xs font-semibold text-ink">Environment Setup</h4>
            <p className="mt-1 text-[11px]">Extract zip file and run in terminal: <code className="text-amber-400">python launcher/first_run_setup.py</code></p>
          </div>

          <div className="rounded-lg border border-line bg-base-950 p-3">
            <span className="font-mono text-[10px] font-semibold text-accent-soft">STEP 03</span>
            <h4 className="mt-1 font-display text-xs font-semibold text-ink">Pull Local Models</h4>
            <p className="mt-1 text-[11px]">Run Ollama commands: <code className="text-amber-400">ollama pull llama3.2:3b</code> and <code className="text-amber-400">ollama pull nomic-embed-text</code></p>
          </div>

          <div className="rounded-lg border border-line bg-base-950 p-3">
            <span className="font-mono text-[10px] font-semibold text-accent-soft">STEP 04</span>
            <h4 className="mt-1 font-display text-xs font-semibold text-ink">Launch Application</h4>
            <p className="mt-1 text-[11px]">Start app server: <code className="text-amber-400">python launcher/run_app.py</code> &rarr; Open <code className="text-emerald-400">http://localhost:8501</code></p>
          </div>
        </div>
      </div>
    ),
  },
  {
    id: "opening",
    title: "2. Post-Launch Walkthrough (Opening the App)",
    icon: BookOpen,
    content: (
      <div className="space-y-3 text-xs text-ink-muted">
        <p className="leading-relaxed">
          When you launch Orbit at <b>http://localhost:8501</b>, you are presented with a modern 3-column dark-mode workspace:
        </p>

        <div className="space-y-2.5">
          <div className="rounded-lg border border-line bg-base-950 p-3">
            <h4 className="font-display text-xs font-semibold text-accent-soft">Rail 1: Left Knowledge Rail (File Manager)</h4>
            <p className="mt-1 text-[11px] leading-relaxed">
              • <b>Workspace Switcher</b>: Select between <i>documents</i>, <i>research</i>, <i>finance</i>, and <i>engineering</i>.<br/>
              • <b>Indexed File Cards</b>: Displays loaded files with format badges (PDF, XLSX, DOCX, PNG).<br/>
              • <b>Upload Dropzone</b>: Drag & drop any of the 29 supported file types.<br/>
              • <b>AI Personas</b>: Switch between <i>Technical Analyst</i>, <i>Tutor</i>, <i>Legal Officer</i>, and <i>Executive Summarizer</i>.<br/>
              • <b>Export PPTX</b>: 1-Click PowerPoint deck generator.
            </p>
          </div>

          <div className="rounded-lg border border-line bg-base-950 p-3">
            <h4 className="font-display text-xs font-semibold text-accent-soft">Rail 2: Center Q&A Thread (Feature Dashboard)</h4>
            <p className="mt-1 text-[11px] leading-relaxed">
              • <b>Scope Banner</b>: Displays active workspace scope (e.g. <i>scoped to research (1 file)</i>).<br/>
              • <b>12 Feature Tabs</b>: Switch between Chat, Voice Call, Web Archiver, Mind Map, Topics, Translate, Battle, Quiz, SQL DB, PII, Compare, Reports.<br/>
              • <b>Message Stream</b>: Grounded answers with inline <b>[1]</b>, <b>[2]</b> citations and clickable source pills.
            </p>
          </div>

          <div className="rounded-lg border border-line bg-base-950 p-3">
            <h4 className="font-display text-xs font-semibold text-accent-soft">Rail 3: Right Grounding Rail (Source Inspector)</h4>
            <p className="mt-1 text-[11px] leading-relaxed">
              • <b>Grounding Gauge</b>: Shows citation verification score (e.g. <i>0.91 high</i>).<br/>
              • <b>Relevance Cards</b>: Shows exact retrieved text snippets with <code>&lt;mark&gt;</code> highlights and page numbers.
            </p>
          </div>
        </div>
      </div>
    ),
  },
  {
    id: "features",
    title: "3. Complete Feature Reference (12 Workspace Tabs)",
    icon: Sparkles,
    content: (
      <div className="grid grid-cols-1 gap-2.5 sm:grid-cols-2 text-xs">
        {[
          ["💬 Grounded Q&A Chat", "Dense vector search + Rank-BM25 hybrid retrieval + Self-RAG verification."],
          ["🎙️ Voice Call Mode", "Hands-free voice interface using microphone input and local Whisper speech transcription."],
          ["🌐 Web Archiver", "Parses and indexes offline web pages, documentation HTML, and articles."],
          ["🗺️ Mind Map Generator", "Generates interactive visual Mermaid.js mind maps from uploaded document concepts."],
          ["🧩 Topic Cluster Discovery", "Performs K-Means semantic clustering to discover hidden themes across files."],
          ["🌐 Multilingual Translator", "Translates document passages into 10+ target languages completely offline."],
          ["⚔️ Model Battle Mode", "Compares responses side-by-side across multiple local LLMs."],
          ["🎓 Auto Document Quiz", "Generates practice test questions with answer keys from document text."],
          ["🗄️ Natural Language SQL Engine", "Queries SQLite (.db/.sqlite) tables using auto-generated SQL code."],
          ["🛡️ PII Redactor & PDF Exporter", "Detects and redacts SSNs, credit cards, emails, and phone numbers, exporting sanitized PDFs."],
          ["🔍 Document Comparator", "Compares two documents side-by-side highlighting overlaps, diffs, and contradictions."],
          ["📊 Report & PPTX Exporter", "Generates 1-click PowerPoint presentations (.pptx) and executive brief summaries."]
        ].map(([title, desc]) => (
          <div key={title} className="rounded-lg border border-line bg-base-950 p-2.5">
            <h4 className="font-display text-xs font-semibold text-ink">{title}</h4>
            <p className="mt-1 text-[11px] text-ink-muted leading-normal">{desc}</p>
          </div>
        ))}
      </div>
    ),
  },
  {
    id: "formats",
    title: "4. Supported File Formats (29 Extensions)",
    icon: FileCode,
    content: (
      <div className="space-y-2 text-xs text-ink-muted">
        <p>Orbit supports 29 file extensions across 7 multimodal ingestion engines:</p>
        <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
          <div className="rounded-lg border border-line bg-base-950 p-2.5">
            <span className="font-mono text-[10px] font-semibold text-accent-soft">DOCUMENTS (5)</span>
            <p className="mt-1 font-mono text-[11px] text-ink">.pdf, .docx, .pptx, .ppt, .md</p>
          </div>
          <div className="rounded-lg border border-line bg-base-950 p-2.5">
            <span className="font-mono text-[10px] font-semibold text-accent-soft">SPREADSHEETS (3)</span>
            <p className="mt-1 font-mono text-[11px] text-ink">.xlsx, .xls, .csv</p>
          </div>
          <div className="rounded-lg border border-line bg-base-950 p-2.5">
            <span className="font-mono text-[10px] font-semibold text-accent-soft">IMAGES & OCR (7)</span>
            <p className="mt-1 font-mono text-[11px] text-ink">.png, .jpg, .jpeg, .webp, .bmp, .tiff, .gif</p>
          </div>
          <div className="rounded-lg border border-line bg-base-950 p-2.5">
            <span className="font-mono text-[10px] font-semibold text-accent-soft">AUDIO & VIDEO (7)</span>
            <p className="mt-1 font-mono text-[11px] text-ink">.wav, .mp3, .m4a, .mp4, .mkv, .mov, .avi</p>
          </div>
          <div className="rounded-lg border border-line bg-base-950 p-2.5 sm:col-span-2">
            <span className="font-mono text-[10px] font-semibold text-accent-soft">CODE & DATABASES (7)</span>
            <p className="mt-1 font-mono text-[11px] text-ink">.txt, .py, .js, .json, .html, .xml, .sql, .sqlite, .db</p>
          </div>
        </div>
      </div>
    ),
  },
  {
    id: "algo",
    title: "5. Algorithmic RAG Architecture Pipeline",
    icon: Cpu,
    content: (
      <div className="space-y-2 text-xs text-ink-muted">
        <p>Core machine learning pipeline powering 100% offline retrieval:</p>
        <div className="space-y-1.5 font-mono text-[11px]">
          <div className="rounded border border-line bg-base-950 p-2 text-ink">1. Multimodal Ingestion &rarr; PyPDF2 + Tesseract OCR + Whisper STT</div>
          <div className="rounded border border-line bg-base-950 p-2 text-ink">2. Recursive Sliding Window Chunker &rarr; 500 Token / 50 Overlap</div>
          <div className="rounded border border-line bg-base-950 p-2 text-ink">3. Dense Vector Embeddings &rarr; nomic-embed-text (768-Dim)</div>
          <div className="rounded border border-line bg-base-950 p-2 text-ink">4. Hybrid RRF Search &rarr; Dense Cosine Similarity + Sparse Rank-BM25</div>
          <div className="rounded border border-line bg-base-950 p-2 text-ink">5. Agentic Multi-Hop RAG &rarr; Recursive Sub-Query Splitting</div>
          <div className="rounded border border-line bg-base-950 p-2 text-ink">6. Local LLM Generator & Self-RAG Critic &rarr; Ollama llama3.2:3b Fact Audit</div>
          <div className="rounded border border-line bg-base-950 p-2 text-ink">7. GraphRAG Entity Extraction &rarr; Source &rarr; Relation &rarr; Target Triples</div>
        </div>
      </div>
    ),
  },
];

export default function UserGuide() {
  const [openSection, setOpenSection] = useState<string | null>("install");

  const toggle = (id: string) => {
    setOpenSection(openSection === id ? null : id);
  };

  return (
    <section id="user-guide" className="border-t border-line bg-base-950 py-24 sm:py-28">
      <div className="mx-auto max-w-7xl px-5 sm:px-8">
        
        {/* Header Title */}
        <Reveal className="max-w-3xl">
          <p className="mb-3 font-mono text-xs uppercase tracking-wide text-accent-soft">
            Documentation & User Guide
          </p>
          <h2 className="font-display text-3xl font-semibold tracking-tight text-ink sm:text-4xl">
            Everything you need to know about Orbit.
          </h2>
          <p className="mt-4 text-base leading-relaxed text-ink-muted">
            Complete user manual, step-by-step setup guide, post-launch 3-column UI walkthrough, 12 workspace feature tabs, and offline format support.
          </p>

          {/* Download Action Buttons */}
          <div className="mt-6 flex flex-wrap items-center gap-3">
            <a
              href="/Orbit_Complete_User_Guide.docx"
              download="Orbit_Complete_User_Guide.docx"
              className="inline-flex items-center gap-2 rounded-lg border border-accent-soft/40 bg-accent/15 px-4 py-2.5 text-xs font-semibold text-ink transition-colors hover:bg-accent/25"
            >
              <FileText className="h-4 w-4 text-accent-soft" />
              Download Word Guide (.docx)
            </a>

            <a
              href="/Orbit_Complete_User_Guide.pdf"
              download="Orbit_Complete_User_Guide.pdf"
              className="inline-flex items-center gap-2 rounded-lg border border-line bg-base-900 px-4 py-2.5 text-xs font-semibold text-ink transition-colors hover:bg-base-800"
            >
              <Download className="h-4 w-4 text-emerald-400" />
              Download PDF Manual (.pdf)
            </a>

            <a
              href="https://github.com/kalakonda-akshay/RAG"
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-2 rounded-lg border border-line bg-base-900 px-4 py-2.5 text-xs font-medium text-ink-muted transition-colors hover:text-ink"
            >
              <ShieldCheck className="h-4 w-4 text-indigo-400" />
              View GitHub Docs
            </a>
          </div>
        </Reveal>

        {/* Interactive Accordion Guide */}
        <Reveal delay={0.1} className="mt-12">
          <div className="flex flex-col gap-3">
            {GUIDE_SECTIONS.map(({ id, title, icon: Icon, content }) => {
              const isOpen = openSection === id;
              return (
                <div
                  key={id}
                  className={`overflow-hidden rounded-xl border transition-all duration-200 ${
                    isOpen
                      ? "border-accent-soft/50 bg-base-900/90 shadow-[0_4px_20px_-4px_rgba(99,102,241,0.15)]"
                      : "border-line bg-base-900/40 hover:border-line/80 hover:bg-base-900/60"
                  }`}
                >
                  <button
                    onClick={() => toggle(id)}
                    className="flex w-full items-center justify-between px-5 py-4 text-left focus:outline-none"
                  >
                    <div className="flex items-center gap-3">
                      <div className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border ${
                        isOpen
                          ? "border-accent-soft/40 bg-accent/15 text-accent-soft"
                          : "border-line bg-base-800 text-ink-muted"
                      }`}>
                        <Icon className="h-4.5 w-4.5" strokeWidth={2} />
                      </div>
                      <h3 className="font-display text-sm font-semibold text-ink">
                        {title}
                      </h3>
                    </div>

                    {isOpen ? (
                      <ChevronUp className="h-4 w-4 text-accent-soft" />
                    ) : (
                      <ChevronDown className="h-4 w-4 text-ink-faint" />
                    )}
                  </button>

                  {isOpen && (
                    <div className="border-t border-line/60 px-5 pb-5 pt-4">
                      {content}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </Reveal>

      </div>
    </section>
  );
}
