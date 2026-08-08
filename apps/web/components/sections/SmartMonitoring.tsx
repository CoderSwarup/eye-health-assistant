'use client';

import { useScrollAnimate } from '@/lib/use-scroll-animate';

const steps = [
  {
    step: '01',
    title: 'Camera',
    description: 'Optional webcam access — you choose when to enable it.',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="h-5 w-5">
        <path d="M23 7l-7 5 7 5V7z" />
        <rect x="1" y="5" width="15" height="14" rx="2" />
      </svg>
    ),
  },
  {
    step: '02',
    title: 'Local Processing',
    description: 'All computation happens on your device using OpenCV and MediaPipe.',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="h-5 w-5">
        <rect x="4" y="4" width="16" height="16" rx="2" />
        <path d="M9 9h6v6H9z" />
      </svg>
    ),
  },
  {
    step: '03',
    title: 'Eye Landmarks',
    description: 'Facial landmarks detected to estimate eye openness and blink patterns.',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="h-5 w-5">
        <circle cx="12" cy="12" r="3" />
        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8S1 12 1 12z" />
      </svg>
    ),
  },
  {
    step: '04',
    title: 'Blink Estimation',
    description: 'Estimated blink rate calculated from a rolling observation window.',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="h-5 w-5">
        <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7S2 12 2 12z" />
        <path d="M12 8v4l2 2" />
      </svg>
    ),
  },
  {
    step: '05',
    title: 'Private Metrics',
    description: 'Wellness insights stored locally. Never uploaded. You control everything.',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="h-5 w-5">
        <rect x="3" y="11" width="18" height="11" rx="2" />
        <path d="M7 11V7a5 5 0 0110 0v4" />
      </svg>
    ),
  },
];

export function SmartMonitoring() {
  const sectionRef = useScrollAnimate();

  return (
    <section className="relative py-[var(--spacing-section)]">
      {/* Subtle background accent */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute right-0 top-1/4 h-[500px] w-[500px] rounded-full bg-[var(--color-accent)]/[0.03] blur-[120px]" />
      </div>

      <div className="relative mx-auto max-w-6xl px-6" ref={sectionRef} data-animate>
        <div className="grid items-center gap-16 lg:grid-cols-2">
          {/* Left — text */}
          <div>
            <span className="label text-[var(--color-accent)]">Smart Mode</span>
            <h2 className="heading-2 mt-4 text-[var(--color-fg-primary)]">
              Optional camera monitoring,
              <br />
              <span className="text-[var(--color-fg-secondary)]">always local, always private</span>
            </h2>
            <p className="body-large mt-4 text-[var(--color-fg-secondary)]">
              When enabled, Eye Health Assistant uses your webcam to estimate blink
              patterns and screen-use signals. Every frame is processed locally and
              never stored or uploaded.
            </p>

            <div className="mt-6 flex flex-wrap gap-3">
              {['Camera is optional', 'No recording by default', 'No cloud upload'].map(
                (tag) => (
                  <span
                    key={tag}
                    className="glass inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs text-[var(--color-fg-secondary)]"
                  >
                    <span className="h-1 w-1 rounded-full bg-[var(--color-success)]" />
                    {tag}
                  </span>
                )
              )}
            </div>
          </div>

          {/* Right — pipeline visualization */}
          <div className="relative">
            <div className="absolute -inset-8 rounded-[var(--radius-xl)] bg-[var(--color-accent)]/[0.04] blur-2xl" />
            <div className="relative space-y-3">
              {steps.map((step, i) => (
                <div
                  key={step.step}
                  className="group flex items-start gap-4 rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-bg-surface)] p-5 transition-all duration-300 hover:border-[var(--color-accent)]/20 hover:bg-[var(--color-bg-elevated)]"
                >
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-[var(--radius-md)] bg-[var(--color-accent)]/10 text-[var(--color-accent)]">
                    {step.icon}
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="caption font-mono text-[var(--color-accent)]">
                        {step.step}
                      </span>
                      <h4 className="text-sm font-semibold text-[var(--color-fg-primary)]">
                        {step.title}
                      </h4>
                    </div>
                    <p className="body-small mt-1 text-[var(--color-fg-secondary)]">
                      {step.description}
                    </p>
                  </div>
                  {i < steps.length - 1 && (
                    <div className="absolute left-[2.45rem] mt-14 h-3 w-px bg-[var(--color-border-strong)]" />
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
