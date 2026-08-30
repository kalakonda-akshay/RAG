import Reveal from "./Reveal";

const SHOTS = [
  {
    title: "Grounded Q&A Thread & Interactive Citations",
    subtitle: "Numbered citation chips & interactive document pills",
    src: "/screenshots/chat_citations.png",
  },
  {
    title: "Real-Time Voice Call Mode",
    subtitle: "Mic recording & offline Whisper STT transcription",
    src: "/screenshots/voice_call.png",
  },
  {
    title: "Auto-Generated Document Quiz",
    subtitle: "Interactive multiple-choice test questions from file context",
    src: "/screenshots/quiz_workspace.png",
  },
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
            Screenshots & Interface
          </p>
          <h2 className="font-display text-3xl font-semibold tracking-tight text-ink sm:text-4xl">
            See Orbit in action.
          </h2>
          <p className="mt-4 text-sm text-ink-muted">
            Live application interfaces running 100% offline on your local computer.
          </p>
        </Reveal>

        <Reveal delay={0.1}>
          <div className="mt-12 grid grid-cols-1 gap-8 md:grid-cols-3">
            {SHOTS.map(({ title, subtitle, src }) => (
              <figure
                key={title}
                className="group overflow-hidden rounded-xl border border-line bg-base-900/80 p-3 transition-all duration-300 hover:border-accent-soft/50 hover:shadow-[0_10px_30px_-10px_rgba(99,102,241,0.2)]"
              >
                <div className="relative aspect-[16/10] overflow-hidden rounded-lg border border-line/60 bg-base-950">
                  <img
                    src={src}
                    alt={title}
                    className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
                  />
                </div>
                <figcaption className="mt-4 px-1">
                  <h3 className="font-display text-sm font-semibold text-ink">
                    {title}
                  </h3>
                  <p className="mt-1 font-mono text-xs text-ink-faint">
                    {subtitle}
                  </p>
                </figcaption>
              </figure>
            ))}
          </div>
        </Reveal>
      </div>
    </section>
  );
}
