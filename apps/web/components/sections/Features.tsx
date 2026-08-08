'use client';

import { useScrollAnimate } from '@/lib/use-scroll-animate';

const features = [
  {
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="h-6 w-6">
        <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7S2 12 2 12z" />
        <circle cx="12" cy="12" r="3" />
      </svg>
    ),
    title: 'Smart Monitoring',
    description:
      'Optional webcam-based blink estimation processed entirely on your device. Camera is optional, recording is off by default.',
  },
  {
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="h-6 w-6">
        <circle cx="12" cy="12" r="10" />
        <path d="M12 6v6l4 2" />
      </svg>
    ),
    title: 'Focus & Break Timer',
    description:
      'Camera-free focus sessions with configurable break reminders. 20-20-20 style or custom durations.',
  },
  {
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="h-6 w-6">
        <path d="M12 2a10 10 0 100 20 10 10 0 000-20z" />
        <path d="M8 14s1.5 2 4 2 4-2 4-2" />
        <path d="M9 9h.01M15 9h.01" />
      </svg>
    ),
    title: 'Eye Care Exercises',
    description:
      'Short guided visual-rest activities you can do at your desk. Gentle blinking, distance viewing, and more.',
  },
  {
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="h-6 w-6">
        <path d="M3 3v18h18" />
        <path d="M7 16l4-8 4 4 4-6" />
      </svg>
    ),
    title: 'Statistics & Insights',
    description:
      'Understand your screen-use patterns with daily, weekly, and monthly trends. All data stays on your device.',
  },
  {
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="h-6 w-6">
        <rect x="3" y="11" width="18" height="11" rx="2" />
        <path d="M7 11V7a5 5 0 0110 0v4" />
      </svg>
    ),
    title: 'Privacy First',
    description:
      'No cloud account required. No webcam uploads. Local SQLite storage. Export or delete your data at any time.',
  },
  {
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="h-6 w-6">
        <path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z" />
        <path d="M3.27 6.96L12 12.01l8.73-5.05M12 22.08V12" />
      </svg>
    ),
    title: 'Cross-Platform',
    description:
      'Built for macOS 13+ and Windows 10/11. Install without Python, Node.js, or any development tools.',
  },
];

export function Features() {
  const sectionRef = useScrollAnimate();

  return (
    <section id="features" className="relative py-[var(--spacing-section)]">
      <div className="mx-auto max-w-6xl px-6" ref={sectionRef} data-animate>
        {/* Section header */}
        <div className="mx-auto max-w-2xl text-center">
          <span className="label text-[var(--color-accent)]">Features</span>
          <h2 className="heading-2 mt-4 text-[var(--color-fg-primary)]">
            Everything you need for healthier screen habits
          </h2>
          <p className="body-large mt-4 text-[var(--color-fg-secondary)]">
            A complete toolkit for your eyes, designed to work quietly in the
            background without interrupting your flow.
          </p>
        </div>

        {/* Feature grid */}
        <div className="mt-10 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {features.map((feature) => (
            <div
              key={feature.title}
              className="group rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-bg-surface)] p-6 transition-all duration-300 hover:border-[var(--color-accent)]/20 hover:bg-[var(--color-bg-elevated)]"
            >
              <div className="flex h-10 w-10 items-center justify-center rounded-[var(--radius-md)] bg-[var(--color-accent)]/10 text-[var(--color-accent)] transition-colors group-hover:bg-[var(--color-accent)]/15">
                {feature.icon}
              </div>
              <h3 className="heading-3 mt-4 text-[var(--color-fg-primary)]">
                {feature.title}
              </h3>
              <p className="body-small mt-2 text-[var(--color-fg-secondary)]">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
