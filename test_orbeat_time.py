import pytest
from datetime import datetime, timezone
from orbeat_time import to_orbeat8

EDGE_TEST_CASES = [
    ("2021-04-01T09:02:48+00:00", "70000000"),
    ("2021-04-01T09:20:00+00:00", "07000000"),
    ("2021-04-01T11:37:51+00:00", "00700000"),
    ("2021-04-02T06:00:00+00:00", "00070000"),
    ("2021-03-31T09:00:00+00:00", "00007000"),
    ("2021-05-27T09:00:00+00:00", "00000700"),
    ("2020-03-29T09:00:00+00:00", "00000007"),
    ("2021-04-01T09:00:00+00:00", "00000000"),
]


@pytest.mark.parametrize("dt_str,expected", EDGE_TEST_CASES)
def test_to_orbeat8_edge_cases(dt_str, expected):
    """Test that specific datetime strings produce expected orbeat outputs (input -> output validation)."""
    dt = datetime.fromisoformat(dt_str)
    unix_ms = int(dt.timestamp() * 1000)
    result = to_orbeat8(unix_ms)
    assert result == expected
