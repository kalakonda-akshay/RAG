import {
  FileText,
  Library,
  MessageSquare,
  Settings,
  Sparkles,
  SendHorizontal,
} from "lucide-react";

const SIDEBAR_ITEMS = [
  { icon: FileText, label: "Documents" },
  { icon: Library, label: "Knowledge Base" },
  { icon: MessageSquare, label: "Chat", active: true },
  { icon: Settings, label: "Settings" },
];

export default function AppMockup() {
  return (
    <div className="w-full animate-float [animation-duration:8s]">
      <div className="overflow-hidden rounded-xl border border-line bg-base-900/90 shadow-[0_30px_80px_-20px_rgba(0,0,0,0.6)] backdrop-blur">
        {/* Title bar */}
        <div className="flex items-center gap-1.5 border-b border-line bg-base-800/60 px-4 py-2.5">
          <span className="h-2.5 w-2.5 rounded-full bg-[#4b5162]" />
          <span className="h-2.5 w-2.5 rounded-full bg-[#4b5162]" />
          <span className="h-2.5 w-2.5 rounded-full bg-[#4b5162]" />
          <span className="ml-3 font-mono text-[11px] text-ink-faint">
            Orbit — local session
          </span>
        </div>

        <div className="flex min-h-[380px]">
          {/* Sidebar */}
          <div className="hidden w-40 shrink-0 border-r border-line bg-base-900/60 p-3 sm:block">
            <div className="flex flex-col gap-1">
              {SIDEBAR_ITEMS.map(({ icon: Icon, label, active }) => (
                <div
                  key={label}
                  className={`flex items-center gap-2 rounded-md px-2.5 py-2 text-xs ${
                    active
                      ? "bg-accent/15 text-ink"
                      : "text-ink-muted"
                  }`}
                >
                  <Icon className="h-3.5 w-3.5" strokeWidth={2} />
                  {label}
                </div>
              ))}
            </div>

            <div className="mt-6 rounded-md border border-line/80 bg-base-800/50 p-2.5">
              <p className="mb-1.5 font-mono text-[10px] uppercase tracking-wide text-ink-faint">
                Loaded
              </p>
              <div className="flex items-center gap-1.5 truncate text-[11px] text-ink-muted">
                <FileText className="h-3 w-3 shrink-0" />
                DBMS_Notes.pdf
              </div>
            </div>
          </div>

          {/* Main chat area */}
          <div className="flex flex-1 flex-col p-4 sm:p-5">
            <h3 className="font-display text-sm font-semibold text-ink">
              Ask your documents
            </h3>

            <div className="mt-4 flex flex-1 flex-col gap-3">
              <div className="ml-auto max-w-[80%] rounded-lg rounded-tr-sm bg-base-800 px-3.5 py-2.5 text-[13px] text-ink">
                What is 2NF?
              </div>

              <div className="max-w-[88%] rounded-lg rounded-tl-sm border border-line bg-base-800/50 px-3.5 py-3 text-[13px] leading-relaxed text-ink-muted">
                <div className="mb-1.5 flex items-center gap-1.5 text-accent-soft">
                  <Sparkles className="h-3.5 w-3.5" />
                  <span className="font-mono text-[10px] uppercase tracking-wide">
                    Local model
                  </span>
                </div>
                <p className="text-ink">
                  2NF (Second Normal Form) requires a table to be in 1NF and
                  removes partial dependencies on a candidate key.
                </p>
                <div className="mt-3 flex items-center gap-2 border-t border-line/70 pt-2.5">
                  <span className="font-mono text-[10px] uppercase tracking-wide text-ink-faint">
                    Sources
                  </span>
                  <span className="rounded border border-line bg-base-900 px-1.5 py-0.5 font-mono text-[10px] text-ink-muted">
                    DBMS_Notes.pdf · Page 14
                  </span>
                </div>
              </div>
            </div>

            <div className="mt-4 flex items-center gap-2 rounded-md border border-line bg-base-800/60 px-3 py-2.5">
              <span className="flex-1 truncate text-[13px] text-ink-faint">
                Ask a question about your documents…
              </span>
              <SendHorizontal className="h-4 w-4 text-ink-faint" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
