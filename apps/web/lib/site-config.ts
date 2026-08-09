export const siteConfig = {
  name: 'Eye Health Assistant',
  tagline: 'A calmer way to work at a screen.',
  description:
    'A privacy-first desktop application that helps you maintain healthier screen-use habits with intelligent reminders, optional eye tracking, guided exercises, and private local statistics.',
  url: process.env.NEXT_PUBLIC_SITE_URL || 'https://eyehealthassistant.com',
  social: {
    github: 'https://github.com/CoderSwarup/eye-health-assistant',
  },
  links: {
    docs: '/docs',
    releases: 'https://github.com/CoderSwarup/eye-health-assistant/releases',
    changelog: 'https://github.com/CoderSwarup/eye-health-assistant/blob/main/docs/CHANGELOG.md',
  },
  download: {
    windows: process.env.NEXT_PUBLIC_DOWNLOAD_WINDOWS_URL || 'https://github.com/CoderSwarup/eye-health-assistant/releases/download/v1.0.0/Eye-Health-Assistant-Windows-v1.0.0.zip',
    macos: process.env.NEXT_PUBLIC_DOWNLOAD_MACOS_URL || 'https://github.com/CoderSwarup/eye-health-assistant/releases/download/v1.0.0/Eye-Health-Assistant-macOS-v1.0.0.dmg',
  },
  platforms: {
    windows: 'Windows 10/11',
    macos: 'macOS 13+',
  },
  disclaimer:
    'Eye Health Assistant is a wellness and educational tool. It is not intended to diagnose, treat, cure, or prevent disease.',
} as const;
