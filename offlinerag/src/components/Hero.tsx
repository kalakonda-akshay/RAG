import { motion } from "framer-motion";
import { ArrowRight, Github, ShieldCheck } from "lucide-react";
import { APP_CONFIG } from "../config/app";
import ParticleField from "./ParticleField";
import AppMockup from "./AppMockup";

const fadeUp = {
  hidden: { opacity: 0, y: 18 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.12, duration: 0.7, ease: [0.16, 1, 0.3, 1] },
  }),
};

const BADGES = [
  "Windows 10 / 11",
  `Latest Version: v${APP_CONFIG.version}`,
  "No API Key Required",
  "Works Offline",
];

export default function Hero() {
  return (
    <section id="top" className="relative overflow-hidden bg-black pt-16">
      <div className="absolute inset-0">
        <ParticleField />
      </div>

      <div className="relative mx-auto grid max-w-7xl grid-cols-1 gap-14 px-5 pb-20 pt-16 sm:px-8 sm:pt-24 lg:grid-cols-2 lg:items-center lg:pb-28 lg:pt-28">
        <div>
          <motion.div
            custom={0}
            variants={fadeUp}
            initial="hidden"
            animate="visible"
            className="mb-6 inline-flex items-center gap-2 rounded-full border border-line bg-base-900/60 px-3.5 py-1.5 backdrop-blur"
          >
            <ShieldCheck className="h-3.5 w-3.5 text-accent-soft" />
            <span className="text-xs font-medium text-ink-muted">
              Local-first document intelligence
            </span>
          </motion.div>

          <motion.h1
            custom={1}
            variants={fadeUp}
            initial="hidden"
            animate="visible"
            className="font-display text-4xl font-semibold leading-[1.08] tracking-tight text-ink sm:text-5xl lg:text-6xl"
          >
            Your Documents.
            <br />
            Your Computer.
            <br />
            <span className="bg-gradient-to-r from-accent-soft to-accent-violet bg-clip-text text-transparent">
              Your Data.
            </span>
          </motion.h1>

          <motion.p
            custom={2}
            variants={fadeUp}
            initial="hidden"
            animate="visible"
            className="mt-6 max-w-xl text-base leading-relaxed text-ink-muted sm:text-lg"
          >
            A completely offline RAG assistant for asking questions about
            your documents — powered locally on your own machine.
          </motion.p>

          <motion.div
            custom={3}
            variants={fadeUp}
            initial="hidden"
            animate="visible"
            className="mt-8 flex flex-col gap-3 sm:flex-row"
          >
            <a
              href={APP_CONFIG.downloadUrl}
              className="focus-ring group flex items-center justify-center gap-2 rounded-md bg-accent px-6 py-3 text-sm font-medium text-white transition-colors hover:bg-accent-soft"
            >
              Download for Windows
              <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
            </a>
            <a
              href={APP_CONFIG.githubUrl}
              target="_blank"
              rel="noreferrer"
              className="focus-ring flex items-center justify-center gap-2 rounded-md border border-line bg-base-900/60 px-6 py-3 text-sm font-medium text-ink transition-colors hover:border-accent/40"
            >
              <Github className="h-4 w-4" />
              View on GitHub
            </a>
          </motion.div>

          <motion.div
            custom={4}
            variants={fadeUp}
            initial="hidden"
            animate="visible"
            className="mt-6 flex flex-wrap gap-x-5 gap-y-2"
          >
            {BADGES.map((badge) => (
              <span
                key={badge}
                className="font-mono text-[11px] uppercase tracking-wide text-ink-faint"
              >
                {badge}
              </span>
            ))}
          </motion.div>

          <motion.p
            custom={5}
            variants={fadeUp}
            initial="hidden"
            animate="visible"
            className="mt-6 text-sm text-ink-muted"
          >
            <span className="text-ink">
              Your documents never need to leave your computer.
            </span>
          </motion.p>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.35, duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
        >
          <AppMockup />
        </motion.div>
      </div>
    </section>
  );
}
