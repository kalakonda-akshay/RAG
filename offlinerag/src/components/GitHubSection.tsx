import { Github, ArrowUpRight } from "lucide-react";
import { APP_CONFIG } from "../config/app";
import Reveal from "./Reveal";

export default function GitHubSection() {
  return (
    <section className="border-t border-line bg-base-900/40 py-24 sm:py-28">
      <div className="mx-auto max-w-7xl px-5 sm:px-8">
        <Reveal>
          <div className="flex flex-col items-start justify-between gap-8 rounded-2xl border border-line bg-base-900/60 p-8 sm:p-10 lg:flex-row lg:items-center">
            <div className="flex items-start gap-4">
              <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg border border-line bg-base-950 text-ink">
                <Github className="h-5 w-5" />
              </div>
              <div>
                <h2 className="font-display text-2xl font-semibold tracking-tight text-ink sm:text-3xl">
                  Open source. Transparent.
                </h2>
                <p className="mt-3 max-w-xl text-sm leading-relaxed text-ink-muted">
                  Explore the source code, report issues, contribute
                  improvements, and follow new releases on GitHub.
                </p>
              </div>
            </div>

            <a
              href={APP_CONFIG.githubUrl}
              target="_blank"
              rel="noreferrer"
              className="focus-ring flex shrink-0 items-center gap-2 rounded-md border border-line bg-base-950 px-5 py-3 text-sm font-medium text-ink transition-colors hover:border-accent/40"
            >
              <Github className="h-4 w-4" />
              View on GitHub
              <ArrowUpRight className="h-3.5 w-3.5 text-ink-faint" />
            </a>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
