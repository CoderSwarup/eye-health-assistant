'use client';

import { useScrollAnimate } from '@/lib/use-scroll-animate';

const privacyPoints = [
  {
    title: 'No account required',
    description: 'Download, install, and start using immediately. No signup, no email, no cloud.',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="h-5 w-5">
        <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" />
        <circle cx="12" cy="7" r="4" />
      </svg>
    ),
  },
  {
    title: 'Local SQLite storage',
    description: 'All your data — sessions, history, settings — lives in a local database on your device.',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="h-5 w-5">
        <ellipse cx="12" cy="5" rx="9" ry="3" />
        <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3" />
        <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" />
      </svg>
    ),
  },
  {
    title: 'No webcam uploads',
    description: 'Camera processing happens entirely on your device. No frames ever leave your machine.',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="h-5 w-5">
        <path d="M23 7l-7 5 7 5V7z" />
        <rect x="1" y="5" width="15" height="14" rx="2" />
        <path d="M1 1l22 22" />
      </svg>
    ),
  },
  {
    title: 'Export and delete',
    description: 'Export your data as JSON or CSV, or delete everything with one click. You are always in control.',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="h-5 w-5">
        <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4" />
        <polyline points="7 10 12 15 17 10" />
        <line x1="12" y1="15" x2="12" y2="3" />
      </svg>
    ),
  },
];

export function Privacy() {
  const sectionRef = useScrollAnimate();

  return (
    <section id="privacy" className="relative py-[var(--spacing-section)]">
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute left-1/2 top-0 h-[400px] w-[600px] -translate-x-1/2 rounded-full bg-[var(--color-accent)]/[0.03] blur-[120px]" />
      </div>

      <div className="relative mx-auto max-w-6xl px-6" ref={sectionRef} data-animate>
        <div className="mx-auto max-w-2xl text-center">
          <span className="label text-[var(--color-accent)]">Privacy</span>
          <h2 className="heading-2 mt-4 text-[var(--color-fg-primary)]">
            Your data stays on your device
          </h2>
          <p className="body-large mt-4 text-[var(--color-fg-secondary)]">
            Privacy is not a feature — it is the foundation. Every piece of data
            stays on your machine. No exceptions.
          </p>
        </div>

        <div className="mt-10 grid gap-6 md:grid-cols-2">
          {privacyPoints.map((point) => (
            <div
              key={point.title}
              className="group flex items-start gap-4 rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-bg-surface)] p-6 transition-all duration-300 hover:border-[var(--color-accent)]/20 hover:bg-[var(--color-bg-elevated)]"
            >
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-[var(--radius-md)] bg-[var(--color-accent)]/10 text-[var(--color-accent)]">
                {point.icon}
              </div>
              <div>
                <h3 className="text-sm font-semibold text-[var(--color-fg-primary)]">
                  {point.title}
                </h3>
                <p className="body-small mt-1 text-[var(--color-fg-secondary)]">
                  {point.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
