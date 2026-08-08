'use client';

import { useScrollAnimate } from '@/lib/use-scroll-animate';

const topics = [
  {
    title: 'Screen Habits',
    description: 'Build awareness of how you use your screen throughout the day.',
  },
  {
    title: 'Breaks',
    description: 'Why regular breaks matter and how to make them automatic.',
  },
  {
    title: 'Blinking',
    description: 'The science of blinking during screen use and why it matters.',
  },
  {
    title: 'Workspace Setup',
    description: 'Optimize your desk, monitor, and lighting for eye comfort.',
  },
  {
    title: 'Lighting',
    description: 'How ambient light affects your eyes during screen use.',
  },
  {
    title: 'When to Seek Advice',
    description: 'Recognizing when to consult an eye-care professional.',
  },
];

export function EyeCare() {
  const sectionRef = useScrollAnimate();

  return (
    <section id="eye-care" className="relative py-[var(--spacing-section)]">
      <div className="mx-auto max-w-6xl px-6" ref={sectionRef} data-animate>
        <div className="mx-auto max-w-2xl text-center">
          <span className="label text-[var(--color-accent)]">Eye Care Center</span>
          <h2 className="heading-2 mt-4 text-[var(--color-fg-primary)]">
            Learn to take better care of your eyes
          </h2>
          <p className="body-large mt-4 text-[var(--color-fg-secondary)]">
            Educational content about healthy screen habits, workspace setup, and
            when to seek professional advice.
          </p>
        </div>

        <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {topics.map((topic) => (
            <div
              key={topic.title}
              className="group rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-bg-surface)] p-6 transition-all duration-300 hover:border-[var(--color-accent)]/20 hover:bg-[var(--color-bg-elevated)]"
            >
              <h3 className="text-sm font-semibold text-[var(--color-fg-primary)]">
                {topic.title}
              </h3>
              <p className="body-small mt-2 text-[var(--color-fg-secondary)]">
                {topic.description}
              </p>
            </div>
          ))}
        </div>

        <p className="mt-8 text-center text-xs text-[var(--color-fg-muted)]">
          Educational content only. Not medical advice. Consult a professional for persistent symptoms.
        </p>
      </div>
    </section>
  );
}
