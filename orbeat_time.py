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
    """
    if value < 0:
        raise ValueError("Value must be non-negative")
        
    try:
        whole_str = oct(int(value))[2:].zfill(whole_digits)[-whole_digits:]
        frac_value = value - int(value)
        frac_str = ""
        for _ in range(frac_digits):
            frac_value *= 8
            frac_str += str(int(frac_value))
            frac_value -= int(frac_value)
        return whole_str + frac_str
    except OverflowError:
        raise OverflowError("Value is too large to process")

def encode_orbeat_time(unix_milliseconds: float) -> str:
    """
    Encode Unix milliseconds timestamp into Orbeat time format.
    """
    if unix_milliseconds < 0:
        raise ValueError("Timestamp must be non-negative")
        
    unix_days = unix_milliseconds / MILLISECONDS_PER_DAY
    unix_years = int(unix_days) / DAYS_PER_YEAR  
    encoded_days = format_octal_part(unix_days, DAYS_WHOLE, DAYS_FRAC)
    encoded_years = format_octal_part(unix_years, YEARS_WHOLE, YEARS_FRAC)
    return "".join(reversed(encoded_years + encoded_days))

def test_orbeat_time() -> None:
    """
    Run test cases for Orbeat time encoding.
    """
    test_cases = [
        ("2024-11-13T12:21:48+00:00", "67040166"),
        ("2024-11-14T02:36:02+00:00", "37601166"),
        ("2024-11-14T16:50:16+00:00", "17451166"),
        ("2024-11-15T07:04:30+00:00", "76222166"),
        ("2024-11-15T21:18:44+00:00", "56072166"),
        ("2024-11-16T11:32:58+00:00", "36633176"),
        ("2024-11-17T01:47:12+00:00", "06404176"),
        ("2024-11-17T16:01:26+00:00", "65254176"),
    ]

    passed = 0
    failed = 0

    for dt_str, expected in test_cases:
        try:
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
        except Exception as e:
            failed += 1
            print(f"❌ FAIL: {dt_str}")
            print(f"   Error: {str(e)}")

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
