import pytest
from datetime import datetime, timezone
from orbeat_time import to_orbeat8

# Edge test cases with 0s and 7s patterns - back-calculated timestamps
EDGE_TEST_CASES = [
    ("2021-04-01T05:02:39.961000+00:00", "70000000"),
    ("2021-04-01T05:20:00.521000+00:00", "07000000"),
    ("2021-04-01T07:37:39.966000+00:00", "00700000"),
    ("2021-04-02T02:00:13.568000+00:00", "00070000"),
    ("2021-03-31T05:00:11.383000+00:00", "00007000"),
    ("2021-05-27T05:00:12.772000+00:00", "00000700"),
    ("2020-03-29T05:00:08.601000+00:00", "00000007"),
    ("2021-04-01T05:00:16.884000+00:00", "00000000"),
]


@pytest.mark.parametrize("dt_str,expected", EDGE_TEST_CASES)
def test_to_orbeat8_edge_cases(dt_str, expected):
    """Test that specific datetime strings produce expected orbeat outputs (input -> output validation)."""
    dt = datetime.fromisoformat(dt_str)
    unix_ms = int(dt.timestamp() * 1000)
    result = to_orbeat8(unix_ms)
    assert result == expected
