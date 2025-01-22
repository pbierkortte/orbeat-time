from datetime import datetime, timezone, timedelta

DAYS_PER_YEAR = 365.25
MS_PER_DAY = 86_400_000


def encode_orbeat_time(unix_ms: float) -> str:
    """Convert Unix timestamp milliseconds to orbeat time format.

    Args:
        unix_ms (float): Unix timestamp in milliseconds

    Returns:
        str: Orbeat time
    """

    days, day_frac = divmod(unix_ms / MS_PER_DAY, 1)
    years, year_frac = divmod(int(days) / DAYS_PER_YEAR, 1)

    y1, y2 = f"{int(years) % 8:o}", f"{int(year_frac * 64):02o}"
    d1, d2 = f"{int(days) % 8:o}", f"{int(day_frac * 4096):04o}"
    return (y1 + y2 + d1 + d2)[::-1]

if __name__ == "__main__":  # pragma: no cover
    print("Demo Output:")
    current_date = datetime.now(timezone.utc).replace(microsecond=0)
    for i in range(8):
        future_date = current_date + timedelta(days=i)
        unix_ms = int(future_date.timestamp() * 1000)
        print(future_date.isoformat(), encode_orbeat_time(unix_ms), sep=" | ")
