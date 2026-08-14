import {
  Upload,
  FileSearch,
  Scissors,
  Layers,
  Database,
  Target,
  MessageCircle,
} from "lucide-react";
import Reveal from "./Reveal";

const STEPS = [
  { icon: Upload, label: "Upload Document" },
  { icon: FileSearch, label: "Extract Text" },
  { icon: Scissors, label: "Split Into Chunks" },
  { icon: Layers, label: "Generate Embeddings" },
  { icon: Database, label: "Store in Local Vector Database" },
  { icon: Target, label: "Retrieve Relevant Context" },
  { icon: MessageCircle, label: "Generate Answer with Local LLM" },
];

export default function HowItWorks() {
  return (
    <section
      id="how-it-works"
      className="border-t border-line bg-base-900/40 py-24 sm:py-28"
    >
      <div className="mx-auto max-w-7xl px-5 sm:px-8">
        <Reveal className="max-w-2xl">
          <p className="mb-3 font-mono text-xs uppercase tracking-wide text-accent-soft">
            Pipeline
          </p>
          <h2 className="font-display text-3xl font-semibold tracking-tight text-ink sm:text-4xl">
            From document to answer.
          </h2>
        </Reveal>

        {/* Desktop: horizontal pipeline */}
        <Reveal delay={0.1} className="mt-16 hidden lg:block">
          <div className="grid grid-cols-7 gap-3">
            {STEPS.map(({ icon: Icon, label }, i) => (
              <div key={label} className="relative flex flex-col items-center text-center">
                {i < STEPS.length - 1 && (
                  <div className="absolute left-1/2 top-6 h-px w-full bg-gradient-to-r from-line to-line" />
                )}
                <div className="relative z-10 flex h-12 w-12 items-center justify-center rounded-full border border-line bg-base-900 text-accent-soft">
                  <Icon className="h-5 w-5" strokeWidth={2} />
                </div>
                <span className="mt-3 font-mono text-[10px] leading-tight text-ink-faint">
                  {String(i + 1).padStart(2, "0")}
                </span>
                <p className="mt-1 text-xs leading-snug text-ink-muted">
                  {label}
                </p>
              </div>
            ))}
          </div>
        </Reveal>

        {/* Mobile / tablet: vertical timeline */}
        <div className="mt-12 space-y-6 lg:hidden">
          {STEPS.map(({ icon: Icon, label }, i) => (
            <Reveal key={label} delay={i * 0.05}>
              <div className="flex items-start gap-4">
                <div className="flex flex-col items-center">
                  <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-line bg-base-900 text-accent-soft">
                    <Icon className="h-4.5 w-4.5" strokeWidth={2} />
                  </div>
                  {i < STEPS.length - 1 && (
                    <span className="mt-1 h-8 w-px bg-line" />
                  )}
                </div>
                <div className="pt-2.5">
                  <span className="font-mono text-[10px] text-ink-faint">
                    {String(i + 1).padStart(2, "0")}
                  </span>
                  <p className="text-sm text-ink">{label}</p>
                </div>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
