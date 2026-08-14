// ─────────────────────────────────────────────────────────────
// SINGLE SOURCE OF TRUTH for every external link on the site.
// Update the values below and every component picks them up —
// nothing is hardcoded elsewhere.
// ─────────────────────────────────────────────────────────────
export const APP_CONFIG = {
  name: "OfflineRAG",
  tagline: "Private knowledge. Local intelligence.",
  version: "1.0.0",

  // REPLACE: your GitHub username/org and repo name
  githubUsername: "YOUR_USERNAME",
  githubRepo: "OfflineRAG",

  get githubUrl() {
    return `https://github.com/${this.githubUsername}/${this.githubRepo}`;
  },
  get releasesUrl() {
    return `${this.githubUrl}/releases`;
  },
  get issuesUrl() {
    return `${this.githubUrl}/issues`;
  },

  // REPLACE: once a release exists, point this straight at the .exe asset,
  // e.g. `${githubUrl}/releases/download/v1.0.0/OfflineRAG-Setup-1.0.0.exe`
  downloadUrl: "#download",

  platforms: ["Windows 10", "Windows 11"],
} as const;
