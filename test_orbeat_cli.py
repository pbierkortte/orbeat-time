import json
import pytest
from datetime import datetime
from orbeat_cli import run_cli


def test_cli_orbeat():
    out, _ = run_cli('--output', 'orbeat', is_test=True)
    assert len(out) == 8

def test_cli_json():
    out, _ = run_cli('--output', 'json', is_test=True)
    data = json.loads(out)
    assert 'orbeat' in data
    assert len(data['orbeat']) == 8
    assert 'iso' in data
    assert datetime.fromisoformat(data['iso'])

def test_cli_help():
    out, _ = run_cli('-h', is_test=True)
    assert 'usage: orbeat' in out
    assert '--output FORMAT' in out
    assert 'default: orbeat' in out

def test_cli_errors():
    _, err = run_cli('--output', 'invalid', is_test=True)
    assert 'invalid choice' in err.lower()

def test_cli_no_args():
    out, _ = run_cli(is_test=True)
    assert len(out) == 8
