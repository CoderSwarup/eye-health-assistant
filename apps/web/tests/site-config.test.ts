import { describe, it, expect } from 'vitest';
import { siteConfig } from '@/lib/site-config';

describe('siteConfig', () => {
  it('has required fields', () => {
    expect(siteConfig.name).toBe('Eye Health Assistant');
    expect(siteConfig.url).toBeDefined();
    expect(siteConfig.social.github).toBeDefined();
  });

  it('has download URLs configured', () => {
    expect(siteConfig.download.windows).toBeDefined();
    expect(siteConfig.download.macos).toBeDefined();
  });

  it('has no fabricated social handles', () => {
    expect(siteConfig.social.github).toContain('github.com');
  });
});
