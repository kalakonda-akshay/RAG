import {
  Lock,
  Cpu,
  SearchCode,
  BrainCircuit,
  Quote,
  KeyRound,
  type LucideIcon,
} from "lucide-react";
import Reveal from "./Reveal";

const FEATURES: { icon: LucideIcon; title: string; desc: string }[] = [
  {
    icon: Lock,
    title: "Private by Design",
    desc: "Your documents remain on your machine.",
  },
  {
    icon: Cpu,
    title: "Local Embeddings",
    desc: "Generate document embeddings without sending your data to a cloud API.",
  },
  {
    icon: SearchCode,
    title: "Semantic Search",
    desc: "Find relevant information based on meaning rather than simple keyword matching.",
  },
  {
    icon: BrainCircuit,
    title: "Local LLM",
    desc: "Generate answers using a language model running locally.",
  },
  {
    icon: Quote,
    title: "Source Citations",
    desc: "See which document and page contributed to an answer.",
  },
  {
    icon: KeyRound,
    title: "No API Key",
    desc: "No OpenAI, Gemini, or other cloud API key is required for normal operation.",
  },
];

export default function Features() {
  return (
    <section id="features" className="border-t border-line bg-base-950 py-24 sm:py-28">
      <div className="mx-auto max-w-7xl px-5 sm:px-8">
        <Reveal className="max-w-2xl">
          <p className="mb-3 font-mono text-xs uppercase tracking-wide text-accent-soft">
            Features
          </p>
          <h2 className="font-display text-3xl font-semibold tracking-tight text-ink sm:text-4xl">
            Everything runs locally.
          </h2>
        </Reveal>

        <div className="mt-14 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {FEATURES.map(({ icon: Icon, title, desc }, i) => (
            <Reveal key={title} delay={i * 0.06}>
              <div className="group h-full rounded-xl border border-line bg-base-900/50 p-6 transition-colors duration-300 hover:border-accent/40 hover:bg-base-900">
                <div className="mb-4 flex h-10 w-10 items-center justify-center rounded-lg bg-accent/10 text-accent-soft transition-colors group-hover:bg-accent/15">
                  <Icon className="h-5 w-5" strokeWidth={2} />
                </div>
                <h3 className="font-display text-base font-semibold text-ink">
                  {title}
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-ink-muted">
                  {desc}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
