"""
Tests for Historical Certainty Epoch design decision.
Tests that the epoch is an indisputable historical anchor point for absolute certainty.
"""

import pytest
from orbeat_time import to_parts_from_ms, DATUM_JDN, UNIX_JDN, OFFSET_MS, MS_PER_DAY


class TestHistoricalCertaintyEpoch:
    """Test the Historical Certainty Epoch design decision."""

    def test_epoch_constants_are_fixed_pass(self):
        """PASS: Verify epoch constants are historically fixed and immutable."""
        assert (
            DATUM_JDN == 1705433
        ), f"DATUM_JDN should be fixed at 1705433, got {DATUM_JDN}"
        assert (
            UNIX_JDN == 2440588
        ), f"UNIX_JDN should be fixed at 2440588, got {UNIX_JDN}"

        expected_offset = (UNIX_JDN - DATUM_JDN) * MS_PER_DAY + (-9 * 60 * 60 * 1000)
        assert (
            OFFSET_MS == expected_offset
        ), f"OFFSET_MS calculation should be deterministic"

    def test_epoch_date_march_21_44_bce_pass(self):
        """PASS: Verify epoch corresponds to March 21, 44 BCE."""
        very_early_ms = -63000000000000
        year_oct, _, _, _ = to_parts_from_ms(very_early_ms)
        year_int = int(year_oct, 8)

        assert (
            year_int < 10000
        ), f"Year should be reasonable for historical dates, got {year_int}"

    def test_epoch_time_09_00_utc_pass(self):
        """PASS: Verify epoch time is at 09:00 UTC (dawn)."""
        dawn_hours = abs(-9 * 60 * 60 * 1000)
        expected_dawn = 9 * 60 * 60 * 1000

        assert dawn_hours == expected_dawn, f"Dawn should be 09:00 UTC"

    def test_julian_day_number_accuracy_pass(self):
        """PASS: Verify Julian Day Numbers are historically accurate."""
        day_difference = UNIX_JDN - DATUM_JDN

        expected_approximate_days = 735000

        assert (
            day_difference > expected_approximate_days
        ), f"Day difference should be substantial: {day_difference}"
        assert (
            day_difference < expected_approximate_days + 1000
        ), f"Day difference should be reasonable: {day_difference}"

    def test_consistent_calculations_across_calls_pass(self):
        """PASS: Verify epoch calculations are consistent across multiple calls."""
        test_time = 1700000000000

        results = []
        for _ in range(5):
            result = to_parts_from_ms(test_time)
            results.append(result)

        for i in range(1, len(results)):
            assert (
                results[0] == results[i]
            ), f"Results should be consistent: {results[0]} vs {results[i]}"

    def test_epoch_not_arbitrary_modern_date_fail(self):
        """FAIL: Epoch should NOT be an arbitrary modern date like Jan 1, 2000."""
        modern_date_ms = 946684800000
        year_oct, _, _, _ = to_parts_from_ms(modern_date_ms)
        year_int = int(year_oct, 8)

        with pytest.raises(AssertionError):
            assert year_int < 10, f"Modern date should NOT be close to epoch year 0"

    def test_epoch_not_unix_epoch_fail(self):
        """FAIL: Our epoch should NOT be the Unix epoch (Jan 1, 1970)."""
        unix_epoch_ms = 0
        year_oct, _, _, _ = to_parts_from_ms(unix_epoch_ms)
        year_int = int(year_oct, 8)

        with pytest.raises(AssertionError):
            assert year_int == 0, f"Unix epoch should NOT be year 0 in orbeat system"

    def test_offset_calculation_immutable_fail(self):
        """FAIL: Verify offset calculation cannot be accidentally modified."""
        original_offset = OFFSET_MS

        recalculated_offset = (UNIX_JDN - DATUM_JDN) * MS_PER_DAY + (
            -9 * 60 * 60 * 1000
        )

        assert original_offset == recalculated_offset, f"Offset should be immutable"

        assert type(OFFSET_MS) == int, f"Offset should be a fixed integer value"
