from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath


REPO_ROOT = Path(__file__).resolve().parents[2]
MAX_BLOB_BYTES = 1_500_000

# High-confidence credential/token signatures. Findings report only pattern name,
# commit and path; potential secret values are never printed.
SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("pem_private_key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("github_token", re.compile(r"\bgh(?:p|o|u|s|r)_[A-Za-z0-9]{30,}\b")),
    ("github_fine_grained_pat", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{50,}\b")),
    ("google_api_key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("openai_style_key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("aws_access_key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("telegram_bot_token", re.compile(r"\b\d{7,12}:[A-Za-z0-9_-]{30,}\b")),
)

RISKY_BASENAMES = {
    ".env",
    ".env.local",
    ".env.production",
    "secrets.env",
    "id_rsa",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
    "credentials.json",
    "service-account.json",
}
RISKY_SUFFIXES = {".pem", ".p12", ".pfx"}

# Only uppercase environment-style names whose semantic suffix is itself an
# authorization credential are considered by the generic assignment detector.
# This intentionally excludes ordinary variables such as page_token and file
# path constants such as DEFAULT_SECRET_FILE; concrete credential formats are
# still caught independently by SECRET_PATTERNS above.
SENSITIVE_ASSIGNMENT = re.compile(
    r"(?m)^\s*(?:export\s+)?"
    r"(?P<name>[A-Z][A-Z0-9_]*(?:API_KEY|ACCESS_TOKEN|BOT_TOKEN|PASSWORD|PRIVATE_KEY|SSH_KEY|VPS_HOST))"
    r"\s*=\s*(?P<value>[^\r\n#]+?)\s*$"
)

PLACEHOLDER_MARKERS = (
    "${{",
    "${",
    "$",
    "%s",
    "<secret",
    "<token",
    "<key",
    "<host",
    "example",
    "changeme",
    "replace_me",
    "dummy",
    "redacted",
    "***",
)


def _git(*args: str, text: bool = True) -> str | bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
    )
    return result.stdout


def _is_placeholder(raw_value: str) -> bool:
    value = raw_value.strip().strip("\"'").strip()
    if not value:
        return True
    lower = value.lower()
    if lower in {"none", "null", "true", "false", "0"}:
        return True
    if any(marker in lower for marker in PLACEHOLDER_MARKERS):
        return True
    # Plain shell variable names / references are not literal credentials.
    if re.fullmatch(r"\$?[A-Z][A-Z0-9_]*", value):
        return True
    return False


def _risky_path(path: str) -> bool:
    pure = PurePosixPath(path)
    name = pure.name.lower()
    if name in RISKY_BASENAMES:
        return True
    if any(name.endswith(suffix) for suffix in RISKY_SUFFIXES):
        return True
    if name.startswith("id_rsa.") or name.startswith("id_ed25519."):
        return True
    return False


def _scan_text(text: str) -> set[str]:
    findings: set[str] = set()
    for label, pattern in SECRET_PATTERNS:
        if pattern.search(text):
            findings.add(label)
    for match in SENSITIVE_ASSIGNMENT.finditer(text):
        if not _is_placeholder(match.group("value")):
            findings.add(f"literal_sensitive_assignment:{match.group('name')}")
    return findings


def scan_full_history() -> list[tuple[str, str, str]]:
    commits = str(_git("rev-list", "--all")).splitlines()
    if not commits:
        raise RuntimeError("git history is unavailable; public-readiness audit requires fetch-depth: 0")

    findings: list[tuple[str, str, str]] = []
    scanned_blobs: dict[str, set[str]] = {}
    blob_paths_seen: set[tuple[str, str]] = set()

    for commit in commits:
        tree = _git("ls-tree", "-r", "-z", "--long", commit, text=False)
        assert isinstance(tree, bytes)
        for entry in tree.split(b"\0"):
            if not entry:
                continue
            try:
                meta, raw_path = entry.split(b"\t", 1)
                parts = meta.split()
                if len(parts) < 4 or parts[1] != b"blob":
                    continue
                blob_sha = parts[2].decode("ascii")
                size = int(parts[3]) if parts[3] != b"-" else 0
                path = raw_path.decode("utf-8", errors="replace")
            except (ValueError, UnicodeDecodeError):
                continue

            if _risky_path(path):
                key = (blob_sha, path)
                if key not in blob_paths_seen:
                    findings.append((commit, path, "risky_secret_filename"))
                    blob_paths_seen.add(key)

            if size <= 0 or size > MAX_BLOB_BYTES:
                continue
            if blob_sha not in scanned_blobs:
                blob = _git("cat-file", "blob", blob_sha, text=False)
                assert isinstance(blob, bytes)
                if b"\x00" in blob[:8192]:
                    scanned_blobs[blob_sha] = set()
                else:
                    text = blob.decode("utf-8", errors="ignore")
                    scanned_blobs[blob_sha] = _scan_text(text)
            for label in scanned_blobs[blob_sha]:
                findings.append((commit, path, label))

    # Deduplicate identical blob findings that appear in many commits. Keep the
    # first commit/path witness without exposing the matched value.
    unique: dict[tuple[str, str], tuple[str, str, str]] = {}
    for commit, path, label in findings:
        unique.setdefault((path, label), (commit, path, label))
    return sorted(unique.values(), key=lambda item: (item[1], item[2]))


def scan_workflow_policy() -> list[str]:
    findings: list[str] = []
    workflow_dir = REPO_ROOT / ".github" / "workflows"
    for path in sorted(workflow_dir.glob("*.y*ml")):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(REPO_ROOT).as_posix()
        if re.search(r"(?m)^\s*pull_request_target\s*:", text):
            findings.append(f"{rel}: pull_request_target is prohibited for this repository")
        if re.search(r"(?m)^\s*permissions\s*:\s*write-all\s*$", text):
            findings.append(f"{rel}: permissions: write-all is prohibited")

    # The reusable candidate-tree validator is the highest-risk PR path because
    # it stages repository content to the VPS. Require its explicit defense-in-
    # depth same-repository guard in addition to GitHub's default withholding of
    # repository secrets from fork-originated pull requests.
    reusable = workflow_dir / "reusable-production-copy-validation.yml"
    reusable_text = reusable.read_text(encoding="utf-8")
    guard = "github.event.pull_request.head.repo.full_name == github.repository"
    if guard not in reusable_text:
        findings.append(
            ".github/workflows/reusable-production-copy-validation.yml: missing same-repository fork guard"
        )
    return findings


def main() -> int:
    os.chdir(REPO_ROOT)
    history_findings = scan_full_history()
    workflow_findings = scan_workflow_policy()

    if history_findings:
        print("PUBLIC_READINESS_SECRET_AUDIT=FAIL")
        print(f"history_findings={len(history_findings)}")
        for commit, path, label in history_findings:
            print(f"- {label} at {path} (witness commit {commit[:12]})")
        print("Potential secret values are intentionally not printed. Rotate affected credentials before publication.")
    else:
        print("PUBLIC_READINESS_SECRET_AUDIT=PASS")
        print("full_history_high_confidence_secret_findings=0")

    if workflow_findings:
        print("PUBLIC_READINESS_WORKFLOW_POLICY=FAIL")
        for finding in workflow_findings:
            print(f"- {finding}")
    else:
        print("PUBLIC_READINESS_WORKFLOW_POLICY=PASS")

    return 1 if history_findings or workflow_findings else 0


if __name__ == "__main__":
    sys.exit(main())
