'use client';

import { useScrollAnimate } from '@/lib/use-scroll-animate';

const steps = [
  {
    number: '01',
    title: 'Choose your mode',
    description:
      'Pick Smart Mode for camera-based monitoring or Timer Mode for camera-free focus sessions.',
  },
  {
    number: '02',
    title: 'Work normally',
    description:
      'Eye Health Assistant runs quietly in the background while you code, design, study, or browse.',
  },
  {
    number: '03',
    title: 'Get gentle reminders',
    description:
      'Receive timely notifications to take breaks, do eye exercises, or simply rest your eyes.',
  },
  {
    number: '04',
    title: 'Understand your habits',
    description:
      'Review your daily and weekly statistics to build healthier screen-use patterns over time.',
  },
];

export function HowItWorks() {
  const sectionRef = useScrollAnimate();

  return (
    <section id="how-it-works" className="relative py-[var(--spacing-section)]">
      <div className="mx-auto max-w-6xl px-6" ref={sectionRef} data-animate>
        <div className="mx-auto max-w-2xl text-center">
          <span className="label text-[var(--color-accent)]">How It Works</span>
          <h2 className="heading-2 mt-4 text-[var(--color-fg-primary)]">
            Four steps to healthier screen habits
          </h2>
        </div>

        <div className="mt-10 grid gap-8 md:grid-cols-4">
          {steps.map((step, i) => (
            <div key={step.number} className="relative text-center">
              {/* Connector line */}
              {i < steps.length - 1 && (
                <div className="absolute left-[calc(50%+24px)] top-6 hidden h-px w-[calc(100%-48px)] bg-[var(--color-border-strong)] md:block" />
              )}

              <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full border border-[var(--color-border-strong)] bg-[var(--color-bg-surface)]">
                <span className="font-mono text-sm font-bold text-[var(--color-accent)]">
                  {step.number}
                </span>
              </div>
              <h3 className="heading-3 mt-4 text-[var(--color-fg-primary)]">
                {step.title}
              </h3>
              <p className="body-small mt-2 text-[var(--color-fg-secondary)]">
                {step.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
