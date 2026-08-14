import { useState } from "react";
import { ChevronDown } from "lucide-react";
import Reveal from "./Reveal";

const ITEMS = [
  {
    q: "Is OfflineRAG really offline?",
    a: "OfflineRAG is designed to perform document processing, retrieval, and LLM inference locally, on your own machine, once the required software and models are installed.",
  },
  {
    q: "Do I need an API key?",
    a: "No API key is required for the intended local setup.",
  },
  {
    q: "What documents can I use?",
    a: "Initially PDF, with DOCX and TXT support planned or configurable.",
  },
  {
    q: "Does my document get uploaded?",
    a: "The application is designed to process documents locally.",
  },
  {
    q: "What operating systems are supported?",
    a: "Initially Windows 10 and Windows 11.",
  },
  {
    q: "Is the project open source?",
    a: "Yes, the source code will be available through GitHub.",
  },
];

function FAQItem({
  q,
  a,
  isOpen,
  onToggle,
}: {
  q: string;
  a: string;
  isOpen: boolean;
  onToggle: () => void;
}) {
  return (
    <div className="border-b border-line">
      <button
        onClick={onToggle}
        aria-expanded={isOpen}
        className="focus-ring flex w-full items-center justify-between gap-4 py-5 text-left"
      >
        <span className="font-display text-base font-medium text-ink">
          {q}
        </span>
        <ChevronDown
          className={`h-4 w-4 shrink-0 text-ink-faint transition-transform duration-300 ${
            isOpen ? "rotate-180" : ""
          }`}
        />
      </button>
      <div
        className={`grid overflow-hidden transition-all duration-300 ${
          isOpen ? "grid-rows-[1fr] pb-5" : "grid-rows-[0fr]"
        }`}
      >
        <div className="min-h-0">
          <p className="max-w-2xl text-sm leading-relaxed text-ink-muted">
            {a}
          </p>
        </div>
      </div>
    </div>
  );
}

export default function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  return (
    <section id="faq" className="border-t border-line bg-base-950 py-24 sm:py-28">
      <div className="mx-auto max-w-3xl px-5 sm:px-8">
        <Reveal className="mb-10">
          <p className="mb-3 font-mono text-xs uppercase tracking-wide text-accent-soft">
            FAQ
          </p>
          <h2 className="font-display text-3xl font-semibold tracking-tight text-ink sm:text-4xl">
            Common questions.
          </h2>
        </Reveal>

        <Reveal delay={0.1}>
          <div className="border-t border-line">
            {ITEMS.map((item, i) => (
              <FAQItem
                key={item.q}
                q={item.q}
                a={item.a}
                isOpen={openIndex === i}
                onToggle={() => setOpenIndex(openIndex === i ? null : i)}
              />
            ))}
          </div>
        </Reveal>
      </div>
    </section>
  );
}
