import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { siteConfig } from '@/lib/site-config';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

export const metadata: Metadata = {
  title: `${siteConfig.name} - Privacy-First Screen Wellness`,
  description: siteConfig.description,
  keywords: [
    'eye health',
    'screen wellness',
    'blink detection',
    '20-20-20 rule',
    'eye strain',
    'privacy first',
    'desktop app',
    'focus timer',
    'break reminder',
  ],
  authors: [{ name: 'Eye Health Assistant Contributors' }],
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: siteConfig.url,
    siteName: siteConfig.name,
    title: `${siteConfig.name} - Privacy-First Screen Wellness`,
    description:
      'Build healthier screen habits with local-first, privacy-respecting monitoring and reminders.',
  },
  twitter: {
    card: 'summary_large_image',
    title: siteConfig.name,
    description: 'Privacy-first desktop app for healthier screen-use habits.',
  },
  robots: {
    index: true,
    follow: true,
  },
  alternates: {
    canonical: siteConfig.url,
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="bg-[var(--color-bg-primary)] text-[var(--color-fg-primary)] antialiased">
        {children}
      </body>
    </html>
  );
}
