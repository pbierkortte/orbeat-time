import math, time, zoneinfo
from datetime import datetime

UNIX_JDN = 2440588
DATUM_JDN = 1705426
MS_PER_DAY = 86400000
DAWN_MS = -9 * 60 * 60 * 1000
OFFSET_MS = (UNIX_JDN - DATUM_JDN) * MS_PER_DAY + DAWN_MS
DAYS_PER_YEAR = 365.2425


def to_parts_from_ms(unix_ms=None):
    """
    Convert Unix timestamp to time components in octal format.

    Args:
        unix_ms (int, optional): Unix timestamp in milliseconds. Defaults to current time.

    Returns:
        tuple: (year_oct, week_oct, day_oct, frac_oct) - all as octal strings
    """
    unix_ms = unix_ms or time.time() * 1000
    ms_since = unix_ms + OFFSET_MS
    days_since = ms_since / MS_PER_DAY

    days = math.floor(days_since)
    frac = days_since - days
    day_in_year = int(days % DAYS_PER_YEAR)

    year_int = int(days / DAYS_PER_YEAR)
    day_int = int(days % 8)
    frac_int = int(frac * 8**4)

    week_int = max(0, (day_in_year - day_int) // 8)

    year_oct = f"{year_int:o}".replace("-", "0")
    week_oct = f"{week_int:02o}"
    day_oct = f"{day_int:01o}"
    frac_oct = f"{frac_int:04o}"
    return year_oct, week_oct, day_oct, frac_oct


def to_ucy(unix_ms=None):
    """
    Convert Unix timestamp to UCY format: YYYY_WW_D.FFFF

    Args:
        unix_ms (int, optional): Unix timestamp in milliseconds. Defaults to current time.

    Returns:
        str: Human-readable timestamp
    """
    return "%s_%s_%s.%s" % to_parts_from_ms(unix_ms)


def to_orbeat8(unix_ms=None):
    """
    Convert Unix timestamp to compact 8-character Orbeat format.

    Args:
        unix_ms (int, optional): Unix timestamp in milliseconds. Defaults to current time.

    Returns:
        str: 8-character compact timestamp
    """
    return ("%s%s%s%s" % to_parts_from_ms(unix_ms))[::-1][:8]


if __name__ == "__main__":
    print(f"{to_ucy()} UCY")
    print(f"{to_orbeat8()} ORB")
