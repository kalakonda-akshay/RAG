import { useEffect, useState } from "react";
import { Github, Menu, X, Waypoints } from "lucide-react";
import { APP_CONFIG } from "../config/app";

const LINKS = [
  { label: "Features", href: "#features" },
  { label: "How It Works", href: "#how-it-works" },
  { label: "Screenshots", href: "#screenshots" },
  { label: "User Guide", href: "#user-guide" },
  { label: "FAQ", href: "#faq" },
];

export default function Navbar() {
  const [open, setOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header
      className={`fixed inset-x-0 top-0 z-50 transition-colors duration-300 ${
        scrolled
          ? "bg-base-950/80 backdrop-blur-md border-b border-line"
          : "bg-transparent border-b border-transparent"
      }`}
    >
      <nav
        className="mx-auto flex h-16 max-w-7xl items-center justify-between px-5 sm:px-8"
        aria-label="Primary"
      >
        <a
          href="#top"
          className="focus-ring flex items-center gap-2 font-display text-[15px] font-semibold text-ink"
        >
          <span className="flex h-7 w-7 items-center justify-center rounded-md bg-accent/15 text-accent-soft">
            <Waypoints className="h-4 w-4" strokeWidth={2.25} />
          </span>
          {APP_CONFIG.name}
        </a>

        <ul className="hidden items-center gap-8 md:flex">
          {LINKS.map((link) => (
            <li key={link.href}>
              <a
                href={link.href}
                className="focus-ring text-sm text-ink-muted transition-colors hover:text-ink"
              >
                {link.label}
              </a>
            </li>
          ))}
        </ul>

        <div className="hidden items-center gap-3 md:flex">
          <a
            href={APP_CONFIG.githubUrl}
            target="_blank"
            rel="noreferrer"
            className="focus-ring flex h-9 w-9 items-center justify-center rounded-md border border-line text-ink-muted transition-colors hover:border-accent/40 hover:text-ink"
            aria-label="View OfflineRAG on GitHub"
          >
            <Github className="h-4 w-4" />
          </a>
          <a
            href={APP_CONFIG.downloadUrl}
            className="focus-ring rounded-md bg-accent px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-accent-soft"
          >
            Download
          </a>
        </div>

        <button
          className="focus-ring flex h-9 w-9 items-center justify-center rounded-md text-ink md:hidden"
          aria-label={open ? "Close menu" : "Open menu"}
          aria-expanded={open}
          onClick={() => setOpen((v) => !v)}
        >
          {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </nav>

      {open && (
        <div className="border-t border-line bg-base-950/95 px-5 pb-6 pt-2 backdrop-blur-md md:hidden">
          <ul className="flex flex-col gap-1">
            {LINKS.map((link) => (
              <li key={link.href}>
                <a
                  href={link.href}
                  onClick={() => setOpen(false)}
                  className="focus-ring block rounded-md px-2 py-2.5 text-sm text-ink-muted hover:bg-base-800 hover:text-ink"
                >
                  {link.label}
                </a>
              </li>
            ))}
          </ul>
          <div className="mt-3 flex gap-3">
            <a
              href={APP_CONFIG.githubUrl}
              target="_blank"
              rel="noreferrer"
              className="focus-ring flex flex-1 items-center justify-center gap-2 rounded-md border border-line py-2.5 text-sm text-ink-muted"
            >
              <Github className="h-4 w-4" /> GitHub
            </a>
            <a
              href={APP_CONFIG.downloadUrl}
              className="focus-ring flex-1 rounded-md bg-accent py-2.5 text-center text-sm font-medium text-white"
            >
              Download
            </a>
          </div>
        </div>
      )}
    </header>
  );
}
