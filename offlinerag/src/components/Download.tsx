import { Download as DownloadIcon, Github, Monitor } from "lucide-react";
import { APP_CONFIG } from "../config/app";
import Reveal from "./Reveal";

export default function Download() {
  return (
    <section id="download" className="border-t border-line bg-base-950 py-24 sm:py-28">
      <div className="mx-auto max-w-7xl px-5 sm:px-8">
        <Reveal>
          <div className="relative overflow-hidden rounded-2xl border border-line bg-gradient-to-b from-base-900 to-base-900/60 px-6 py-14 text-center sm:px-14">
            <div className="pointer-events-none absolute inset-0 bg-grid-fade" />
            <div className="relative">
              <h2 className="font-display text-3xl font-semibold tracking-tight text-ink sm:text-4xl">
                Ready to run locally?
              </h2>
              <p className="mx-auto mt-4 max-w-lg text-base leading-relaxed text-ink-muted">
                Download OfflineRAG for Windows and run your knowledge
                assistant directly on your computer.
              </p>

              <div className="mx-auto mt-8 inline-flex items-center gap-2 rounded-full border border-line bg-base-900/70 px-4 py-1.5">
                <Monitor className="h-3.5 w-3.5 text-accent-soft" />
                <span className="font-mono text-xs text-ink-muted">
                  {APP_CONFIG.name} v{APP_CONFIG.version} · {APP_CONFIG.platforms.join(" / ")}
                </span>
              </div>

              <div className="mt-8 flex flex-col justify-center gap-3 sm:flex-row">
                <a
                  href={APP_CONFIG.downloadUrl}
                  className="focus-ring flex items-center justify-center gap-2 rounded-md bg-accent px-6 py-3 text-sm font-medium text-white transition-colors hover:bg-accent-soft"
                >
                  <DownloadIcon className="h-4 w-4" />
                  Download for Windows
                </a>
                <a
                  href={APP_CONFIG.releasesUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="focus-ring flex items-center justify-center gap-2 rounded-md border border-line bg-base-900/60 px-6 py-3 text-sm font-medium text-ink transition-colors hover:border-accent/40"
                >
                  <Github className="h-4 w-4" />
                  View All Releases
                </a>
              </div>

              <p className="mt-6 text-xs text-ink-faint">
                The application is designed to operate offline after
                installation.
              </p>

              {/* REPLACE: APP_CONFIG.downloadUrl in src/config/app.ts with
                  the real GitHub Release .exe asset URL once published. */}
            </div>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
