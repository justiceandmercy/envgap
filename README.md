# envgap

Find gaps between environment variables referenced in your code and those declared in `.env.example`.

`envgap` scans a repository's source files for environment variable reads (`os.getenv`, `process.env.X`, `os.Getenv`, `ENV[...]`, `$VAR`, ...) and compares them against the variables declared in `.env.example` (or `.env.sample` / `.env.template`). It reports two kinds of gaps:

- **Missing declarations**: variables read in code but not declared in `.env.example`.
- **Unused declarations**: variables declared in `.env.example` but never read in code.

## Features

- Multi-language scanning: Python, JavaScript/TypeScript, Go, Ruby, Shell, PHP, Java/Kotlin, Rust.
- Auto-discovers `.env.example`, `.env.sample`, `.env.template` (falls back to `.env`).
- Plain text or JSON output.
- Optional non-zero exit code for CI gating.
- No external dependencies; pure standard library.

## Install

```sh
git clone https://github.com/yourname/envgap.git
cd envgap
chmod +x envgap.py
# optional: symlink onto PATH
ln -s "$(pwd)/envgap.py" /usr/local/bin/envgap
```

Requires Python 3.9+.

## Usage

```sh
# Scan current directory
python3 envgap.py

# Scan a specific repo
python3 envgap.py /path/to/repo

# JSON output for tooling
python3 envgap.py --json

# Gate CI on gaps
python3 envgap.py --exit-code
```

Example output:

```
Scanned /path/to/repo
Env vars used in code: 12
Env vars declared: 14

Used in code but NOT declared:
  - REDIS_URL

Declared but NOT used in code:
  - LEGACY_FLAG
```

## License

MIT
