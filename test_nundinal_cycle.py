"""
Tests for 8-day Nundinal Cycle design decision.
Tests the proven Roman 8-day week structure as practical foundation.
"""

import pytest
from orbeat_time import to_parts_from_ms


class TestNundinalCycle:
    """Test the 8-day Nundinal Cycle design decision."""

    def test_day_cycle_is_8_days_pass(self):
        """PASS: Verify the day cycle repeats every 8 days."""
        base_time_ms = 1700000000000

        days = []
        for i in range(16):
            time_ms = base_time_ms + (i * 24 * 60 * 60 * 1000)
            _, _, day_oct, _ = to_parts_from_ms(time_ms)
            day_int = int(day_oct, 8)
            days.append(day_int)

        for i in range(8):
            assert days[i] == days[i + 8], f"Day {i} should equal day {i+8} in cycle"

    def test_day_values_range_0_to_7_pass(self):
        """PASS: Verify day values are in range 0-7."""
        test_times = [1700000000000, 1600000000000, 1800000000000, 1500000000000]

        for time_ms in test_times:
            _, _, day_oct, _ = to_parts_from_ms(time_ms)
            day_int = int(day_oct, 8)
            assert 0 <= day_int <= 7, f"Day {day_int} should be in range 0-7"

    def test_consecutive_days_increment_correctly_pass(self):
        """PASS: Verify consecutive days increment correctly with rollover."""
        base_time_ms = 1700000000000

        for i in range(10):
            time_ms = base_time_ms + (i * 24 * 60 * 60 * 1000)
            _, _, day_oct, _ = to_parts_from_ms(time_ms)
            day_int = int(day_oct, 8)
            expected_day = (int(to_parts_from_ms(base_time_ms)[2], 8) + i) % 8
            assert (
                day_int == expected_day
            ), f"Day {i}: expected {expected_day}, got {day_int}"

    def test_week_increments_every_8_days_pass(self):
        """PASS: Verify week increments after every 8 days."""
        base_time_ms = 1700000000000
        _, base_week_oct, _, _ = to_parts_from_ms(base_time_ms)
        base_week = int(base_week_oct, 8)

        time_plus_8_days = base_time_ms + (8 * 24 * 60 * 60 * 1000)
        _, week_oct, _, _ = to_parts_from_ms(time_plus_8_days)
        week_plus_8 = int(week_oct, 8)

        assert (
            week_plus_8 != base_week
        ), f"Week should change after 8 days: {base_week} vs {week_plus_8}"

    def test_day_cycle_not_7_days_fail(self):
        """FAIL: Day cycle should NOT be 7 days (like standard week)."""
        base_time_ms = 1700000000000

        days = []
        for i in range(14):
            time_ms = base_time_ms + (i * 24 * 60 * 60 * 1000)
            _, _, day_oct, _ = to_parts_from_ms(time_ms)
            day_int = int(day_oct, 8)
            days.append(day_int)

        with pytest.raises(AssertionError):
            for i in range(7):
                assert days[i] == days[i + 7], f"Should NOT have 7-day cycle"

    def test_day_values_not_exceed_7_fail(self):
        """FAIL: Day values should never exceed 7 in octal (base-8) system."""
        test_times = [1700000000000 + (i * 24 * 60 * 60 * 1000) for i in range(100)]

        for time_ms in test_times:
            _, _, day_oct, _ = to_parts_from_ms(time_ms)
            day_int = int(day_oct, 8)

            assert day_int <= 7, f"Day value {day_int} should never exceed 7"

            assert (
                "8" not in day_oct and "9" not in day_oct
            ), f"Invalid octal digit in day: {day_oct}"
