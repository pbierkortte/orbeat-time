import json
import pytest
import subprocess
from datetime import datetime


def run_cli(*args):
    result = subprocess.run(
        ["python", "-m", "orbeat_cli", *args],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip(), result.stderr.strip()


def test_cli_orbeat():
    out, _ = run_cli("--output", "orbeat")
    assert len(out) == 8


def test_cli_json():
    out, _ = run_cli("--output", "json")
    data = json.loads(out)
    assert "orbeat" in data
    assert len(data["orbeat"]) == 8
    assert "iso" in data
    assert datetime.fromisoformat(data["iso"])


def test_cli_help():
    out, _ = run_cli("-h")
    assert "usage: orbeat" in out
    assert "--output FORMAT" in out
    assert "default: orbeat" in out


def test_cli_errors():
    _, err = run_cli("--output", "invalid")
    assert "invalid choice" in err.lower()


def test_cli_no_args():
    out, _ = run_cli()
    assert len(out) == 8
