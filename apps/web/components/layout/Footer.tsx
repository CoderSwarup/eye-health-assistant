import { siteConfig } from '@/lib/site-config';

type FooterLink = {
  label: string;
  href: string;
  external?: boolean;
};

const footerSections: { title: string; links: FooterLink[] }[] = [
  {
    title: 'Product',
    links: [
      { label: 'Features', href: '#features' },
      { label: 'How It Works', href: '#how-it-works' },
      { label: 'Eye Care', href: '#eye-care' },
      { label: 'Privacy', href: '#privacy' },
      { label: 'FAQ', href: '#faq' },
    ],
  },
  {
    title: 'Resources',
    links: [
      { label: 'Documentation', href: siteConfig.links.docs },
      { label: 'GitHub', href: siteConfig.social.github, external: true },
      { label: 'Releases', href: siteConfig.links.releases, external: true },
      { label: 'Changelog', href: siteConfig.links.changelog, external: true },
    ],
  },
];

export function Footer() {
  return (
    <footer className="border-t border-[var(--color-border)] bg-[var(--color-bg-surface)]">
      <div className="mx-auto max-w-6xl px-6 py-16">
        <div className="grid gap-12 md:grid-cols-4">
          {/* Brand */}
          <div className="md:col-span-2">
            <div className="flex items-center gap-2.5">
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
            </div>
            <p className="mt-4 max-w-sm text-sm leading-relaxed text-[var(--color-fg-muted)]">
              A privacy-first desktop application that helps you maintain healthier
              screen-use habits. No cloud, no account, no compromise.
            </p>
            <p className="mt-4 text-xs text-[var(--color-fg-muted)]">
              {siteConfig.disclaimer}
            </p>
          </div>

          {/* Link sections */}
          {footerSections.map((section) => (
            <div key={section.title}>
              <h4 className="label text-[var(--color-fg-secondary)]">{section.title}</h4>
              <ul className="mt-4 space-y-3">
                {section.links.map((link) => (
                  <li key={link.label}>
                    <a
                      href={link.href}
                      {...(link.external
                        ? { target: '_blank', rel: 'noopener noreferrer' }
                        : {})}
                      className="text-sm text-[var(--color-fg-muted)] transition-colors hover:text-[var(--color-fg-primary)]"
                    >
                      {link.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Bottom bar */}
        <div className="mt-16 flex flex-col items-center justify-between gap-4 border-t border-[var(--color-border)] pt-8 md:flex-row">
          <p className="text-xs text-[var(--color-fg-muted)]">
            &copy; {new Date().getFullYear()} Eye Health Assistant Contributors. MIT License.
          </p>
          <div className="flex gap-6">
            <a
              href={siteConfig.social.github}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-[var(--color-fg-muted)] transition-colors hover:text-[var(--color-fg-secondary)]"
            >
              GitHub
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
