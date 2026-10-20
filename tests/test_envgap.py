import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scanner import extract_vars, parse_declared_text, scan_repo, read_declared


def test_extract_python():
    code = 'x = os.environ.get("FOO"); y = os.getenv("BAR")'
    assert extract_vars(code) == {"FOO", "BAR"}


def test_extract_js():
    code = 'const a = process.env.API_KEY; const b = process.env["SECRET"];'
    assert extract_vars(code) == {"API_KEY", "SECRET"}


def test_parse_declared():
    text = "FOO=1\n# comment\nBAR=\nexport BAZ=2\n"
    assert parse_declared_text(text) == {"FOO", "BAR", "BAZ"}


def test_scan_and_declared(tmp_path):
    (tmp_path / "app.py").write_text('import os\nx=os.getenv("USED")\n')
    (tmp_path / ".env.example").write_text("USED=1\nUNUSED=2\n")
    used = scan_repo(tmp_path)
    declared = read_declared(tmp_path)
    assert used == {"USED"}
    assert declared == {"USED", "UNUSED"}


def test_shell_vars():
    code = 'echo $HOME; echo ${PATH_VAR}'
    assert extract_vars(code) >= {"HOME", "PATH_VAR"}
