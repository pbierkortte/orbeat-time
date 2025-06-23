import pytest
from datetime import datetime, timezone
from orbeat_time import to_orbeat8

EDGE_TEST_CASES = [
    ("2021-04-01T10:02:47.998770+00:00", "70000000"),
    ("2021-04-01T10:20:01.998770+00:00", "07000000"),
    ("2021-04-01T12:37:50.998770+00:00", "00700000"),
    ("2021-04-02T07:00:20.998770+00:00", "00070000"),
    ("2021-03-31T10:00:20.998770+00:00", "00007000"),
    ("2021-05-27T10:00:20.998770+00:00", "00000700"),
    ("2020-03-29T10:00:20.998770+00:00", "00000007"),
    ("2021-04-01T10:00:20.998770+00:00", "00000000"),
]


@pytest.mark.parametrize("dt_str,expected", EDGE_TEST_CASES)
def test_to_orbeat8_edge_cases(dt_str, expected):
    """Test that specific datetime strings produce expected orbeat outputs (input -> output validation)."""
    dt = datetime.fromisoformat(dt_str)
    unix_ms = int(dt.timestamp() * 1000)
    result = to_orbeat8(unix_ms)
    assert result == expected
