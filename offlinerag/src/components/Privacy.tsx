import { FileText, Cpu, Network, BrainCircuit, MessageSquare, ArrowDown } from "lucide-react";
import Reveal from "./Reveal";

const FLOW = [
  { icon: FileText, label: "Your Documents" },
  { icon: Cpu, label: "Local Processing" },
  { icon: Network, label: "Local Vector Search" },
  { icon: BrainCircuit, label: "Local LLM" },
  { icon: MessageSquare, label: "Your Answer" },
];

export default function Privacy() {
  return (
    <section className="border-t border-line bg-base-950 py-24 sm:py-28">
      <div className="mx-auto grid max-w-7xl grid-cols-1 gap-14 px-5 sm:px-8 lg:grid-cols-2 lg:items-center">
        <Reveal>
          <p className="mb-3 font-mono text-xs uppercase tracking-wide text-accent-soft">
            Privacy
          </p>
          <h2 className="font-display text-3xl font-semibold tracking-tight text-ink sm:text-4xl">
            Your data stays yours.
          </h2>
          <p className="mt-5 max-w-md text-base leading-relaxed text-ink-muted">
            OfflineRAG is designed so that your documents and questions can
            remain on your computer.
          </p>
          <div className="mt-6 inline-flex items-center rounded-md border border-line bg-base-900/60 px-4 py-2.5">
            <span className="text-sm text-ink">
              No document upload required.
            </span>
          </div>
        </Reveal>

        <Reveal delay={0.1}>
          <div className="mx-auto flex max-w-xs flex-col items-center gap-1 rounded-2xl border border-line bg-base-900/40 px-6 py-8">
            {FLOW.map(({ icon: Icon, label }, i) => (
              <div key={label} className="flex flex-col items-center">
                <div className="flex w-full items-center gap-3 rounded-lg border border-line bg-base-900 px-4 py-3">
                  <Icon className="h-4 w-4 shrink-0 text-accent-soft" strokeWidth={2} />
                  <span className="font-mono text-xs text-ink">{label}</span>
                </div>
                {i < FLOW.length - 1 && (
                  <ArrowDown className="my-1.5 h-4 w-4 text-ink-faint" />
                )}
              </div>
            ))}
          </div>
        </Reveal>
      </div>
    </section>
  );
}
