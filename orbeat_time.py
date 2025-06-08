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


def decode_orbeat_time(orbeat_code: str, reference_unix_ms: float = None) -> float:
    """
    Find the most recent Unix timestamp for a given Orbeat code before a reference time.

    Args:
        orbeat_code: The Orbeat time string to decode.
        reference_unix_ms: The reference Unix timestamp in milliseconds.
                           Defaults to the current time if not provided.

    Returns:
        The Unix timestamp in milliseconds for the most recent occurrence.
    """
    if not isinstance(orbeat_code, str) or len(orbeat_code) != 8:
        raise ValueError("Invalid Orbeat code format: Must be an 8-character string.")

    rc = orbeat_code[::-1]
    try:  # Target Orbeat components (yw_t, yf_t, dw_t, df_t) from reversed code
        yw_t, yf_t, dw_t, df_t = (
            int(rc[0], 8),
            int(rc[1:3], 8),
            int(rc[3], 8),
            int(rc[4:], 8),
        )
    except ValueError:
        raise ValueError("Invalid Orbeat code format")

    # Adjusted reference time and target day fraction (midpoint of df_t quantum)
    adj_ref_ms = (
        reference_unix_ms
        if reference_unix_ms is not None
        else datetime.now(timezone.utc).timestamp() * 1000
    ) - DAWN_OFFSET_MS
    day_frac_target = (df_t + 0.5) / (8**DAYS_FRAC)

    day_num_ref = int(
        (adj_ref_ms / MILLISECONDS_PER_DAY) - 1e-9
    )  # Start day for search (adj. frame), epsilon for float

    for offset in range(
        int(8.5 * DAYS_PER_YEAR)
    ):  # Max search window ~8.5 Orbeat years
        day_c = day_num_ref - offset  # Candidate day number
        if day_c < 0:
            break  # Cannot be before epoch

        # Candidate Orbeat components (mirroring encode logic for year/day whole parts)
        yr_c_f, yr_frac_c_f = divmod(day_c / DAYS_PER_YEAR, 1)

        if (
            int(yr_c_f) % 8 == yw_t
            and int(yr_frac_c_f * (8**YEARS_FRAC)) == yf_t
            and (day_c + NUNDINAL_OFFSET) % 8 == dw_t
        ):  # dw_c calculation inlined

            adj_ms_c = (
                day_c + day_frac_target
            ) * MILLISECONDS_PER_DAY  # Candidate ms (adjusted frame)
            if adj_ms_c < adj_ref_ms:  # Must be strictly before reference
                unix_ms_c = adj_ms_c + DAWN_OFFSET_MS  # Candidate ms (actual Unix)
                if (
                    encode_orbeat_time(unix_ms_c) == orbeat_code
                ):  # Final verification for df_t
                    return unix_ms_c

    raise ValueError("Could not find a matching timestamp in the search window.")


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
