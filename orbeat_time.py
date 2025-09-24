import math, time, zoneinfo
from datetime import datetime

UNIX_JDN = 2440588
DATUM_JDN = 1705433
MS_PER_DAY = 86400000
DAWN_MS = -9 * 60 * 60 * 1000
OFFSET_MS = (UNIX_JDN - DATUM_JDN) * MS_PER_DAY + DAWN_MS
DAYS_PER_YEAR = 365.2421875  # 365.24219 = 0o555.147 + 2.5e-6
STANDARD_YEAR = 368
SHORT_YEAR = 360


def to_parts_from_ms_ref(unix_ms=None):
    """
    Reference implementation using forward-only greedy algorithm.

    Args:
        unix_ms (int, optional): Unix timestamp in milliseconds. Defaults to current time.

    Returns:
        tuple: (year, week, day, fracs) - all as numeric values
    """
    unix_ms = unix_ms or time.time() * 1000
    ms_since = unix_ms + OFFSET_MS

    if ms_since < 0:
        raise NotImplementedError()

    remaining_ms = ms_since
    year_index = 0
    cumulative_days = 0

    while True:
        proj_drift = cumulative_days + STANDARD_YEAR
        proj_drift -= (year_index + 1) * DAYS_PER_YEAR

        if proj_drift < 4:
            days_this_year = STANDARD_YEAR
        else:
            days_this_year = SHORT_YEAR

        year_ms = days_this_year * MS_PER_DAY

        if remaining_ms < year_ms:
            day_of_year = remaining_ms // MS_PER_DAY
            ms_into_day = remaining_ms % MS_PER_DAY
            week_base = 0 if days_this_year == STANDARD_YEAR else 1
            week = week_base + (day_of_year // 8)
            day = day_of_year % 8
            fracs = ms_into_day / MS_PER_DAY

            return year_index, int(week), int(day), fracs

        remaining_ms -= year_ms
        cumulative_days += days_this_year
        year_index += 1


def to_parts_from_ms(unix_ms=None):
    """
    Convert Unix timestamp to time components.

    Args:
        unix_ms (int, optional): Unix timestamp in milliseconds. Defaults to current time.

    Returns:
        tuple: (year, week, day, fracs) - all as numeric values
    """
    unix_ms = unix_ms or time.time() * 1000
    ms_since = unix_ms + OFFSET_MS
    days = ms_since / MS_PER_DAY
    day_of_week = int(days % 8)
    fracs = (ms_since % MS_PER_DAY) / MS_PER_DAY

    # Linear estimate for year
    Y0 = 0.0027379093329411184
    Y1 = -4.211716108814683e-06
    years = int(Y0 * days + Y1 + 0.5)

    # Calculate year boundaries using the pattern
    rho = (DAYS_PER_YEAR - SHORT_YEAR) / 8.0
    longs_before = lambda y: int(rho * y + 0.5)
    is_long = lambda y: longs_before(y + 1) - longs_before(y) == 1
    year_length = lambda y: STANDARD_YEAR if is_long(y) else SHORT_YEAR
    start_of_year = lambda y: SHORT_YEAR * y + 8 * longs_before(y)

    # Find exact year and day within year
    c_y = start_of_year(years)
    y_len = year_length(years)
    d_in_y = days - c_y

    # Adjust year if needed
    if d_in_y < 0:
        years -= 1
        c_y = start_of_year(years)
        y_len = year_length(years)
        d_in_y = days - c_y
    elif d_in_y >= y_len:
        years += 1
        c_y = start_of_year(years)
        y_len = year_length(years)
        d_in_y = days - c_y

    # Calculate week (short years start at week 1)
    weeks = (0 if y_len == STANDARD_YEAR else 1) + int(d_in_y / 8)

    return years, weeks, day_of_week, fracs


def to_eastern(unix_ms=None):
    """
    Get time in Eastern timezone.

    Args:
        unix_ms (int, optional): Unix timestamp in milliseconds. Defaults to current time.

    Returns:
        str: Eastern time in format "YYYY-MM-DD HH:MM AM/PM EST/EDT/LMT"
    """
    unix_ms = unix_ms or time.time() * 1000
    eastern = zoneinfo.ZoneInfo("America/New_York")
    dt = datetime.fromtimestamp(unix_ms / 1000, tz=eastern)
    return dt.strftime("%Y-%m-%d %I:%M %p %Z")


def to_orbeat8(unix_ms=None):
    """
    Convert Unix timestamp to compact 8-character Orbeat format.

    Args:
        unix_ms (int, optional): Unix timestamp in milliseconds. Defaults to current time.

    Returns:
        str: 8-character compact timestamp
    """
    year, week, day, frac = to_parts_from_ms(unix_ms)
    frac_int = int(frac * 8**4)
    year_oct = f"{year:o}".replace("-", "0")
    week_oct = f"{week:02o}"
    day_oct = f"{day:01o}"
    frac_oct = f"{frac_int:04o}"
    full_string = f"{year_oct}{week_oct}{day_oct}{frac_oct}"[::-1][:8]
    return full_string


def to_ucy(unix_ms=None):
    """
    Converts Unix timestamp to UCY format: YYYY_WW_D.FFFF

    UCY:
        How those without shadows play hide and seek with the sun.

    Args:
        unix_ms (int, optional): Unix timestamp in milliseconds. Defaults to current time.

    Returns:
        str: Human-readable timestamp
    """
    year, week, day, frac = to_parts_from_ms(unix_ms)
    frac_int = int(frac * 8**4)
    year_oct = f"{year:o}".replace("-", "0")
    week_oct = f"{week:02o}"
    day_oct = f"{day:01o}"
    frac_oct = f"{frac_int:04o}"
    full_string = f"{year_oct}_{week_oct}_{day_oct}.{frac_oct}"
    return full_string


if __name__ == "__main__":  # pragma: no cover
    print(f"Eastern Time: {to_eastern()}")
    print(f"Orbeat Time: {to_orbeat8()}")
    print(f"UCY Time: {to_ucy()}")
