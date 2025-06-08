import pytest
import random
from datetime import datetime, timezone
from orbeat_time import encode_orbeat_time, decode_orbeat_time

EDGE_TEST_CASES = [
    ("1970-01-06T10:02:38+00:00", "70000000"),
    ("1970-01-06T10:19:51+00:00", "07000000"),
    ("1970-01-06T12:37:40+00:00", "00700000"),
    ("1970-01-07T07:00:10+00:00", "00070000"),
    ("1970-01-05T10:00:10+00:00", "00007000"),
    ("1970-02-15T10:00:10+00:00", "00000700"),
    ("1970-11-22T10:00:10+00:00", "00000070"),
    ("1977-01-01T10:00:10+00:00", "00000007"),
]

SAMPLE_SIZE = 1024
EXPECTED_FLOOR = SAMPLE_SIZE * 8 // 64 // 2
MAX_RANDOM_MS = 50 * 365 * 24 * 60 * 60 * 1000  # 50 years

# Generate random test samples for digit distribution testing
DIGIT_DISTRIBUTION_SAMPLES = [
    random.randint(0, MAX_RANDOM_MS) for _ in range(SAMPLE_SIZE)
]


@pytest.mark.parametrize("dt_str,expected", EDGE_TEST_CASES)
def test_encode_orbeat_time_valid_dates(dt_str, expected):
    dt = datetime.fromisoformat(dt_str)
    unix_ms = dt.timestamp() * 1000
    result = encode_orbeat_time(unix_ms)
    assert result == expected


@pytest.mark.parametrize("unix_ms_sample", DIGIT_DISTRIBUTION_SAMPLES)
def test_decode_orbeat_time_round_trip(unix_ms_sample):
    """
    Tests the encode-decode round trip consistency for a sample of timestamps.
    """
    orbeat_code = encode_orbeat_time(unix_ms_sample)
    reference_offset_ms = 25 * 1000
    decoded_ms = decode_orbeat_time(orbeat_code, unix_ms_sample + reference_offset_ms)
    time_difference_ms = abs(unix_ms_sample - decoded_ms)
    max_expected_difference_ms = ((1 / (8**4)) * 24 * 60 * 60 * 1000 / 2) + 100
    assert time_difference_ms < max_expected_difference_ms


def test_decode_orbeat_time_no_reference_ms():
    """Test decoding without a reference_unix_ms, should default to now."""
    now_ms = datetime.now(timezone.utc).timestamp() * 1000
    # Use a time far enough in the past that test execution time doesn't make it "now"
    past_ms = now_ms - 60000  # 60 seconds ago
    orbeat_code = encode_orbeat_time(past_ms)
    decoded_ms = decode_orbeat_time(orbeat_code)  # No reference_unix_ms
    time_difference_ms = abs(past_ms - decoded_ms)
    # Max diff: half quantum + tolerance for default reference time variance (e.g. 1-2 seconds)
    max_expected_difference_ms = (((1 / (8**4)) * 24 * 60 * 60 * 1000) / 2) + 2000
    assert time_difference_ms < max_expected_difference_ms


@pytest.mark.parametrize("unix_ms", DIGIT_DISTRIBUTION_SAMPLES)
def test_fuzz_sample(unix_ms):
    orbeat = encode_orbeat_time(unix_ms)
    assert isinstance(orbeat, str)
    assert len(orbeat) == 8
    assert all(c in "01234567" for c in orbeat)


def test_digit_distribution():
    counts = [[0] * 8 for _ in range(8)]

    for unix_ms in DIGIT_DISTRIBUTION_SAMPLES:
        orbeat = encode_orbeat_time(unix_ms)

        for pos, digit in enumerate(orbeat):
            counts[int(digit)][pos] += 1

    for digit in range(8):
        for pos in range(8):
            assert (
                counts[digit][pos] >= EXPECTED_FLOOR
            ), f"Test failed: Cell at digit {digit}, position {pos} has count {counts[digit][pos]}. Expected at least {EXPECTED_FLOOR}."


def test_encode_orbeat_time_epoch_zero():
    """Test encoding for Unix epoch (0 ms)."""
    # Unix epoch (1970-01-01T00:00:00Z) -> 0 ms
    # DAWN_OFFSET_MS is 10 hours (36,000,000 ms).
    # adjusted_unix_ms = 0 - 36,000,000 = -36,000,000 ms
    # days_float = -36000000 / 86400000 = -0.41666...
    # days, day_frac = divmod(-0.41666..., 1) => days = -1, day_frac = 0.58333...
    # NUNDINAL_OFFSET = 3
    # days_with_offset = -1 + 3 = 2
    # years_float = -1 / 365.25 = -0.00273...
    # years, year_frac = divmod(-0.00273..., 1) => years = -1, year_frac = 0.99726...
    #
    # yw = int(years) % 8 = -1 % 8 = 7
    # yf = int(year_frac * (8**2)) = int(0.99726... * 64) = 63 (octal 77)
    # dw = int(days_with_offset) % 8 = 2 % 8 = 2
    # df = int( (7/12) * (8**4) ) = int(2389.333...) = 2389 (octal 4525)
    # Expected code: (7_77_2_4525)[::-1] = "52542777"
    unix_ms_epoch = 0
    expected_orbeat_epoch = "52542777"  # Corrected from "03542777"
    assert encode_orbeat_time(unix_ms_epoch) == expected_orbeat_epoch
