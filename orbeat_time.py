import time
import zoneinfo
from datetime import datetime

MS_PER_DAY = 86400000
DAYS_PER_YEAR = 365.25
PRIME_MERIDIAN_MS = -10 * 60 * 60 * 1000
CAESAR_JDN = 1705426
UNIX_JDN = 2440588
CAESAR_OFFSET_MS = (UNIX_JDN - CAESAR_JDN) * MS_PER_DAY


def to_ucy(unix_ms=None):
    """
    Converts Unix millisecond timestamp to UCY format.

    Args:
        unix_ms: Unix timestamp in milliseconds. Defaults to current time.

    Returns:
        str: UCY format as "YYYY_WW_D.FFFF" where:
             - YYYY: Years after Ceasar (Octal, 0-prefix for pre-epoch)
             - WW: Week number within the year (0-45 in octal)
             - D: Day within the 8-day week (0-7 in octal)
             - FFFF: Fractional part of day (0-7777 in octal)
    """
    now_ms = int(time.time() * 1000)
    ms_since_caesar = int(unix_ms or now_ms) + CAESAR_OFFSET_MS + PRIME_MERIDIAN_MS
    days_since_caesar = ms_since_caesar / MS_PER_DAY
    day_in_year = days_since_caesar % DAYS_PER_YEAR
    years = int(days_since_caesar / DAYS_PER_YEAR)
    weeks = int(day_in_year / 8)
    days = int(days_since_caesar % 8)
    fracs = int((days_since_caesar % 1) * 4096)
    ucy = f"{years:o}_{weeks:o}_{days:o}.{fracs:04o}".replace("-", "0")
    return ucy


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
    now_ms = int(time.time() * 1000)
    ms_since_caesar = int(unix_ms or now_ms) + CAESAR_OFFSET_MS + PRIME_MERIDIAN_MS
    days_since_caesar = ms_since_caesar / MS_PER_DAY
    day_in_year = days_since_caesar % DAYS_PER_YEAR
    years = int(days_since_caesar / DAYS_PER_YEAR)
    weeks = int(day_in_year / 8)
    days = int(days_since_caesar % 8)
    fracs = int((days_since_caesar % 1) * 4096)
    orbeat = f"{years:o}{weeks:02o}{days:o}{fracs:04o}"[::-1][:8]
    return orbeat


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
