# Mobile Dependency Security Review

Status: OPEN - remediation not verified
Review date: 2026-10-26

Observed dependency versions:
- Expo: 58.0.19
- Expo CLI: 58.1.15
- node-forge: 1.4.0
- zod: 3.25.76

Findings:
- GHSA-86w9-cpqp-85rv: node-forge signature verification advisory.
- GHSA-mrhx-c7xc-m3w5: Zod constrained collection memory exhaustion advisory.
- npm audit reported five high-severity findings in the dependency tree.

Checks previously passed:
- Expo SDK compatibility check
- Expo Doctor (20/20)
- Mobile TypeScript check

Do not use npm audit fix --force without reviewing the resulting dependency
changes and compatibility. These findings remain unresolved until a supported
remediation is applied and verified. This note does not mitigate the findings.