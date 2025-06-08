from datetime import datetime, timedelta, timezone

DAYS_PER_YEAR = 365.25
MILLISECONDS_PER_DAY = 24 * 60 * 60 * 1000
DAWN_OFFSET_MS = 10 * 60 * 60 * 1000  # 5 AM EST is 10 AM UTC
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
    adjusted_unix_ms = unix_ms - DAWN_OFFSET_MS
    days, day_frac = divmod(adjusted_unix_ms / MILLISECONDS_PER_DAY, 1)

    years, year_frac = divmod(int(days) / DAYS_PER_YEAR, 1)

    days_with_offset = days + NUNDINAL_OFFSET

    years_whole = f"{int(years) % 8:0{YEARS_WHOLE}o}"
    years_frac = f"{int(year_frac * (8 ** YEARS_FRAC)):0{YEARS_FRAC}o}"
    days_whole = f"{int(days_with_offset) % 8:0{DAYS_WHOLE}o}"
    days_frac = f"{int(day_frac * (8 ** DAYS_FRAC)):0{DAYS_FRAC}o}"

    return (years_whole + years_frac + days_whole + days_frac)[::-1]


def decode_orbeat_time(orbeat_code, reference_unix_ms=None):
    """
    Find the most recent Unix timestamp for a given Orbeat code before a reference time.

    Args:
        orbeat_code: The Orbeat time string to decode.
        reference_unix_ms: The reference Unix timestamp in milliseconds.
                           Defaults to the current time if not provided.

    Returns:
        The Unix timestamp in milliseconds for the most recent occurrence.
    """
    rc = orbeat_code[::-1]
    yw, yf, dw, df = int(rc[0], 8), int(rc[1:3], 8), int(rc[3], 8), int(rc[4:], 8)
    ref_ms = (
        reference_unix_ms or datetime.now(timezone.utc).timestamp() * 1000
    ) - DAWN_OFFSET_MS
    for offset in range(int(8.5 * DAYS_PER_YEAR)):
        day = int(ref_ms / MILLISECONDS_PER_DAY) - offset
        if day < 0:
            break
        years, year_frac = divmod(day / DAYS_PER_YEAR, 1)
        if int(years) % 8 == yw and int(year_frac * 64) == yf and (day + 3) % 8 == dw:
            unix_ms = (day + (df + 0.5) / 4096) * MILLISECONDS_PER_DAY + DAWN_OFFSET_MS
            if (
                unix_ms < ref_ms + DAWN_OFFSET_MS
                and encode_orbeat_time(unix_ms) == orbeat_code
            ):
                return unix_ms


if __name__ == "__main__":  # pragma: no cover
    print("Demo Output:")
    current_date = datetime.now(timezone.utc).replace(microsecond=0)
    for i in range(8):
        future_date = current_date + timedelta(days=i)
        unix_ms = int(future_date.timestamp() * 1000)
        print(future_date.isoformat(), encode_orbeat_time(unix_ms), sep=" | ")

    print("\nDecoding Demo:")
    test_code = "02376765"
    decoded_ms = decode_orbeat_time(test_code)
    decoded_date = datetime.fromtimestamp(decoded_ms / 1000, tz=timezone.utc)
    print(f"Code '{test_code}' most recently occurred at: {decoded_date.isoformat()}")
