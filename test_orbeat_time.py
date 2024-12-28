import pytest
from datetime import datetime
from orbeat_time import encode_orbeat_time

TEST_CASES = [
    ("1970-01-01T00:00:00+00:00", "00000000"),  # Tests Unix epoch, year whole = 0, and day whole = 0 (base case)
    ("2023-11-14T22:13:20+00:00", "02373765"),  # Tests documented example case with Unix timestamp 1700000000000
    ("2100-01-01T10:39:16+00:00", "23432771"),  # Tests far future date (century boundary)
    ("2024-01-01T15:30:45+00:00", "72153775"),  # Tests first day of leap year (year transition + leap year start)
    ("2024-02-29T08:45:30+00:00", "62726216"),  # Tests leap day (special calendar case)
    ("1970-12-27T00:00:00+00:00", "00000770"),  # Tests year part = 00 (clean year division)
    ("1972-12-31T23:59:59+00:00", "77777772"),  # Tests year part = 77 (maximum year fraction)
    ("1972-12-31T23:45:45+00:00", "72777772"),  # Tests day part = 7777 (maximum day fraction pattern)
]

@pytest.mark.parametrize("dt_str,expected", TEST_CASES)
def test_encode_orbeat_time_valid_dates(dt_str, expected):
    dt = datetime.fromisoformat(dt_str)
    unix_ms = dt.timestamp() * 1000
    result = encode_orbeat_time(unix_ms)
    assert result == expected
    assert isinstance(result, str)
    assert all(c in '01234567' for c in result)
