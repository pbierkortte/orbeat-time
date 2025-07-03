import pytest, zoneinfo
from datetime import datetime
from orbeat_time import to_ucy, to_orbeat8, to_eastern

EDGE_TEST_CASES = [
    ("2037-03-12T08:59:59+00:00", "4037_54_7.7777", "77777457"),
    ("2014-03-13T08:59:59+00:00", "4010_54_7.7777", "77777450"),
    ("2013-05-21T08:59:59+00:00", "4010_07_7.7777", "77777700"),
    ("2013-03-18T08:59:59+00:00", "4010_00_7.7777", "77777000"),
    ("1941-03-21T08:59:59+00:00", "3700_00_0.7777", "77770000"),
    ("1941-03-20T11:59:59+00:00", "3700_00_0.0777", "77700000"),
    ("1941-03-20T09:22:29+00:00", "3700_00_0.0077", "77000000"),
    ("1941-03-20T09:02:29+00:00", "3700_00_0.0007", "70000000"),
]


@pytest.mark.parametrize("dt_str,expected_ucy,expected_orbeat8", EDGE_TEST_CASES)
def test_orbeat_time_formats(dt_str, expected_ucy, expected_orbeat8):
    """Test that specific datetime strings produce expected orbeat and ucy outputs."""
    dt = datetime.fromisoformat(dt_str)
    unix_ms = int(dt.timestamp() * 1000)
    eastern = zoneinfo.ZoneInfo("America/New_York")
    dt_eastern = datetime.fromisoformat(dt_str).astimezone(eastern)
    expected_eastern = dt_eastern.strftime("%Y-%m-%d %I:%M %p %Z")
    assert to_ucy(unix_ms) == expected_ucy
    assert to_orbeat8(unix_ms) == expected_orbeat8
    assert to_eastern(unix_ms) == expected_eastern
