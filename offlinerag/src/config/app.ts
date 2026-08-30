// ─────────────────────────────────────────────────────────────
// SINGLE SOURCE OF TRUTH for every external link on the site.
// Update the values below and every component picks them up —
// nothing is hardcoded elsewhere.
// ─────────────────────────────────────────────────────────────
export const APP_CONFIG = {
  name: "Orbit",
  tagline: "Offline Multimodal RAG Assistant",
  version: "1.0.0",

  githubUsername: "kalakonda-akshay",
  githubRepo: "RAG",

  get githubUrl() {
    return `https://github.com/${this.githubUsername}/${this.githubRepo}`;
  },
  get releasesUrl() {
    return `${this.githubUrl}/releases`;
  },
  get issuesUrl() {
    return `${this.githubUrl}/issues`;
  },

  downloadUrl: "https://github.com/kalakonda-akshay/RAG/releases/latest/download/OfflineRAGAssistant_Setup.zip",

  platforms: ["Windows 10", "Windows 11"],
} as const;
