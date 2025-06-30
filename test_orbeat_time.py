import pytest
from datetime import datetime
from orbeat_time import to_orbeat8

EDGE_TEST_CASES = [
    ("2021-03-24T08:59:59+00:00", "77777557"),
    ("2020-05-24T08:59:59+00:00", "77777707"),
    ("2013-05-29T08:59:59+00:00", "77777700"),
    ("2013-04-04T08:59:59+00:00", "77770000"),
    ("2013-04-03T11:59:59+00:00", "77700000"),
    ("2013-04-03T09:22:29+00:00", "77000000"),
    ("2013-04-03T09:02:48+00:00", "70000000"),
    ("2013-04-03T09:00:00+00:00", "00000000"),
]


@pytest.mark.parametrize("dt_str,expected", EDGE_TEST_CASES)
def test_to_orbeat8_edge_cases(dt_str, expected):
    """Test that specific datetime strings produce expected orbeat outputs (input -> output validation)."""
    dt = datetime.fromisoformat(dt_str)
    unix_ms = int(dt.timestamp() * 1000)
    result = to_orbeat8(unix_ms)
    assert result == expected
