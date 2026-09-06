# Findings

## What Each Tool Caught (and How I Fixed It)

**Gitleaks — Secret Detection**

Gitleaks flagged a hardcoded AWS secret key in `src/security_ci_pipeline/main.py` that matched its `generic-api-key` rule. The credentials were sitting directly in source code, which is exactly the kind of thing this pipeline is meant to catch.

To fix it, I removed the raw credentials from the codebase and refactored the app to read them from environment variables via `os.environ` instead. In CI, those values are injected securely through GitHub Secrets so they never touch the repo.

---

**uv audit — Dependency Vulnerability Scanning**

`uv audit` picked up a known CVE (CVE-2024-35195) in `requests==2.31.0`, which was pinned as a direct dependency. The advisory had a fix available in a newer release.

The fix was straightforward: bumped the version spec to `requests>=2.32.2` in `pyproject.toml` and re-ran `uv lock` to regenerate `uv.lock` with the patched release.

---

## GitHub Secrets — What They Actually Protect (and What They Don't)

GitHub Secrets are a solid first step for keeping credentials out of your codebase, but they're not a complete security boundary. Here's how I think about the tradeoffs:

**What storing credentials in Secrets actually helps with:**
- Keeping API keys out of version control history, forks, and public repos.
- Preventing casual credential exposure — GitHub automatically redacts secret values from workflow logs.

**What it doesn't protect against:**
- A malicious or compromised workflow that exfiltrates secrets by encoding them (e.g., base64) and forwarding them to an external endpoint. This is a real risk with `pull_request_target` triggers.
- Long-lived IAM key exposure. Static secrets stored in GitHub don't rotate automatically and don't enforce least-privilege scoping. The better alternative here is OIDC with short-lived IAM roles — no long-lived keys to leak in the first place.

---

## Challenges I Ran Into

**Getting Gitleaks to actually trigger:**
Out of the box, Gitleaks skipped the dummy `EXAMPLE` keys I initially used because they hit default allowlists. I had to switch to realistic high-entropy tokens for the rule to fire reliably. Also, the action needs `fetch-depth: 0` in the checkout step — without full git history, it misses commits and doesn't scan uncommitted working tree changes properly.

**Action versioning:**
Figuring out the right tag for `astral-sh/setup-uv` took some digging since the documentation comments didn't always match available release tags. Landed on `astral-sh/setup-uv@v4` as the stable tag that actually resolved without errors.

---

## AI Collaboration Disclosure

I used Gemini to help with parts of this project — specifically for brainstorming realistic CVE candidates compatible with Python 3.14, generating high-entropy mock AWS credentials that would reliably trigger Gitleaks, and working through the CI workflow YAML structure.
