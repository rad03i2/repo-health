# Security Policy

## Scope
Repo Health is a local, read-only repository auditor. It does not upload repository contents, execute inspected files, modify the target repository, or contact external services.

## Sensitive data
The secret checks are deliberately heuristic. Findings identify the signal type and path but never print the matched secret. A match is not proof that a credential is valid. If a real credential was committed, revoke/rotate it and remove it from Git history using appropriate tooling.

## Reporting
Please report security concerns through GitHub's private vulnerability reporting feature when available. Do not include live credentials or private user data in a public issue.

## Supported version
Security fixes target the latest release on the default branch.
