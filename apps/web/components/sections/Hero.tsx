'use client';

import { siteConfig } from '@/lib/site-config';

export function Hero() {
  return (
    <section className="relative min-h-screen overflow-hidden pt-24">
      {/* Ambient background */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute left-1/2 top-0 h-[600px] w-[800px] -translate-x-1/2 rounded-full bg-[var(--color-accent)]/[0.04] blur-[120px]" />
        <div className="absolute bottom-0 left-1/4 h-[400px] w-[400px] rounded-full bg-[var(--color-accent)]/[0.03] blur-[100px]" />
      </div>

      <div className="relative mx-auto max-w-6xl px-6 pb-24 pt-20 md:pt-32">
        {/* Badge */}
        <div className="animate-fade-in-up flex justify-center">
          <div className="glass inline-flex items-center gap-2 rounded-full px-4 py-1.5">
            <span className="h-1.5 w-1.5 rounded-full bg-[var(--color-success)]" />
            <span className="caption text-[var(--color-fg-secondary)]">
              Privacy-first desktop app
            </span>
          </div>
        </div>

        {/* Headline */}
        <h1 className="display mx-auto mt-8 max-w-4xl text-center text-[var(--color-fg-primary)] animate-fade-in-up delay-100">
          A calmer way to{' '}
          <span className="text-gradient">work at a screen</span>
        </h1>

        {/* Subheadline */}
        <p className="body-large mx-auto mt-6 max-w-2xl text-center text-[var(--color-fg-secondary)] animate-fade-in-up delay-200">
          {siteConfig.name} helps you build healthier screen habits with intelligent
          reminders, optional eye tracking, guided exercises, and private local
          statistics.
        </p>

        {/* CTAs */}
        <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row animate-fade-in-up delay-300">
          <a
            href="#download"
            className="group relative inline-flex items-center gap-2 rounded-[var(--radius-lg)] bg-[var(--color-accent)] px-7 py-3.5 text-sm font-medium text-[var(--color-fg-inverse)] transition-all hover:bg-[var(--color-accent-light)] hover:shadow-[0_0_30px_var(--color-accent-glow)]"
          >
            Download for Mac
            <svg
              viewBox="0 0 16 16"
              fill="currentColor"
              className="h-4 w-4 transition-transform group-hover:translate-x-0.5"
            >
              <path d="M6.22 3.22a.75.75 0 011.06 0l4.25 4.25a.75.75 0 010 1.06l-4.25 4.25a.75.75 0 01-1.06-1.06L9.94 8 6.22 4.28a.75.75 0 010-1.06z" />
            </svg>
          </a>
          <a
            href={siteConfig.social.github}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 rounded-[var(--radius-lg)] border border-[var(--color-border-strong)] px-7 py-3.5 text-sm font-medium text-[var(--color-fg-secondary)] transition-all hover:border-[var(--color-fg-muted)] hover:text-[var(--color-fg-primary)]"
          >
            View on GitHub
          </a>
        </div>

        {/* Platform info */}
        <p className="mt-6 text-center text-xs text-[var(--color-fg-muted)] animate-fade-in-up delay-400">
          {siteConfig.platforms.macos} &middot; {siteConfig.platforms.windows} &middot; Free &amp; open source
        </p>

        {/* Product Visual — Mockup Dashboard */}
        <div className="mt-16 animate-scale-in delay-500">
          <div className="relative mx-auto max-w-4xl">
            {/* Glow behind */}
            <div className="absolute -inset-4 rounded-[var(--radius-xl)] bg-[var(--color-accent)]/[0.06] blur-2xl" />

            {/* Window chrome */}
            <div className="relative overflow-hidden rounded-[var(--radius-xl)] border border-[var(--color-border-strong)] bg-[var(--color-bg-surface)]">
              {/* Title bar */}
              <div className="flex items-center gap-2 border-b border-[var(--color-border)] px-4 py-3">
                <div className="h-3 w-3 rounded-full bg-[#ff5f57]" />
                <div className="h-3 w-3 rounded-full bg-[#febc2e]" />
                <div className="h-3 w-3 rounded-full bg-[#28c840]" />
                <span className="ml-3 text-xs text-[var(--color-fg-muted)]">
                  Eye Health Assistant
                </span>
              </div>

              {/* Dashboard content */}
              <div className="flex">
                {/* Sidebar */}
                <div className="hidden w-48 border-r border-[var(--color-border)] p-4 md:block">
                  <div className="space-y-1">
                    {['Dashboard', 'Live Monitoring', 'Exercises', 'Eye Care', 'Statistics', 'Settings'].map(
                      (item, i) => (
                        <div
                          key={item}
                          className={`rounded-[var(--radius-md)] px-3 py-2 text-xs ${
                            i === 0
                              ? 'bg-[var(--color-accent)]/10 text-[var(--color-accent)]'
                              : 'text-[var(--color-fg-muted)]'
                          }`}
                        >
                          {item}
                        </div>
                      )
                    )}
                  </div>
                </div>

                {/* Main content */}
                <div className="flex-1 p-6">
                  <div className="mb-6 text-sm font-semibold text-[var(--color-fg-primary)]">
                    Dashboard
                  </div>

                  {/* Metric cards */}
                  <div className="mb-4 grid grid-cols-2 gap-3 md:grid-cols-4">
                    {[
                      { label: 'Screen Time', value: '2h 45m', accent: false },
                      { label: 'Blink Rate', value: '16/min', accent: true },
                      { label: 'Breaks', value: '4/5', accent: false },
                      { label: 'Score', value: '82', accent: true },
                    ].map((m) => (
                      <div
                        key={m.label}
                        className="rounded-[var(--radius-md)] bg-[var(--color-bg-elevated)] p-3"
                      >
                        <div className="caption text-[var(--color-fg-muted)]">
                          {m.label}
                        </div>
                        <div
                          className={`mt-1 text-lg font-bold ${
                            m.accent
                              ? 'text-[var(--color-accent)]'
                              : 'text-[var(--color-fg-primary)]'
                          }`}
                        >
                          {m.value}
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Chart placeholder */}
                  <div className="rounded-[var(--radius-md)] bg-[var(--color-bg-elevated)] p-4">
                    <div className="mb-3 text-xs text-[var(--color-fg-muted)]">
                      Weekly Activity
                    </div>
                    <div className="flex items-end gap-1.5" style={{ height: 80 }}>
                      {[40, 65, 55, 80, 70, 45, 60].map((h, i) => (
                        <div
                          key={i}
                          className="flex-1 rounded-sm bg-[var(--color-accent)]/20 transition-all hover:bg-[var(--color-accent)]/40"
                          style={{ height: `${h}%` }}
                        />
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
