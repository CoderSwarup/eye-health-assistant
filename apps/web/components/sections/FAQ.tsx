'use client';

import { useState } from 'react';
import { useScrollAnimate } from '@/lib/use-scroll-animate';

const faqs = [
  {
    question: 'What is Eye Health Assistant?',
    answer:
      'A privacy-first desktop application that helps you build healthier screen-use habits through intelligent reminders, optional eye tracking, guided exercises, and private local statistics.',
  },
  {
    question: 'Does it require a camera?',
    answer:
      'No. Camera is completely optional. Timer Mode works entirely without a camera, providing focus/break reminders based on configurable intervals.',
  },
  {
    question: 'Does the camera record me?',
    answer:
      'No. Camera processing happens entirely on your device using OpenCV and MediaPipe. No video is ever recorded, stored, or uploaded. Only derived metrics like estimated blink rate are calculated.',
  },
  {
    question: 'Is camera processing local?',
    answer:
      'Yes. All camera processing happens locally on your device. No frames are sent to any server or cloud service.',
  },
  {
    question: 'Does it work offline?',
    answer:
      'Yes. Core functionality — timer mode, exercises, statistics, and settings — works entirely offline. No internet connection is required.',
  },
  {
    question: 'Where is my data stored?',
    answer:
      'All data is stored in a local SQLite database on your device. No data is synced to the cloud.',
  },
  {
    question: 'Can I delete my data?',
    answer:
      'Yes. You can export your data as JSON or CSV, or delete everything from Settings at any time.',
  },
  {
    question: 'Is this medical software?',
    answer:
      'No. Eye Health Assistant is a wellness and educational tool. It is not intended to diagnose, treat, cure, or prevent disease. Consult a professional for persistent symptoms.',
  },
  {
    question: 'What operating systems are supported?',
    answer:
      'macOS 13+ and Windows 10/11. The application is built as a standalone installer — no Python, Node.js, or other tools required.',
  },
  {
    question: 'Is the project open source?',
    answer:
      'Yes. Eye Health Assistant is released under the MIT License. The source code is available on GitHub.',
  },
];

export function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);
  const sectionRef = useScrollAnimate();

  return (
    <section id="faq" className="relative py-[var(--spacing-section)]">
      <div className="mx-auto max-w-3xl px-6" ref={sectionRef} data-animate>
        <div className="text-center">
          <span className="label text-[var(--color-accent)]">FAQ</span>
          <h2 className="heading-2 mt-4 text-[var(--color-fg-primary)]">
            Frequently asked questions
          </h2>
        </div>

        <div className="mt-12 divide-y divide-[var(--color-border)]">
          {faqs.map((faq, i) => (
            <div key={i}>
              <button
                onClick={() => setOpenIndex(openIndex === i ? null : i)}
                className="flex w-full items-center justify-between py-5 text-left transition-colors hover:text-[var(--color-accent)]"
              >
                <span className="text-sm font-medium text-[var(--color-fg-primary)]">
                  {faq.question}
                </span>
                <svg
                  viewBox="0 0 16 16"
                  fill="currentColor"
                  className={`h-4 w-4 shrink-0 text-[var(--color-fg-muted)] transition-transform duration-200 ${
                    openIndex === i ? 'rotate-180' : ''
                  }`}
                >
                  <path d="M4.47 5.97a.75.75 0 011.06 0L8 8.44l2.47-2.47a.75.75 0 111.06 1.06l-3 3a.75.75 0 01-1.06 0l-3-3a.75.75 0 010-1.06z" />
                </svg>
              </button>
              <div
                className={`overflow-hidden transition-all duration-300 ${
                  openIndex === i ? 'max-h-40 pb-5' : 'max-h-0'
                }`}
              >
                <p className="body-small text-[var(--color-fg-secondary)]">
                  {faq.answer}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
