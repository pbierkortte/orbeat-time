import time
import zoneinfo
from datetime import datetime

MS_PER_DAY = 86400000
DAYS_PER_YEAR = 365.2425
DAWN_MS = -9 * 60 * 60 * 1000
DATUM_JDN = 1705426
UNIX_JDN = 2440588
OFFSET_MS = (UNIX_JDN - DATUM_JDN) * MS_PER_DAY + DAWN_MS


def _parts_from_ms(unix_ms=None):
    """Helper to calculate Orbeat time components from a Unix timestamp."""
    if unix_ms is None:
        unix_ms = int(time.time() * 1000)

    ms_since = unix_ms + OFFSET_MS
    days_since = ms_since / MS_PER_DAY

    days = int(days_since)
    frac = days_since - days
    day_in_year = int(days % DAYS_PER_YEAR)

    year_int = int(days / DAYS_PER_YEAR)
    week_int = int(day_in_year / 8)
    day_int = int(days % 8)
    frac_int = int(frac * 8**4)

    return year_int, week_int, day_int, frac_int


def to_ucy(unix_ms=None):
    """
    Converts Unix millisecond timestamp to UCY format.

    Args:
        unix_ms: Unix timestamp in milliseconds. Defaults to current time.

    Returns:
        str: UCY format as "YYYY_WW_D.FFFF" where:
             - YYYY: Year number (in octal)
             - WW: Week number within the year (0-45 in octal)
             - D: Day within the 8-day week (0-7 in octal)
             - FFFF: Fractional part of day (0-7777 in octal)
    """
    years_int, weeks_int, days_int, frac_int = _parts_from_ms(unix_ms)

    year_oct = f"{years_int:04o}"
    week_oct = f"{weeks_int:02o}"
    day_oct = f"{days_int:o}"
    frac_oct = f"{frac_int:04o}"

    ucy = f"{year_oct}_{week_oct}_{day_oct}.{frac_oct}"
    return ucy.replace("-", "0")


def to_orbeat8(unix_ms=None):
    """
    Converts Unix millisecond timestamp to 8-character Orbeat format.

    Args:
        unix_ms: Unix timestamp in milliseconds. Defaults to current time.

    Returns:
        str: Orbeat8 format as 8-character string where:
             - Concatenates years (octal), weeks (2-digit octal), days (octal), fractions (4-digit octal)
             - Reverses the concatenated string and truncates to 8 characters
             - Uses same temporal calculations as UCY but in compressed cryptic format
    """
    years_int, weeks_int, days_int, frac_int = _parts_from_ms(unix_ms)

    year_oct = f"{years_int:o}"
    week_oct = f"{weeks_int:02o}"
    day_oct = f"{days_int:o}"
    frac_oct = f"{frac_int:04o}"

    orbeat = f"{year_oct}{week_oct}{day_oct}{frac_oct}"
    return orbeat[::-1][:8]


def to_eastern():
    """
    Converts current time to Eastern timezone format (EST/EDT with daylight saving).

    Returns:
        str: Eastern format as "YYYY-MM-DD HH:MM AM/PM EST/EDT"
    """
    eastern = zoneinfo.ZoneInfo("America/New_York")
    now_eastern = datetime.now(eastern)
    return now_eastern.strftime("%Y-%m-%d %I:%M %p %Z")


if __name__ == "__main__":
    print(f"{to_ucy()} UCY")
    print(f"{to_orbeat8()} ORB")
    print(to_eastern())
