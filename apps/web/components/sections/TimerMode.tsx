'use client';

import { useScrollAnimate } from '@/lib/use-scroll-animate';

export function TimerMode() {
  const sectionRef = useScrollAnimate();

  return (
    <section className="relative py-[var(--spacing-section)]">
      <div className="mx-auto max-w-6xl px-6" ref={sectionRef} data-animate>
        <div className="grid items-center gap-16 lg:grid-cols-2">
          {/* Left — visual */}
          <div className="order-2 lg:order-1">
            <div className="relative mx-auto max-w-sm">
              <div className="absolute -inset-8 rounded-[var(--radius-xl)] bg-[var(--color-accent)]/[0.04] blur-2xl" />
              <div className="relative rounded-[var(--radius-xl)] border border-[var(--color-border-strong)] bg-[var(--color-bg-surface)] p-8">
                {/* Timer display */}
                <div className="text-center">
                  <div className="caption text-[var(--color-fg-muted)]">Focus Session</div>
                  <div className="mt-4 font-mono text-6xl font-bold tracking-tighter text-[var(--color-fg-primary)]">
                    19:42
                  </div>
                  <div className="mt-2 text-sm text-[var(--color-fg-secondary)]">
                    Next break in 19 minutes
                  </div>
                </div>

                {/* Progress */}
                <div className="mt-8 h-1.5 overflow-hidden rounded-full bg-[var(--color-bg-elevated)]">
                  <div
                    className="h-full rounded-full bg-[var(--color-accent)] transition-all"
                    style={{ width: '35%' }}
                  />
                </div>

                {/* Controls */}
                <div className="mt-6 flex justify-center gap-3">
                  <div className="rounded-[var(--radius-md)] bg-[var(--color-accent)]/10 px-4 py-2 text-xs font-medium text-[var(--color-accent)]">
                    Pause
                  </div>
                  <div className="rounded-[var(--radius-md)] bg-[var(--color-bg-elevated)] px-4 py-2 text-xs text-[var(--color-fg-muted)]">
                    Skip
                  </div>
                </div>

                {/* Stats */}
                <div className="mt-6 grid grid-cols-3 gap-4 border-t border-[var(--color-border)] pt-6">
                  {[
                    { label: 'Sessions', value: '3' },
                    { label: 'Breaks', value: '2/3' },
                    { label: 'Streak', value: '5d' },
                  ].map((s) => (
                    <div key={s.label} className="text-center">
                      <div className="text-lg font-bold text-[var(--color-fg-primary)]">
                        {s.value}
                      </div>
                      <div className="caption text-[var(--color-fg-muted)]">{s.label}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Right — text */}
          <div className="order-1 lg:order-2">
            <span className="label text-[var(--color-accent)]">Timer Mode</span>
            <h2 className="heading-2 mt-4 text-[var(--color-fg-primary)]">
              No camera. No tracking.
              <br />
              <span className="text-[var(--color-fg-secondary)]">Just better timing.</span>
            </h2>
            <p className="body-large mt-4 text-[var(--color-fg-secondary)]">
              Start a focus session and receive gentle break reminders at configurable
              intervals. The 20-20-20 rule, customized for your workflow.
            </p>

            <ul className="mt-8 space-y-4">
              {[
                'Configurable focus and break durations',
                '20-20-20 rule or custom presets',
                'Quiet hours for uninterrupted deep work',
                'Notification controls with intensity settings',
                'Works entirely without a camera',
              ].map((item) => (
                <li key={item} className="flex items-start gap-3">
                  <svg
                    viewBox="0 0 16 16"
                    fill="currentColor"
                    className="mt-0.5 h-4 w-4 shrink-0 text-[var(--color-accent)]"
                  >
                    <path d="M8 0a8 8 0 110 16A8 8 0 018 0zm3.28 5.22a.75.75 0 00-1.06 0L7 8.44 5.78 7.22a.75.75 0 00-1.06 1.06l1.75 1.75a.75.75 0 001.06 0l3.75-3.75a.75.75 0 000-1.06z" />
                  </svg>
                  <span className="body-small text-[var(--color-fg-secondary)]">{item}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}
