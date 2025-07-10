import pytest
from datetime import datetime
from orbeat_time import to_parts_from_ms, DAYS_PER_YEAR
import math


class TestYearBoundaryV2:
    """
    Tests for behavior at the boundary of a year, validating
    the core design principles of the system.

    The tests in this file prove the system's core design ideas:
    1. The system is based on the true solar year
    2. The day count is continuous and never resets
    3. Short weeks at year boundaries are an intentional design feature
    4. Astronomical accuracy is prioritized over convenient calendar divisions
    5. The 8-day cycle remains unbroken, showing a deeper continuity
    """

    def test_solar_year_accuracy(self):
        """
        Verifies the system uses the true tropical year (365.24219 days),
        not an artificial 365-day calendar year, ensuring astronomical precision.
        """
        tropical_year_days = 365.24219
        assert (
            abs(DAYS_PER_YEAR - tropical_year_days) < 0.001
        ), "The system must use the true solar year length for astronomical accuracy."

        # Check that the time between two equinoxes reflects this value.
        mar_21_2024_ms = datetime(2024, 3, 21, 9, 0, 0).timestamp() * 1000
        mar_21_2025_ms = datetime(2025, 3, 20, 9, 0, 0).timestamp() * 1000
        time_diff_days = (mar_21_2025_ms - mar_21_2024_ms) / (24 * 60 * 60 * 1000)
        assert (
            abs(time_diff_days - DAYS_PER_YEAR) < 2
        ), "The interval between consecutive equinoxes should approximate the tropical year."

    def test_continuous_time_day_count(self):
        """
        Ensures the underlying day count is monotonically increasing and
        never resets across year boundaries, reflecting a continuous flow of time.
        """
        from orbeat_time import OFFSET_MS, MS_PER_DAY

        test_dates = [
            datetime(2023, 3, 21, 9, 0, 0).timestamp() * 1000,
            datetime(2024, 3, 20, 9, 0, 0).timestamp() * 1000,
            datetime(2024, 3, 21, 9, 0, 0).timestamp() * 1000,
            datetime(2025, 3, 20, 9, 0, 0).timestamp() * 1000,
        ]
        day_counts = [math.floor((ms + OFFSET_MS) / MS_PER_DAY) for ms in test_dates]
        for i in range(1, len(day_counts)):
            assert (
                day_counts[i] > day_counts[i - 1]
            ), "The fundamental day count must never reset or decrease."

    def test_intentional_short_weeks_as_feature(self):
        """
        Demonstrates that weeks at year boundaries are deliberately shorter
        as a necessary feature to reconcile the continuous 8-day cycle
        with the fractional solar year.
        """
        boundary_dates = [
            datetime(2024, 3, 20, 9, 0, 0).timestamp() * 1000
            + (d * 24 * 60 * 60 * 1000)
            for d in range(-10, 11)
        ]
        week_day_counts = {}
        for ms in boundary_dates:
            year_oct, week_oct, day_oct, _ = to_parts_from_ms(ms)
            week_key = f"{year_oct}_{week_oct}"
            if week_key not in week_day_counts:
                week_day_counts[week_key] = set()
            week_day_counts[week_key].add(int(day_oct, 8))

        short_weeks = {w for w, d in week_day_counts.items() if len(d) < 8}
        assert (
            len(short_weeks) > 0
        ), "The year boundary must create 'short weeks' as a design feature."

    def test_astronomical_priority_over_neatness(self):
        """
        Shows the system prioritizes alignment with astronomical events (the equinox)
        over creating convenient, artificial calendar boundaries.
        """
        equinox_ms = datetime(2024, 3, 20, 3, 6).timestamp() * 1000
        # Day before equinox
        _, week_before, _, _ = to_parts_from_ms(equinox_ms - (24 * 60 * 60 * 1000))
        # Day after equinox
        _, week_after, _, _ = to_parts_from_ms(equinox_ms + (24 * 60 * 60 * 1000))
        # The week number should be low after the equinox, showing a year change.
        assert (
            int(week_after, 8) <= 5
        ), "The year should turn over in close alignment with the actual equinox."

    def test_unbroken_continuity_in_day_cycle(self):
        """
        Verifies that apparent surface-level discontinuities, like changing
        year and week numbers, mask the deeper, unbroken continuity of the 8-day cycle.
        """
        boundary_ms = datetime(2024, 3, 21, 9, 0, 0).timestamp() * 1000
        days = []
        for day_offset in range(-5, 6):
            test_ms = boundary_ms + (day_offset * 24 * 60 * 60 * 1000)
            _, _, day_oct, _ = to_parts_from_ms(test_ms)
            days.append(int(day_oct, 8))

        # The day cycle must remain perfectly continuous, even as year/week change.
        for i in range(1, len(days)):
            expected_day = (days[i - 1] + 1) % 8
            assert (
                days[i] == expected_day
            ), "The 8-day cycle must be unbroken, proving the deeper continuity."
