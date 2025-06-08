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
    if reference_unix_ms is None:
        reference_unix_ms = datetime.now(timezone.utc).timestamp() * 1000

    adjusted_reference_unix_ms = reference_unix_ms - DAWN_OFFSET_MS

    if not isinstance(orbeat_code, str) or len(orbeat_code) != 8:
        raise ValueError("Invalid Orbeat code format: Must be an 8-character string.")

    reversed_code = orbeat_code[::-1]
    yw_str = reversed_code[0:YEARS_WHOLE]
    yf_str = reversed_code[YEARS_WHOLE : YEARS_WHOLE + YEARS_FRAC]
    dw_str = reversed_code[
        YEARS_WHOLE + YEARS_FRAC : YEARS_WHOLE + YEARS_FRAC + DAYS_WHOLE
    ]
    df_str = reversed_code[YEARS_WHOLE + YEARS_FRAC + DAYS_WHOLE :]

    try:
        yw_oct = int(yw_str, 8)
        yf_oct = int(yf_str, 8)
        dw_oct = int(dw_str, 8)
        df_oct = int(df_str, 8)
    except ValueError:
        raise ValueError("Invalid Orbeat code format")

    target_day_plus_frac = (df_oct + 0.5) / (8**DAYS_FRAC)
    day_of_reference = int((adjusted_reference_unix_ms - 1e-9) / MILLISECONDS_PER_DAY)
    max_search_days_offset = int(8.5 * DAYS_PER_YEAR)

    for d_offset in range(max_search_days_offset):
        d_candidate = day_of_reference - d_offset

        if d_candidate < 0:
            break

        years_val_cand, year_frac_val_cand = divmod(d_candidate / DAYS_PER_YEAR, 1)
        years_val_cand = int(years_val_cand)

        calc_yw_oct_cand = years_val_cand % 8
        calc_yf_oct_cand = int(year_frac_val_cand * (8**YEARS_FRAC))
        calc_dw_oct_cand = int(d_candidate + NUNDINAL_OFFSET) % 8

        if (
            calc_yw_oct_cand == yw_oct
            and calc_yf_oct_cand == yf_oct
            and calc_dw_oct_cand == dw_oct
        ):

            # candidate_unix_ms is in the shifted frame
            candidate_unix_ms_shifted = (
                d_candidate + target_day_plus_frac
            ) * MILLISECONDS_PER_DAY

            # Compare in the shifted frame
            if candidate_unix_ms_shifted < adjusted_reference_unix_ms:
                # To verify the Orbeat code, we need to convert the shifted timestamp
                # back to a true UTC timestamp before passing it to encode_orbeat_time,
                # as encode_orbeat_time expects a true UTC timestamp and applies the
                # DAWN_OFFSET_MS internally.
                actual_candidate_unix_ms_for_encoding_check = (
                    candidate_unix_ms_shifted + DAWN_OFFSET_MS
                )

                if (
                    encode_orbeat_time(actual_candidate_unix_ms_for_encoding_check)
                    == orbeat_code
                ):
                    return actual_candidate_unix_ms_for_encoding_check

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
