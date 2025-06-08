import pytest
import random
from datetime import datetime, timezone
from orbeat_time import encode_orbeat_time, decode_orbeat_time

EDGE_TEST_CASES = [
    ("1970-01-06T00:02:38.203+00:00", "70000000"),
    ("1970-01-06T00:19:51.796+00:00", "07000000"),
    ("1970-01-06T02:37:40.546+00:00", "00700000"),
    ("1970-01-06T21:00:10.546+00:00", "00070000"),
    ("1970-01-05T00:00:10.546+00:00", "00007000"),
    ("1970-02-15T00:00:10.546+00:00", "00000700"),
    ("1970-11-22T00:00:10.546+00:00", "00000070"),
    ("1977-01-01T00:00:10.546+00:00", "00000007"),
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
