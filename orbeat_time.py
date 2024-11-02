from datetime import datetime, timedelta, timezone

DAYS_PER_YEAR = 365.24219
MILLISECONDS_PER_DAY = 24 * 60 * 60 * 1000
YEARS_WHOLE = 1
YEARS_FRAC = 1
DAYS_WHOLE = 2
DAYS_FRAC = 4


def format_octal_part(value, whole_digits, frac_digits):
    whole_str = oct(int(value))[2:].zfill(whole_digits)[-whole_digits:]
    frac_value = value - int(value)
    frac_str = ""
    for _ in range(frac_digits):
        frac_value *= 8
        frac_str += str(int(frac_value))
        frac_value -= int(frac_value)
    return whole_str + frac_str


def encode_orbeat_time(unix_milliseconds):
    unix_days = unix_milliseconds / MILLISECONDS_PER_DAY
    unix_years = int(unix_days / DAYS_PER_YEAR)
    encoded_days = format_octal_part(unix_days, DAYS_WHOLE, DAYS_FRAC)
    encoded_years = format_octal_part(unix_years, YEARS_WHOLE, YEARS_FRAC)
    return "".join(reversed(encoded_years + encoded_days))


def test_orbeat_time():
    test_cases = [
        ("2024-11-02T23:42:17+00:00", "51775706"),
        ("2024-11-04T01:45:21+00:00", "35407706"), 
        ("2024-11-05T03:48:25+00:00", "11210006"),
        ("2024-11-06T05:51:29+00:00", "74711006"),
        ("2024-11-07T07:54:33+00:00", "50522006"),
        ("2024-11-08T09:57:37+00:00", "34233006"),
        ("2024-11-09T12:00:41+00:00", "10044006"),
        ("2024-11-10T14:03:45+00:00", "04545006")
    ]

    passed = 0
    failed = 0

    for dt_str, expected in test_cases:
        dt = datetime.fromisoformat(dt_str)
        unix_ms = dt.timestamp() * 1000
        result = encode_orbeat_time(unix_ms)
        
        if result == expected:
            passed += 1
            print(f"✅ PASS: {dt_str} -> {result}")
        else:
            failed += 1
            print(f"❌ FAIL: {dt_str}")
            print(f"   Expected: {expected}")
            print(f"   Got:      {result}")
            print(f"   UTC time: {dt.isoformat()}")
            print(f"   Unix ms:  {unix_ms}")

    print(f"\nTest Summary:")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total:  {passed + failed}")


if __name__ == "__main__":
    print("Demo Output:")
    current_date = datetime.now(timezone.utc).replace(microsecond=0)
    for i in range(8):
        future_date = current_date + timedelta(days=i)
        unix_ms = int(future_date.timestamp() * 1000) 
        print(future_date.isoformat(), encode_orbeat_time(unix_ms), sep=" | ")

    print("\nRunning Tests:")
    test_orbeat_time()
