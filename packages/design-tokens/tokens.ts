/**
 * Design tokens for Eye Health Assistant.
 *
 * These tokens define the visual language of the application.
 * Both the desktop (PySide6) and web (Next.js) applications
 * derive their visual styles from these values.
 */

export const colors = {
  // Neutral foundation
  neutral: {
    50: '#F8F9FA',
    100: '#F1F3F5',
    200: '#E9ECEF',
    300: '#DEE2E6',
    400: '#ADB5BD',
    500: '#6C757D',
    600: '#495057',
    700: '#343A40',
    800: '#222222',
    900: '#1A1A1A',
    950: '#111111',
  },
  // Accent colors (used sparingly)
  blue: {
    500: '#2563EB',
    600: '#2563EB',
    700: '#1D4ED8',
  },
  purple: {
    500: '#7C3AED',
    600: '#7C3AED',
  },
  // Status colors
  success: '#16A34A',
  warning: '#D97706',
  error: '#DC2626',
  info: '#2563EB',
} as const;

export const spacing = {
  0: '0px',
  1: '4px',
  2: '8px',
  3: '12px',
  4: '16px',
  5: '20px',
  6: '24px',
  8: '32px',
  10: '40px',
  12: '48px',
  16: '64px',
} as const;

export const typography = {
  fontFamily: {
    sans: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
  },
  fontSize: {
    caption: '11px',
    label: '12px',
    body: '13px',
    subtitle: '14px',
    heading: '16px',
    title: '22px',
    display: '28px',
  },
  fontWeight: {
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },
} as const;

export const borderRadius = {
  sm: '4px',
  md: '8px',
  lg: '12px',
  xl: '16px',
  full: '9999px',
} as const;

export const shadows = {
  sm: '0 1px 2px rgba(0, 0, 0, 0.04)',
  md: '0 2px 4px rgba(0, 0, 0, 0.06)',
  lg: '0 4px 8px rgba(0, 0, 0, 0.08)',
  xl: '0 8px 16px rgba(0, 0, 0, 0.12)',
} as const;
