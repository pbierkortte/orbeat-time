import pytest
from datetime import datetime
from orbeat_time import to_ucy, to_orbeat8

EDGE_TEST_CASES = [
    # Note: timestamps descend in value
    ("2021-03-24T08:59:59+00:00", "4017_55_7.7777", "77777557"),
    ("2014-03-29T08:59:59+00:00", "4010_55_7.7777", "77777550"),
    ("2013-05-29T08:59:59+00:00", "4010_07_7.7777", "77777700"),
    ("2013-04-03T08:59:59+00:00", "4010_00_7.7777", "77777000"),
    ("1941-03-29T08:59:59+00:00", "3700_00_0.7777", "77770000"),
    ("1941-03-28T11:59:59+00:00", "3700_00_0.0777", "77700000"),
    ("1941-03-28T09:22:29+00:00", "3700_00_0.0077", "77000000"),
    ("1941-03-28T09:02:29+00:00", "3700_00_0.0007", "70000000"),
]


@pytest.mark.parametrize("dt_str,expected_ucy,expected_orbeat8", EDGE_TEST_CASES)
def test_orbeat_time_formats(dt_str, expected_ucy, expected_orbeat8):
    """Test that specific datetime strings produce expected orbeat and ucy outputs."""
    dt = datetime.fromisoformat(dt_str)
    unix_ms = int(dt.timestamp() * 1000)
    assert to_ucy(unix_ms) == expected_ucy
    assert to_orbeat8(unix_ms) == expected_orbeat8
