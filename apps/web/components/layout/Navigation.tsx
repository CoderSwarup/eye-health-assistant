'use client';

import { useState, useEffect } from 'react';
import { siteConfig } from '@/lib/site-config';

const navLinks = [
  { label: 'Features', href: '#features' },
  { label: 'How It Works', href: '#how-it-works' },
  { label: 'Privacy', href: '#privacy' },
  { label: 'Eye Care', href: '#eye-care' },
  { label: 'FAQ', href: '#faq' },
];

export function Navigation() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  useEffect(() => {
    if (mobileOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => { document.body.style.overflow = ''; };
  }, [mobileOpen]);

  return (
    <>
      <nav
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
          scrolled
            ? 'glass-strong py-3'
            : 'py-5 bg-transparent'
        }`}
      >
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6">
          {/* Logo */}
          <a href="#" className="flex items-center gap-2.5">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-[var(--color-accent)]/10">
              <svg
                viewBox="0 0 24 24"
                fill="none"
                className="h-4.5 w-4.5 text-[var(--color-accent)]"
                stroke="currentColor"
                strokeWidth="1.5"
              >
                <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7S2 12 2 12z" />
                <circle cx="12" cy="12" r="3" />
              </svg>
            </div>
            <span className="text-sm font-semibold tracking-tight text-[var(--color-fg-primary)]">
              {siteConfig.name}
            </span>
          </a>

          {/* Desktop links */}
          <div className="hidden items-center gap-8 md:flex">
            {navLinks.map((link) => (
              <a
                key={link.href}
                href={link.href}
                className="text-sm text-[var(--color-fg-secondary)] transition-colors hover:text-[var(--color-fg-primary)]"
              >
                {link.label}
              </a>
            ))}
          </div>

          {/* Desktop CTA */}
          <div className="hidden items-center gap-3 md:flex">
            <a
              href={siteConfig.social.github}
              target="_blank"
              rel="noopener noreferrer"
              className="rounded-[var(--radius-md)] px-4 py-2 text-sm text-[var(--color-fg-secondary)] transition-colors hover:text-[var(--color-fg-primary)]"
            >
              GitHub
            </a>
            <a
              href="#download"
              className="rounded-[var(--radius-md)] bg-[var(--color-accent)] px-4 py-2 text-sm font-medium text-[var(--color-fg-inverse)] transition-all hover:bg-[var(--color-accent-light)] hover:shadow-[0_0_20px_var(--color-accent-glow)]"
            >
              Download
            </a>
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="flex h-10 w-10 items-center justify-center rounded-[var(--radius-md)] text-[var(--color-fg-secondary)] transition-colors hover:text-[var(--color-fg-primary)] md:hidden"
            aria-label="Toggle menu"
          >
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.5"
              className="h-5 w-5"
            >
              {mobileOpen ? (
                <path d="M6 6l12 12M6 18L18 6" />
              ) : (
                <path d="M4 8h16M4 16h16" />
              )}
            </svg>
          </button>
        </div>
      </nav>

      {/* Mobile menu */}
      <div
        className={`fixed inset-0 z-40 bg-[var(--color-bg-primary)]/95 backdrop-blur-lg transition-all duration-300 md:hidden ${
          mobileOpen ? 'opacity-100' : 'pointer-events-none opacity-0'
        }`}
      >
        <div className="flex h-full flex-col items-center justify-center gap-8">
          {navLinks.map((link) => (
            <a
              key={link.href}
              href={link.href}
              onClick={() => setMobileOpen(false)}
              className="text-2xl font-medium text-[var(--color-fg-primary)] transition-colors hover:text-[var(--color-accent)]"
            >
              {link.label}
            </a>
          ))}
          <a
            href="#download"
            onClick={() => setMobileOpen(false)}
            className="mt-4 rounded-[var(--radius-lg)] bg-[var(--color-accent)] px-8 py-3 text-lg font-medium text-[var(--color-fg-inverse)]"
          >
            Download
          </a>
        </div>
      </div>
    </>
  );
}
