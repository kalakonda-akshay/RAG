import { Waypoints } from "lucide-react";
import { APP_CONFIG } from "../config/app";

const COLUMNS = [
  {
    heading: "Project",
    links: [
      { label: "GitHub", href: APP_CONFIG.githubUrl },
      { label: "Releases", href: APP_CONFIG.releasesUrl },
      { label: "Issues", href: APP_CONFIG.issuesUrl },
    ],
  },
  {
    heading: "Resources",
    // REPLACE: point these at real pages/files once they exist
    links: [
      { label: "Documentation", href: "#" },
      { label: "Privacy", href: "#" },
      { label: "License", href: "#" },
    ],
  },
];

export default function Footer() {
  return (
    <footer className="border-t border-line bg-base-950">
      <div className="mx-auto max-w-7xl px-5 py-14 sm:px-8">
        <div className="flex flex-col gap-10 sm:flex-row sm:justify-between">
          <div className="max-w-xs">
            <div className="flex items-center gap-2 font-display text-sm font-semibold text-ink">
              <span className="flex h-7 w-7 items-center justify-center rounded-md bg-accent/15 text-accent-soft">
                <Waypoints className="h-4 w-4" strokeWidth={2.25} />
              </span>
              {APP_CONFIG.name}
            </div>
            <p className="mt-3 text-sm text-ink-muted">
              {APP_CONFIG.tagline}
            </p>
          </div>

          <div className="grid grid-cols-2 gap-10 sm:flex sm:gap-16">
            {COLUMNS.map((col) => (
              <div key={col.heading}>
                <h3 className="font-mono text-[11px] uppercase tracking-wide text-ink-faint">
                  {col.heading}
                </h3>
                <ul className="mt-3 space-y-2.5">
                  {col.links.map((link) => (
                    <li key={link.label}>
                      <a
                        href={link.href}
                        target={link.href.startsWith("http") ? "_blank" : undefined}
                        rel={link.href.startsWith("http") ? "noreferrer" : undefined}
                        className="focus-ring text-sm text-ink-muted transition-colors hover:text-ink"
                      >
                        {link.label}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

        <div className="mt-12 border-t border-line pt-6">
          <p className="text-xs text-ink-faint">© 2026 {APP_CONFIG.name}</p>
        </div>
      </div>
    </footer>
  );
}
