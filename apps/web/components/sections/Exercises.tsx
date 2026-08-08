'use client';

import { useScrollAnimate } from '@/lib/use-scroll-animate';

const exercises = [
  {
    title: 'Gentle Blinking',
    duration: '2 min',
    description: 'Slow, deliberate blinks to refresh your tear film.',
    color: 'var(--color-accent)',
  },
  {
    title: 'Visual Rest',
    duration: '3 min',
    description: 'Close your eyes and relax your focusing muscles.',
    color: '#8b5cf6',
  },
  {
    title: 'Distance Viewing',
    duration: '2 min',
    description: 'Look at a distant object to relieve eye strain.',
    color: '#22c55e',
  },
  {
    title: 'Guided Break',
    duration: '5 min',
    description: 'A complete eye-care routine with step-by-step guidance.',
    color: '#f59e0b',
  },
];

export function Exercises() {
  const sectionRef = useScrollAnimate();

  return (
    <section className="relative py-[var(--spacing-section)]">
      <div className="mx-auto max-w-6xl px-6" ref={sectionRef} data-animate>
        <div className="mx-auto max-w-2xl text-center">
          <span className="label text-[var(--color-accent)]">Exercises</span>
          <h2 className="heading-2 mt-4 text-[var(--color-fg-primary)]">
            Short guided routines for your eyes
          </h2>
          <p className="body-large mt-4 text-[var(--color-fg-secondary)]">
            Quick, evidence-informed activities you can do at your desk in under
            five minutes.
          </p>
        </div>

        <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {exercises.map((exercise) => (
            <div
              key={exercise.title}
              className="group rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-bg-surface)] p-6 transition-all duration-300 hover:border-[var(--color-accent)]/20 hover:bg-[var(--color-bg-elevated)]"
            >
              <div
                className="flex h-10 w-10 items-center justify-center rounded-[var(--radius-md)]"
                style={{ backgroundColor: `color-mix(in srgb, ${exercise.color} 10%, transparent)` }}
              >
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  className="h-5 w-5"
                  style={{ color: exercise.color }}
                >
                  <circle cx="12" cy="12" r="10" />
                  <path d="M12 6v6l4 2" />
                </svg>
              </div>
              <h3 className="mt-4 text-sm font-semibold text-[var(--color-fg-primary)]">
                {exercise.title}
              </h3>
              <span className="caption mt-1 inline-block" style={{ color: exercise.color }}>
                {exercise.duration}
              </span>
              <p className="body-small mt-2 text-[var(--color-fg-secondary)]">
                {exercise.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
