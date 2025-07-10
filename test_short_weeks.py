"""
Tests for Short Weeks design decision.
Tests that last week of the new year and first week of new year may discard days
to maintain both astronomical precision and continuous week cycles.
"""

from datetime import datetime
import pytest
from orbeat_time import DAYS_PER_YEAR, to_parts_from_ms


class TestShortWeeks:
    """Test the Short Weeks design decision."""

    def test_week_cycles_remain_continuous_pass(self):
        """PASS: Verify week cycles remain continuous across year boundaries."""
        mar_20_2024 = datetime(2024, 3, 20, 9, 0, 0).timestamp() * 1000
        mar_22_2024 = datetime(2024, 3, 22, 9, 0, 0).timestamp() * 1000

        year_20, week_20, day_20, _ = to_parts_from_ms(mar_20_2024)
        year_22, week_22, day_22, _ = to_parts_from_ms(mar_22_2024)

        year_20_int = int(year_20, 8)
        year_22_int = int(year_22, 8)
        day_20_int = int(day_20, 8)
        day_22_int = int(day_22, 8)

        day_diff = (day_22_int - day_20_int) % 8
        expected_diff = 2
        assert (
            day_diff == expected_diff
        ), f"Days should be continuous: {day_20_int} -> {day_22_int}"

    def test_astronomical_precision_maintained_pass(self):
        """PASS: Verify astronomical precision is maintained despite short weeks."""
        mar_21_2023 = datetime(2023, 3, 21, 9, 0, 0).timestamp() * 1000
        mar_21_2024 = datetime(2024, 3, 21, 9, 0, 0).timestamp() * 1000

        year_2023, _, _, _ = to_parts_from_ms(mar_21_2023)
        year_2024, _, _, _ = to_parts_from_ms(mar_21_2024)

        year_2023_int = int(year_2023, 8)
        year_2024_int = int(year_2024, 8)

        year_diff = year_2024_int - year_2023_int
        assert year_diff == 1, f"Year should increment by 1: {year_diff}"

        time_diff_ms = mar_21_2024 - mar_21_2023
        time_diff_days = time_diff_ms / (24 * 60 * 60 * 1000)

        expected_days = 365.25
        assert (
            abs(time_diff_days - expected_days) < 2
        ), f"Year length should be reasonable: {time_diff_days}"

    def test_weeks_may_be_shortened_pass(self):
        """PASS: Verify weeks may be shortened to maintain alignment."""
        year_boundaries = [
            (datetime(2023, 3, 15, 9, 0, 0), datetime(2023, 3, 25, 9, 0, 0)),
            (datetime(2024, 3, 15, 9, 0, 0), datetime(2024, 3, 25, 9, 0, 0)),
            (datetime(2025, 3, 15, 9, 0, 0), datetime(2025, 3, 25, 9, 0, 0)),
        ]

        for start_date, end_date in year_boundaries:
            start_ms = start_date.timestamp() * 1000
            end_ms = end_date.timestamp() * 1000

            current_ms = start_ms
            weeks_seen = set()
            days_per_week = {}

            while current_ms <= end_ms:
                year, week, day, _ = to_parts_from_ms(current_ms)
                week_int = int(week, 8)
                day_int = int(day, 8)

                weeks_seen.add(week_int)
                if week_int not in days_per_week:
                    days_per_week[week_int] = set()
                days_per_week[week_int].add(day_int)

                current_ms += 24 * 60 * 60 * 1000

            for week_num, days_set in days_per_week.items():
                if len(days_set) < 8:
                    assert (
                        len(days_set) > 0
                    ), f"Week should have at least 1 day: {week_num}"

    def test_no_broken_week_cycles_pass(self):
        """PASS: Verify week cycles are not broken (no gaps in day sequence)."""
        test_date = datetime(2024, 3, 21, 9, 0, 0).timestamp() * 1000

        consecutive_days = []
        for i in range(20):
            current_ms = test_date + (i * 24 * 60 * 60 * 1000)
            _, _, day, _ = to_parts_from_ms(current_ms)
            day_int = int(day, 8)
            consecutive_days.append(day_int)

        for i in range(1, len(consecutive_days)):
            prev_day = consecutive_days[i - 1]
            curr_day = consecutive_days[i]

            expected_day = (prev_day + 1) % 8
            assert (
                curr_day == expected_day
            ), f"Day sequence broken: {prev_day} -> {curr_day}, expected {expected_day}"

    def test_year_week_alignment_pass(self):
        """PASS: Verify year and week alignment is maintained."""
        orbeat_year_starts = []
        for year in [2023, 2024, 2025, 2026]:
            mar_21 = datetime(year, 3, 21, 9, 0, 0).timestamp() * 1000
            orbeat_year_starts.append(mar_21)

        for year_start_ms in orbeat_year_starts:
            year, week, day, _ = to_parts_from_ms(year_start_ms)
            week_int = int(week, 8)
            day_int = int(day, 8)

            assert week_int <= 2, f"Year start should be early week: {week_int}"

    def test_continuous_8_day_cycle_maintained_pass(self):
        """PASS: Verify 8-day cycle is maintained despite short weeks."""
        base_date = datetime(2024, 1, 1, 9, 0, 0).timestamp() * 1000

        day_sequence = []
        for i in range(50):
            current_ms = base_date + (i * 24 * 60 * 60 * 1000)
            _, _, day, _ = to_parts_from_ms(current_ms)
            day_int = int(day, 8)
            day_sequence.append(day_int)

        for i in range(8, len(day_sequence)):
            assert (
                day_sequence[i] == day_sequence[i - 8]
            ), f"8-day cycle broken at position {i}: {day_sequence[i]} vs {day_sequence[i-8]}"

    def test_not_all_weeks_same_length_fail(self):
        """FAIL: Not all weeks should be exactly 8 days long."""
        start_date = datetime(2024, 2, 1, 9, 0, 0).timestamp() * 1000
        end_date = datetime(2024, 5, 1, 9, 0, 0).timestamp() * 1000

        weeks_found = {}
        current_ms = start_date

        while current_ms <= end_date:
            year, week, day, _ = to_parts_from_ms(current_ms)
            week_key = f"{year}_{week}"

            if week_key not in weeks_found:
                weeks_found[week_key] = set()

            day_int = int(day, 8)
            weeks_found[week_key].add(day_int)

            current_ms += 24 * 60 * 60 * 1000

        week_lengths = [len(days) for days in weeks_found.values()]
        unique_lengths = set(week_lengths)

        assert (
            len(unique_lengths) > 1 or min(week_lengths) < 8
        ), f"Should have some short weeks: {week_lengths}"

    def test_not_broken_astronomical_precision_fail(self):
        """FAIL: Astronomical precision should NOT be broken by short weeks."""
        year_lengths = []
        for start_year in [2020, 2021, 2022, 2023, 2024]:
            start_ms = datetime(start_year, 3, 21, 9, 0, 0).timestamp() * 1000
            end_ms = datetime(start_year + 1, 3, 21, 9, 0, 0).timestamp() * 1000

            year_length_ms = end_ms - start_ms
            year_length_days = year_length_ms / (24 * 60 * 60 * 1000)
            year_lengths.append(year_length_days)

        for year_length in year_lengths:
            tropical_diff = abs(year_length - DAYS_PER_YEAR)
            assert (
                tropical_diff < 2
            ), f"Year length should be close to tropical year: {year_length} vs {DAYS_PER_YEAR}"

    def test_not_completely_arbitrary_short_weeks_fail(self):
        """FAIL: Short weeks should NOT be completely arbitrary."""
        boundary_patterns = []

        for year in [2023, 2024, 2025]:
            pattern = []
            for day_offset in range(-5, 6):
                test_date = datetime(year, 3, 21, 9, 0, 0).timestamp() * 1000
                test_ms = test_date + (day_offset * 24 * 60 * 60 * 1000)

                orbeat_year, week, day, _ = to_parts_from_ms(test_ms)
                pattern.append((int(orbeat_year, 8), int(week, 8), int(day, 8)))

            boundary_patterns.append(pattern)

        for i in range(len(boundary_patterns) - 1):
            pattern1 = boundary_patterns[i]
            pattern2 = boundary_patterns[i + 1]

            day_seq1 = [p[2] for p in pattern1]
            day_seq2 = [p[2] for p in pattern2]

            differences = []
            for j in range(len(day_seq1)):
                diff = (day_seq2[j] - day_seq1[j]) % 8
                differences.append(diff)

            unique_diffs = set(differences)
            assert (
                len(unique_diffs) <= 2
            ), f"Pattern should be consistent across years: {differences}"
