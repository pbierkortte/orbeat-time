import random
import pytest
from orbeat import unix_ms_to_parts, unix_ms_to_parts_ref, DATUM_MS, MS_PER_DAY

YEARS_TO_TEST = 1000
SAMPLES_PER_YEAR = 100
TOTAL_SAMPLES = YEARS_TO_TEST * SAMPLES_PER_YEAR

from datetime import datetime, timezone


# Generate test cases
def generate_test_cases():
    """
    Generate timestamps for testing, spanning the Unix epoch.
    """
    random.seed(45)

    # Start 500 years before the Unix epoch (approx 1470 AD)
    # This ensures we test both negative and positive timestamps
    start_year_offset = 1470 - (-44)  # Years from 44 BCE to 1470 AD
    ms = DATUM_MS + (start_year_offset * 365.24219 * MS_PER_DAY)

    for i in range(YEARS_TO_TEST):
        ref_start_parts = unix_ms_to_parts_ref(ms)
        year_ms = int(ref_start_parts[4] * MS_PER_DAY)
        for _ in range(SAMPLES_PER_YEAR):
            offset = 0 if year_ms == 0 else random.randrange(year_ms)
            test_ms = ms + offset
            # Use datetime for readable test case ID
            try:
                dt = datetime.fromtimestamp(test_ms / 1000, tz=timezone.utc)
                yield pytest.param(test_ms, id=dt.isoformat())
            except (OverflowError, OSError):
                # Handle dates that are too far in the past/future for fromtimestamp
                yield pytest.param(test_ms, id=f"ms_{test_ms}")

        ms += year_ms


@pytest.mark.parametrize("test_ms", generate_test_cases())
def test_implementation_consistency(test_ms):
    """
    Verify that the optimized unix_ms_to_parts matches the reference.
    """
    ref_parts = unix_ms_to_parts_greedy(test_ms)
    new_parts = unix_ms_to_parts(test_ms)

    r_y, r_w, r_d, r_f, r_l, r_dr = ref_parts
    n_y, n_w, n_d, n_f, n_l, n_dr = new_parts

    # Assert that core components are identical
    identical_err = f"Mismatch in core parts for timestamp {test_ms}"
    assert (r_y, r_w, r_d, r_l) == (n_y, n_w, n_d, n_l), core_error_msg

    # Assert that fractional parts are close enough
    fraction_error_msg = f"Mismatch in fraction for timestamp {test_ms}"
    assert abs(r_f - n_f) < 1e-9, fraction_error_msg

    # Assert that drift calculations are close enough
    drift_error_msg = f"Mismatch in drift for timestamp {test_ms}"
    assert abs(r_dr - n_dr) < 1e-9, drift_error_msg
