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
    A simple, two-step decoder that first finds the days, then the seconds.
    """
    if reference_unix_ms is None:
        reference_unix_ms = datetime.now(timezone.utc).timestamp() * 1000

    # Step 1: Walk back day-by-day to find the correct day.
    target_date_part = orbeat_code[::-1][:4]
    day_candidate_ms = reference_unix_ms
    found_day_ms = None
    for _ in range(365 * 10):  # Search back up to 10 years
        encoded_candidate = encode_orbeat_time(day_candidate_ms)
        if encoded_candidate[::-1][:4] == target_date_part:
            found_day_ms = day_candidate_ms
            break
        day_candidate_ms -= MILLISECONDS_PER_DAY

    if found_day_ms is None:
        raise ValueError("Could not find a matching date part in the search window.")

    # Step 2: Walk back second-by-second from the found day.
    # Start search 24h after the found timestamp to ensure we cover the whole day.
    time_candidate_ms = found_day_ms + MILLISECONDS_PER_DAY
    for _ in range(MILLISECONDS_PER_DAY // 1000):  # Search a full day
        if encode_orbeat_time(time_candidate_ms) == orbeat_code:
            return time_candidate_ms
        time_candidate_ms -= 10000

    raise ValueError("Found date part but could not find exact time match.")


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
