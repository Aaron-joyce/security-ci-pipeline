# Security CI Pipeline

A small Python app I built to explore DevSecOps in practice — specifically, how to wire up automated security scanning directly into a GitHub Actions pipeline (shift-left security).

The idea is simple: every time a commit is pushed, the pipeline checks for hardcoded secrets and vulnerable dependencies before anything gets close to production.

---

## Tools I Used

- **Python 3.14** managed with [`uv`](https://github.com/astral-sh/uv) for packaging and running the project.
- **[Gitleaks](https://github.com/gitleaks/gitleaks)** for secret detection — it scans the git history and working tree to catch any credentials that shouldn't be there.
- **`uv audit`** for dependency vulnerability scanning — it checks all direct and transitive dependencies against known CVE advisories.
- **`boto3`** to simulate a real AWS DynamoDB integration, giving the pipeline something meaningful to secure.

---

## Project Layout

```text
├── .github/
│   └── workflows/
│        └── security_ci.yaml    # CI workflow (Gitleaks + uv audit)
├── src/
│   └── security_ci_pipeline/
│       └── main.py         # DynamoDB client handler
├── pyproject.toml          # Project configuration and dependencies
├── uv.lock                 # Deterministic dependency lockfile
└── README.md
```
