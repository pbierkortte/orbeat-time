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


def test_decode_orbeat_time_invalid_code_format():
    """Test decoding with an invalid Orbeat code format (covers lines 65-66)."""
    with pytest.raises(ValueError, match="Invalid Orbeat code format"):
        decode_orbeat_time("INVALID!", 0)  # Invalid characters
    with pytest.raises(
        ValueError, match="Invalid Orbeat code format: Must be an 8-character string."
    ):
        decode_orbeat_time("1234567", 0)  # Too short
    with pytest.raises(
        ValueError, match="Invalid Orbeat code format"
    ):  # This will be caught by int(..., 8)
        decode_orbeat_time("00000008", 0)  # Invalid octal digit '8'


def test_decode_orbeat_time_not_found_in_window():
    """Test decoding a code that won't be found (hits line 99)."""
    # Code from 20 years in the future
    # future_timestamp = datetime(2045, 1, 1, tzinfo=timezone.utc).timestamp() * 1000
    # orbeat_code_future = encode_orbeat_time(future_timestamp) # Original: some value
    # With 10h offset, new code for 2045-01-01T00:00:00Z is "61633772"
    orbeat_code_future = "61633772"
    # Reference time is 10 days after epoch, search window is ~8.5 years
    reference_near_epoch_ms = 10 * 24 * 60 * 60 * 1000
    with pytest.raises(
        ValueError, match="Could not find a matching timestamp in the search window."
    ):
        decode_orbeat_time(orbeat_code_future, reference_near_epoch_ms)


def test_decode_orbeat_time_search_goes_before_epoch_and_not_found():
    """
    Test that search stops if d_candidate < 0 (hits line 76),
    and then raises ValueError if no prior match was found (hits line 99).
    """
    # An Orbeat code for a date far from epoch, e.g., 1978-01-01
    # (Year 8 from epoch, day 2922 from epoch if epoch is day 0)
    # yw_oct = (1978-1970) % 8 = 0
    # yf_oct = 0
    # dw_oct = (2922 + NUNDINAL_OFFSET) % 8 = (2922 + 3) % 8 = 2925 % 8 = 5
    # df_oct = 0 (assuming start of day)
    # Reversed code: 00005000 -> Original code "00050000"
    code_1978_start_of_day = "00050000"

    # Set reference_unix_ms to 1ms after epoch.
    # day_of_reference will be 0.
    # The loop for d_offset will make d_candidate negative quickly.
    # Since code_1978_start_of_day is for 1978, it won't be found at d_candidate = 0.
    # The loop should break due to d_candidate < 0, then raise ValueError.
    with pytest.raises(
        ValueError, match="Could not find a matching timestamp in the search window."
    ):
        decode_orbeat_time(code_1978_start_of_day, reference_unix_ms=1)


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
