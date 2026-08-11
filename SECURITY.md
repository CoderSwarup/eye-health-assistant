# Security Policy

## Reporting Vulnerabilities

If you discover a security vulnerability, please report it responsibly:

1. **Do not** open a public GitHub issue
2. Email security@[your-domain].com (if available)
3. Or create a private security advisory on GitHub

## Security Measures

### Data Privacy

- **Local-only storage**: All data stays on your device
- **No cloud sync**: No accounts, no remote servers
- **No telemetry**: No usage data is collected
- **No tracking**: No analytics or tracking scripts

### Camera Security

- **In-memory processing only**: Webcam frames are never written to disk
- **Explicit permission**: Camera access requires user consent
- **Visual indicator**: Camera status always visible in UI
- **No upload**: Camera data never leaves your device

### Database Security

- **SQLite**: Local database file only
- **No remote access**: Database is not exposed over network
- **Encryption**: Consider enabling SQLCipher for sensitive data (future)

### Application Security

- **Input validation**: All user inputs are validated
- **Type safety**: TypeScript strict mode + Python type hints
- **Dependency scanning**: Automated dependency updates via Dependabot
- **Code signing**: Desktop app can be code-signed for distribution

## Best Practices

### For Users

1. Keep the application updated
2. Review camera permissions in your OS settings
3. Regularly export and backup your data
4. Report any suspicious behavior immediately

### For Developers

1. Never commit secrets or API keys
2. Use environment variables for configuration
3. Run security linters before committing
4. Review dependencies for vulnerabilities

## Data Retention

- **Sessions**: Stored locally in SQLite database
- **Settings**: Stored in local config file
- **Logs**: Rotated and stored locally (5MB max, 3 backups)
- **No cloud backups**: User must manually backup if desired

## Compliance

- **GDPR**: Local-only storage simplifies compliance
- **CCPA**: No personal data collection
- **HIPAA**: Not a medical device — no HIPAA requirements

## Updates

Security patches will be released as:
- **Critical**: Immediate patch release
- **High**: Next minor version
- **Medium/Low**: Next major version

## Contact

For security inquiries:
- GitHub Security Advisories
- Email: [your-security-email]
