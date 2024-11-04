import pytest
from datetime import datetime
from orbeat_time import encode_orbeat_time

TEST_CASES = [
    ("2024-11-13T12:21:48+00:00", "67040166"),
    ("2024-11-14T02:36:02+00:00", "37601166"),
    ("2024-11-14T16:50:16+00:00", "17451166"),
    ("2024-11-15T07:04:30+00:00", "76222166"),
    ("2024-11-15T21:18:44+00:00", "56072166"),
    ("2024-11-16T11:32:58+00:00", "36633176"),
    ("2024-11-17T01:47:12+00:00", "06404176"),
    ("2024-11-17T16:01:26+00:00", "65254176"),
]

@pytest.mark.parametrize("dt_str,expected", TEST_CASES)
def test_encode_orbeat_time_valid_dates(dt_str, expected):
    dt = datetime.fromisoformat(dt_str)
    unix_ms = dt.timestamp() * 1000
    result = encode_orbeat_time(unix_ms)
    assert result == expected

def test_negative_timestamp():
    with pytest.raises(ValueError):
        encode_orbeat_time(-1000)

def test_zero_timestamp():
    result = encode_orbeat_time(0)
    assert isinstance(result, str)
    assert all(c in '01234567' for c in result)

def test_large_timestamp():
    future_date = datetime.fromisoformat("2100-01-01T00:00:00+00:00")
    unix_ms = future_date.timestamp() * 1000
    result = encode_orbeat_time(unix_ms)
    assert isinstance(result, str)
    assert all(c in '01234567' for c in result)
