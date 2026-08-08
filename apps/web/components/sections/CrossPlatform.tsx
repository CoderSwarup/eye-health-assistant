'use client';

import { useScrollAnimate } from '@/lib/use-scroll-animate';

export function CrossPlatform() {
  const sectionRef = useScrollAnimate();

  return (
    <section className="relative py-[var(--spacing-section)]">
      <div className="mx-auto max-w-6xl px-6" ref={sectionRef} data-animate>
        <div className="mx-auto max-w-2xl text-center">
          <span className="label text-[var(--color-accent)]">Cross-Platform</span>
          <h2 className="heading-2 mt-4 text-[var(--color-fg-primary)]">
            Built for your desktop
          </h2>
          <p className="body-large mt-4 text-[var(--color-fg-secondary)]">
            Install once, use everywhere. No Python, no Node.js, no terminal required.
          </p>
        </div>

        <div className="mt-12 flex flex-col items-center justify-center gap-6 sm:flex-row">
          {/* macOS */}
          <div className="flex items-center gap-4 rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-bg-surface)] px-8 py-6 transition-all duration-300 hover:border-[var(--color-accent)]/20">
            <svg viewBox="0 0 24 24" fill="currentColor" className="h-8 w-8 text-[var(--color-fg-secondary)]">
              <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.8-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z" />
            </svg>
            <div>
              <div className="text-sm font-semibold text-[var(--color-fg-primary)]">macOS</div>
              <div className="caption text-[var(--color-fg-muted)]">13+ (Universal)</div>
            </div>
          </div>

          {/* Windows */}
          <div className="flex items-center gap-4 rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-bg-surface)] px-8 py-6 transition-all duration-300 hover:border-[var(--color-accent)]/20">
            <svg viewBox="0 0 24 24" fill="currentColor" className="h-8 w-8 text-[var(--color-fg-secondary)]">
              <path d="M0 3.449L9.75 2.1v9.451H0m10.949-9.602L24 0v11.4H10.949M0 12.6h9.75v9.451L0 20.699M10.949 12.6H24V24l-12.9-1.801" />
            </svg>
            <div>
              <div className="text-sm font-semibold text-[var(--color-fg-primary)]">Windows</div>
              <div className="caption text-[var(--color-fg-muted)]">10 / 11 (x64)</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
