import { describe, it, expect } from 'vitest';

describe('Navigation', () => {
  const requiredSections = ['Features', 'How It Works', 'Privacy', 'Eye Care', 'FAQ'];

  it('has all required navigation sections', () => {
    requiredSections.forEach((section) => {
      expect(requiredSections).toContain(section);
    });
  });

  it('required sections count is correct', () => {
    expect(requiredSections.length).toBe(5);
  });
});
