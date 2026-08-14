import { ImageIcon } from "lucide-react";
import Reveal from "./Reveal";

// REPLACE: swap each `src: undefined` placeholder below for a real
// screenshot path once available, e.g. src: "/screenshots/chat.png"
const SHOTS = [
  { title: "Main Chat Interface", src: undefined as string | undefined },
  { title: "Document Upload", src: undefined as string | undefined },
  { title: "Search / Retrieval Results", src: undefined as string | undefined },
  { title: "Source Citations", src: undefined as string | undefined },
  { title: "Settings / Model Page", src: undefined as string | undefined },
];

export default function Screenshots() {
  return (
    <section
      id="screenshots"
      className="border-t border-line bg-base-900/40 py-24 sm:py-28"
    >
      <div className="mx-auto max-w-7xl px-5 sm:px-8">
        <Reveal className="max-w-2xl">
          <p className="mb-3 font-mono text-xs uppercase tracking-wide text-accent-soft">
            Screenshots
          </p>
          <h2 className="font-display text-3xl font-semibold tracking-tight text-ink sm:text-4xl">
            See OfflineRAG in action.
          </h2>
          <p className="mt-4 text-sm text-ink-muted">
            Placeholder frames below — real product screenshots will replace
            these before release.
          </p>
        </Reveal>

        <Reveal delay={0.1}>
          <div className="thin-scroll mt-12 flex snap-x gap-5 overflow-x-auto pb-4">
            {SHOTS.map(({ title, src }) => (
              <figure
                key={title}
                className="w-[280px] shrink-0 snap-start sm:w-[340px]"
              >
                <div className="flex aspect-[16/10] items-center justify-center overflow-hidden rounded-xl border border-dashed border-line bg-base-900">
                  {src ? (
                    <img
                      src={src}
                      alt={title}
                      className="h-full w-full object-cover"
                    />
                  ) : (
                    <div className="flex flex-col items-center gap-2 text-ink-faint">
                      <ImageIcon className="h-6 w-6" strokeWidth={1.5} />
                      <span className="font-mono text-[10px] uppercase tracking-wide">
                        Screenshot coming soon
                      </span>
                    </div>
                  )}
                </div>
                <figcaption className="mt-3 text-sm text-ink-muted">
                  {title}
                </figcaption>
              </figure>
            ))}
          </div>
        </Reveal>
      </div>
    </section>
  );
}
