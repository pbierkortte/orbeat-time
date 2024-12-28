from datetime import datetime, timedelta, timezone

DAYS_PER_YEAR = 365.24219
MILLISECONDS_PER_DAY = 24 * 60 * 60 * 1000
YEARS_WHOLE = 1
YEARS_FRAC = 1
DAYS_WHOLE = 2
DAYS_FRAC = 4


def format_octal_part(value: float, whole_digits: int, frac_digits: int) -> str:
    """
    Format a number into octal with specified whole and fractional digits.

    Args:
        value: The number to format
        whole_digits: Number of digits before decimal (0 to skip)
        frac_digits: Number of digits after decimal (0 to skip)

    Returns:
        Formatted octal string
    """

    whole_value, frac_value = divmod(value if value >= 0 else 0, 1)
    whole_str = oct(int(whole_value))[2:].zfill(whole_digits)[-whole_digits:] if whole_digits > 0 else ''
    frac_str = oct(int(frac_value * 8**frac_digits))[2:].zfill(frac_digits)[-frac_digits:] if frac_digits > 0 else ''
    return whole_str + frac_str


def encode_orbeat_time(unix_milliseconds: float) -> str:
    """
    Encode Unix milliseconds timestamp into Orbeat time format.

    Args:
        unix_milliseconds: Unix timestamp in milliseconds

    Returns:
        Encoded Orbeat time string

    Raises:
        ValueError: If timestamp is negative
    """
    if unix_milliseconds < 0:
        raise ValueError("Timestamp must be non-negative")

    unix_days = unix_milliseconds / MILLISECONDS_PER_DAY
    unix_years = int(unix_days) / DAYS_PER_YEAR
    encoded_days = format_octal_part(unix_days, DAYS_WHOLE, DAYS_FRAC)
    encoded_years = format_octal_part(unix_years, YEARS_WHOLE, YEARS_FRAC)
    return "".join(reversed(encoded_years + encoded_days))


if __name__ == "__main__":
    print("Demo Output:")
    current_date = datetime.now(timezone.utc).replace(microsecond=0)
    for i in range(8):
        future_date = current_date + timedelta(days=i)
        unix_ms = int(future_date.timestamp() * 1000)
        print(future_date.isoformat(), encode_orbeat_time(unix_ms), sep=" | ")
