from datetime import datetime, timedelta, timezone

DAYS_PER_YEAR = 365.25
MILLISECONDS_PER_DAY = 24 * 60 * 60 * 1000
NUNDINAL_OFFSET = 3
YEARS_WHOLE = 1
YEARS_FRAC = 2
DAYS_WHOLE = 1
DAYS_FRAC = 4


def encode_orbeat_time(unix_ms: float) -> str:
    """
    Encode Unix milliseconds timestamp into Orbeat time format.

    Args:
        unix_milliseconds: Unix timestamp in milliseconds

    Returns:
        Encoded Orbeat time string
    """

    days, day_frac = divmod(unix_ms / MILLISECONDS_PER_DAY, 1)

    years, year_frac = divmod(int(days) / DAYS_PER_YEAR, 1)

    days_with_offset = days + NUNDINAL_OFFSET

    years_whole = f"{int(years) % 8:0{YEARS_WHOLE}o}"
    years_frac = f"{int(year_frac * (8 ** YEARS_FRAC)):0{YEARS_FRAC}o}"
    days_whole = f"{int(days_with_offset) % 8:0{DAYS_WHOLE}o}"
    days_frac = f"{int(day_frac * (8 ** DAYS_FRAC)):0{DAYS_FRAC}o}"

    return (years_whole + years_frac + days_whole + days_frac)[::-1]


if __name__ == "__main__":  # pragma: no cover
    print("Demo Output:")
    current_date = datetime.now(timezone.utc).replace(microsecond=0)
    for i in range(8):
        future_date = current_date + timedelta(days=i)
        unix_ms = int(future_date.timestamp() * 1000)
        print(future_date.isoformat(), encode_orbeat_time(unix_ms), sep=" | ")
