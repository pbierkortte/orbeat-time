from datetime import datetime, timezone

DAYS_PER_YEAR = 365.25
MILLISECONDS_PER_DAY = 24 * 60 * 60 * 1000
YEARS_WHOLE = 1
YEARS_FRAC = 2
DAYS_WHOLE = 1
DAYS_FRAC = 4


def format_octal_part(value, whole_digits, frac_digits):
    whole_value, frac_value = divmod(value if value >= 0 else 0, 1)
    whole_str = (
        oct(int(whole_value))[2:].zfill(whole_digits)[-whole_digits:]
        if whole_digits > 0
        else ""
    )
    frac_str = (
        oct(int(frac_value * 8**frac_digits))[2:].zfill(frac_digits)[-frac_digits:]
        if frac_digits > 0
        else ""
    )
    return whole_str + frac_str


def encode_orbeat_time(unix_milliseconds):
    unix_days = (
        unix_milliseconds if unix_milliseconds > 0 else 0
    ) / MILLISECONDS_PER_DAY
    unix_years = int(unix_days) / DAYS_PER_YEAR
    encoded_days = format_octal_part(unix_days, DAYS_WHOLE, DAYS_FRAC)
    encoded_years = format_octal_part(unix_years, YEARS_WHOLE, YEARS_FRAC)
    return "".join(reversed(encoded_years + encoded_days))


if __name__ == "__main__":
    print(encode_orbeat_time(int(datetime.now(timezone.utc).timestamp() * 1000)))
