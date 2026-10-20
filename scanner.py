import re
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", "venv", ".venv", "__pycache__",
             "dist", "build", ".tox", ".mypy_cache", ".pytest_cache"}

SOURCE_EXTS = {".py", ".js", ".ts", ".jsx", ".tsx", ".mjs", ".cjs",
               ".go", ".rb", ".sh", ".bash", ".zsh", ".php", ".java",
               ".kt", ".rs"}

PATTERNS = [
    re.compile(r'os\.environ(?:\.get)?\s*\[\s*["\']([A-Z_][A-Z0-9_]*)["\']\s*\]'),
    re.compile(r'os\.environ\.get\s*\(\s*["\']([A-Z_][A-Z0-9_]*)["\']'),
    re.compile(r'os\.getenv\s*\(\s*["\']([A-Z_][A-Z0-9_]*)["\']'),
    re.compile(r'environ\.get\s*\(\s*["\']([A-Z_][A-Z0-9_]*)["\']'),
    re.compile(r'process\.env\.([A-Z_][A-Z0-9_]*)'),
    re.compile(r'process\.env\[\s*["\']([A-Z_][A-Z0-9_]*)["\']\s*\]'),
    re.compile(r'os\.Getenv\s*\(\s*"([A-Z_][A-Z0-9_]*)"'),
    re.compile(r'ENV\[\s*["\']([A-Z_][A-Z0-9_]*)["\']\s*\]'),
    re.compile(r'ENV\.fetch\s*\(\s*["\']([A-Z_][A-Z0-9_]*)["\']'),
    re.compile(r'\$\{([A-Z_][A-Z0-9_]*)\}'),
    re.compile(r'\$([A-Z_][A-Z0-9_]*)\b'),
]

DECLARED_NAMES = [".env.example", ".env.sample", ".env.template",
                  ".env.sample.local"]


def extract_vars(text):
    found = set()
    for pat in PATTERNS:
        for m in pat.finditer(text):
            found.add(m.group(1))
    return found


def scan_repo(root):
    used = set()
    for path in Path(root).rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in SOURCE_EXTS:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        used |= extract_vars(text)
    return used


def parse_declared_text(text):
    declared = set()
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key = line.split("=", 1)[0].strip()
            if key.startswith("export "):
                key = key[len("export "):].strip()
            if key and re.match(r'^[A-Z_][A-Z0-9_]*$', key):
                declared.add(key)
    return declared


def read_declared(root, explicit=None):
    if explicit:
        p = Path(explicit)
        if not p.is_absolute():
            p = Path(root) / p
        return parse_declared_text(p.read_text(encoding="utf-8"))
    for name in DECLARED_NAMES:
        p = Path(root) / name
        if p.is_file():
            return parse_declared_text(p.read_text(encoding="utf-8"))
    p = Path(root) / ".env"
    if p.is_file():
        return parse_declared_text(p.read_text(encoding="utf-8"))
    return set()
