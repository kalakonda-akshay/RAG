import { useEffect, useRef } from "react";

/**
 * ParticleField
 * ─────────────
 * The site's signature visual: a live purple particle network on a
 * solid black canvas — matching the reference "Aether Flow" animation.
 * Nodes drift, connect when close, repel gently from the cursor, and
 * their links glow white near the pointer.
 *
 * It doubles as a metaphor for what OfflineRAG actually does: your
 * documents become chunks, chunks become local embeddings, and related
 * pieces link together in a vector space that never leaves your machine.
 *
 * Respects prefers-reduced-motion by rendering a single static frame
 * with no pointer interaction.
 */
export default function ParticleField() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const reduceMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;

    let width = 0;
    let height = 0;
    let dpr = Math.min(window.devicePixelRatio || 1, 2);
    let animationId = 0;

    const mouse = { x: null as number | null, y: null as number | null, radius: 160 };

    type TrailPoint = { x: number; y: number; life: number };
    let trail: TrailPoint[] = [];

    class Particle {
      x: number;
      y: number;
      dx: number;
      dy: number;
      size: number;

      constructor(x: number, y: number, dx: number, dy: number, size: number) {
        this.x = x;
        this.y = y;
        this.dx = dx;
        this.dy = dy;
        this.size = size;
      }

      draw() {
        ctx!.beginPath();
        ctx!.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx!.fillStyle = "rgba(191, 128, 255, 0.85)";
        ctx!.fill();
      }

      update() {
        if (this.x > width || this.x < 0) this.dx = -this.dx;
        if (this.y > height || this.y < 0) this.dy = -this.dy;

        if (mouse.x !== null && mouse.y !== null) {
          const distX = mouse.x - this.x;
          const distY = mouse.y - this.y;
          const dist = Math.hypot(distX, distY);
          if (dist < mouse.radius + this.size) {
            const forceX = distX / dist;
            const forceY = distY / dist;
            const force = (mouse.radius - dist) / mouse.radius;
            this.x -= forceX * force * 4;
            this.y -= forceY * force * 4;
          }
        }

        this.x += this.dx;
        this.y += this.dy;
        this.draw();
      }
    }

    let particles: Particle[] = [];

    function init() {
      particles = [];
      const count = (width * height) / 9500;
      for (let i = 0; i < count; i++) {
        const size = Math.random() * 1.8 + 1;
        const x = Math.random() * (width - size * 2) + size;
        const y = Math.random() * (height - size * 2) + size;
        const dx = (Math.random() - 0.5) * 0.35;
        const dy = (Math.random() - 0.5) * 0.35;
        particles.push(new Particle(x, y, dx, dy, size));
      }
    }

    function resize() {
      const parent = canvas!.parentElement;
      width = parent ? parent.clientWidth : window.innerWidth;
      height = parent ? parent.clientHeight : window.innerHeight;
      canvas!.width = width * dpr;
      canvas!.height = height * dpr;
      canvas!.style.width = `${width}px`;
      canvas!.style.height = `${height}px`;
      ctx!.setTransform(dpr, 0, 0, dpr, 0, 0);
      init();
    }

    function connect() {
      const maxDist = (width / 7) * (height / 7);
      for (let a = 0; a < particles.length; a++) {
        for (let b = a; b < particles.length; b++) {
          const dx = particles[a].x - particles[b].x;
          const dy = particles[a].y - particles[b].y;
          const distSq = dx * dx + dy * dy;

          if (distSq < maxDist) {
            const opacity = 1 - distSq / 22000;
            if (opacity <= 0) continue;

            let nearMouse = false;
            if (mouse.x !== null && mouse.y !== null) {
              const dm = Math.hypot(particles[a].x - mouse.x, particles[a].y - mouse.y);
              nearMouse = dm < mouse.radius;
            }

            ctx!.strokeStyle = nearMouse
              ? `rgba(255, 255, 255, ${Math.min(opacity, 1)})`
              : `rgba(200, 150, 255, ${Math.min(opacity, 0.5)})`;
            ctx!.lineWidth = 1;
            ctx!.beginPath();
            ctx!.moveTo(particles[a].x, particles[a].y);
            ctx!.lineTo(particles[b].x, particles[b].y);
            ctx!.stroke();
          }
        }
      }
    }

    function drawTrail() {
      for (let i = trail.length - 1; i >= 0; i--) {
        const t = trail[i];
        t.life -= 0.045;
        if (t.life <= 0) {
          trail.splice(i, 1);
          continue;
        }
        const radius = t.life * 5.5;
        const gradient = ctx!.createRadialGradient(
          t.x,
          t.y,
          0,
          t.x,
          t.y,
          radius
        );
        gradient.addColorStop(0, `rgba(216, 180, 255, ${t.life * 0.9})`);
        gradient.addColorStop(1, "rgba(216, 180, 255, 0)");
        ctx!.beginPath();
        ctx!.arc(t.x, t.y, radius, 0, Math.PI * 2);
        ctx!.fillStyle = gradient;
        ctx!.fill();
      }
    }

    function drawFrame() {
      ctx!.fillStyle = "#000000";
      ctx!.fillRect(0, 0, width, height);
      for (const p of particles) p.update();
      connect();
      drawTrail();
    }

    function animate() {
      animationId = requestAnimationFrame(animate);
      drawFrame();
    }

    resize();
    if (reduceMotion) {
      drawFrame();
    } else {
      animate();
    }

    const onResize = () => {
      resize();
      if (reduceMotion) drawFrame();
    };
    // Listen on the window (not the canvas) so the effect still tracks the
    // cursor even while it's over the headline, buttons, or app mockup that
    // sit visually on top of the canvas.
    const onMouseMove = (e: MouseEvent) => {
      const rect = canvas!.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const inside = x >= 0 && x <= width && y >= 0 && y <= height;

      if (inside) {
        mouse.x = x;
        mouse.y = y;
        trail.push({ x, y, life: 1 });
        if (trail.length > 40) trail.shift();
      } else {
        mouse.x = null;
        mouse.y = null;
      }
    };
    const onMouseLeave = () => {
      mouse.x = null;
      mouse.y = null;
    };

    window.addEventListener("resize", onResize);
    if (!reduceMotion) {
      window.addEventListener("mousemove", onMouseMove);
      window.addEventListener("mouseout", onMouseLeave);
    }

    return () => {
      window.removeEventListener("resize", onResize);
      window.removeEventListener("mousemove", onMouseMove);
      window.removeEventListener("mouseout", onMouseLeave);
      cancelAnimationFrame(animationId);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      aria-hidden="true"
      className="absolute inset-0 h-full w-full"
    />
  );
}
