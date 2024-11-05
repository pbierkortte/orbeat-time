import pytest
from datetime import datetime
from orbeat_time import encode_orbeat_time

TEST_CASES = [
    ("1970-01-01T00:00:00+00:00", "00000000"),
    ("2024-11-14T16:50:16+00:00", "17451166"),
    ("2024-11-15T07:04:30+00:00", "76222166"),
    ("2024-11-15T21:18:44+00:00", "56072166"),
    ("2024-11-16T11:32:58+00:00", "36633176"),
    ("2025-12-31T10:33:51+00:00", "21435477"),
    ("2026-01-01T10:33:51+00:00", "21436400"),
    ("2100-01-01T10:39:16+00:00", "23432702"),
    
]

@pytest.mark.parametrize("dt_str,expected", TEST_CASES)
def test_encode_orbeat_time_valid_dates(dt_str, expected):
    dt = datetime.fromisoformat(dt_str)
    unix_ms = dt.timestamp() * 1000
    result = encode_orbeat_time(unix_ms)
    assert result == expected
    assert isinstance(result, str)
    assert all(c in '01234567' for c in result)
