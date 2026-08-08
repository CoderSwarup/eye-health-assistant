'use client';

import { siteConfig } from '@/lib/site-config';
import { useScrollAnimate } from '@/lib/use-scroll-animate';

export function DownloadCTA() {
  const sectionRef = useScrollAnimate();

  return (
    <section id="download" className="relative py-[var(--spacing-section)]">
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute left-1/2 top-1/2 h-[500px] w-[800px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-[var(--color-accent)]/[0.05] blur-[150px]" />
      </div>

      <div className="relative mx-auto max-w-3xl px-6 text-center" ref={sectionRef} data-animate>
        <h2 className="heading-1 text-[var(--color-fg-primary)]">
          Take a better break.
        </h2>
        <p className="body-large mx-auto mt-4 max-w-xl text-[var(--color-fg-secondary)]">
          Build healthier screen habits without giving up your privacy.
          Free, open source, and local-first.
        </p>

        <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
          <a
            href={siteConfig.download.macos}
            className="group inline-flex items-center gap-2 rounded-[var(--radius-lg)] bg-[var(--color-accent)] px-8 py-4 text-sm font-medium text-[var(--color-fg-inverse)] transition-all hover:bg-[var(--color-accent-light)] hover:shadow-[0_0_40px_var(--color-accent-glow-strong)]"
          >
            <svg viewBox="0 0 24 24" fill="currentColor" className="h-4 w-4">
              <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.8-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z" />
            </svg>
            Download for Mac
          </a>
          <a
            href={siteConfig.download.windows}
            className="inline-flex items-center gap-2 rounded-[var(--radius-lg)] border border-[var(--color-border-strong)] px-8 py-4 text-sm font-medium text-[var(--color-fg-secondary)] transition-all hover:border-[var(--color-fg-muted)] hover:text-[var(--color-fg-primary)]"
          >
            <svg viewBox="0 0 24 24" fill="currentColor" className="h-4 w-4">
              <path d="M0 3.449L9.75 2.1v9.451H0m10.949-9.602L24 0v11.4H10.949M0 12.6h9.75v9.451L0 20.699M10.949 12.6H24V24l-12.9-1.801" />
            </svg>
            Download for Windows
          </a>
        </div>

        <p className="mt-6 text-xs text-[var(--color-fg-muted)]">
          {siteConfig.platforms.macos} &middot; {siteConfig.platforms.windows} &middot; Free &amp; open source
        </p>
      </div>
    </section>
  );
}
