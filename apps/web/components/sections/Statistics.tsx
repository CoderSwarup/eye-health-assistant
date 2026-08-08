'use client';

import { useScrollAnimate } from '@/lib/use-scroll-animate';

export function Statistics() {
  const sectionRef = useScrollAnimate();

  return (
    <section className="relative py-[var(--spacing-section)]">
      <div className="mx-auto max-w-6xl px-6" ref={sectionRef} data-animate>
        <div className="grid items-center gap-16 lg:grid-cols-2">
          {/* Left — text */}
          <div>
            <span className="label text-[var(--color-accent)]">Statistics</span>
            <h2 className="heading-2 mt-4 text-[var(--color-fg-primary)]">
              Understand your screen-use patterns
            </h2>
            <p className="body-large mt-4 text-[var(--color-fg-secondary)]">
              Daily, weekly, and monthly insights help you build better habits over
              time. All data stays on your device.
            </p>

            <div className="mt-8 grid grid-cols-2 gap-4">
              {[
                { label: 'Screen Time', value: '4h 32m' },
                { label: 'Avg Blink Rate', value: '16/min' },
                { label: 'Breaks Taken', value: '7 / 8' },
                { label: 'Exercises', value: '3 today' },
              ].map((stat) => (
                <div
                  key={stat.label}
                  className="rounded-[var(--radius-md)] bg-[var(--color-bg-surface)] p-4"
                >
                  <div className="caption text-[var(--color-fg-muted)]">{stat.label}</div>
                  <div className="mt-1 text-xl font-bold text-[var(--color-fg-primary)]">
                    {stat.value}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Right — chart */}
          <div className="relative">
            <div className="absolute -inset-8 rounded-[var(--radius-xl)] bg-[var(--color-accent)]/[0.04] blur-2xl" />
            <div className="relative rounded-[var(--radius-xl)] border border-[var(--color-border-strong)] bg-[var(--color-bg-surface)] p-6">
              <div className="mb-4 flex items-center justify-between">
                <span className="text-sm font-medium text-[var(--color-fg-primary)]">
                  Weekly Trends
                </span>
                <span className="caption text-[var(--color-fg-muted)]">This week</span>
              </div>

              {/* Chart bars */}
              <div className="space-y-3">
                {[
                  { day: 'Mon', hours: 6.5, max: 10 },
                  { day: 'Tue', hours: 8.2, max: 10 },
                  { day: 'Wed', hours: 5.8, max: 10 },
                  { day: 'Thu', hours: 7.1, max: 10 },
                  { day: 'Fri', hours: 6.9, max: 10 },
                  { day: 'Sat', hours: 3.2, max: 10 },
                  { day: 'Sun', hours: 2.1, max: 10 },
                ].map((d) => (
                  <div key={d.day} className="flex items-center gap-3">
                    <span className="w-8 text-xs text-[var(--color-fg-muted)]">{d.day}</span>
                    <div className="h-2 flex-1 overflow-hidden rounded-full bg-[var(--color-bg-elevated)]">
                      <div
                        className="h-full rounded-full bg-[var(--color-accent)]/60 transition-all duration-700"
                        style={{ width: `${(d.hours / d.max) * 100}%` }}
                      />
                    </div>
                    <span className="w-12 text-right text-xs text-[var(--color-fg-muted)]">
                      {d.hours}h
                    </span>
                  </div>
                ))}
              </div>

              {/* Insight */}
              <div className="mt-6 rounded-[var(--radius-md)] bg-[var(--color-accent)]/5 p-4">
                <div className="flex items-start gap-2">
                  <svg
                    viewBox="0 0 16 16"
                    fill="currentColor"
                    className="mt-0.5 h-3.5 w-3.5 shrink-0 text-[var(--color-accent)]"
                  >
                    <path d="M8 0a8 8 0 110 16A8 8 0 018 0zm.75 4.75a.75.75 0 00-1.5 0v3.5a.75.75 0 00.37.65l2.5 1.5a.75.75 0 10.76-1.3L8.75 7.94V4.75z" />
                  </svg>
                  <p className="text-xs leading-relaxed text-[var(--color-fg-secondary)]">
                    Your longest screen sessions usually happen on Tuesday mornings.
                    Consider setting earlier break reminders on those days.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
