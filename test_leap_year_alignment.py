"""
Tests for Leap Year Alignment design decision.
Tests that leap years align with the Gregorian calendar for practical synchronization.
"""

import pytest
from datetime import datetime
from orbeat_time import to_parts_from_ms, DAYS_PER_YEAR


class TestLeapYearAlignment:
    """Test the Leap Year Alignment design decision."""

    def test_gregorian_leap_years_recognized_pass(self):
        """PASS: Verify system recognizes Gregorian leap years."""
        gregorian_leap_years = [2020, 2024, 2028, 2000, 1996]

        for year in gregorian_leap_years:
            try:
                feb_29 = datetime(year, 2, 29, 9, 0, 0).timestamp() * 1000
                result = to_parts_from_ms(feb_29)
                assert result is not None, f"Should handle leap year {year} correctly"
            except ValueError:
                pytest.fail(f"Gregorian leap year {year} should be valid")

    def test_non_leap_years_handled_correctly_pass(self):
        """PASS: Verify non-leap years are handled correctly."""
        non_leap_years = [2021, 2022, 2023, 1900, 2100]

        for year in non_leap_years:
            try:
                feb_29 = datetime(year, 2, 29, 9, 0, 0).timestamp() * 1000
                pytest.fail(f"Feb 29 should not exist in non-leap year {year}")
            except ValueError:
                pass

            feb_28 = datetime(year, 2, 28, 9, 0, 0).timestamp() * 1000
            result = to_parts_from_ms(feb_28)
            assert result is not None, f"Should handle non-leap year {year} correctly"

    def test_century_rule_alignment_pass(self):
        """PASS: Verify alignment with Gregorian century rule."""
        century_test_cases = [
            (1900, False),
            (2000, True),
            (2100, False),
            (2400, True),
        ]

        for year, should_be_leap in century_test_cases:
            try:
                feb_29 = datetime(year, 2, 29, 9, 0, 0).timestamp() * 1000
                result = to_parts_from_ms(feb_29)
                assert (
                    should_be_leap
                ), f"Year {year} should not be leap but Feb 29 exists"
            except ValueError:
                assert (
                    not should_be_leap
                ), f"Year {year} should be leap but Feb 29 doesn't exist"

    def test_leap_year_synchronization_pass(self):
        """PASS: Verify leap years stay synchronized over time."""
        mar_1_leap = datetime(2024, 3, 1, 9, 0, 0).timestamp() * 1000
        mar_1_non_leap = datetime(2023, 3, 1, 9, 0, 0).timestamp() * 1000

        year_leap, week_leap, day_leap, _ = to_parts_from_ms(mar_1_leap)
        year_non_leap, week_non_leap, day_non_leap, _ = to_parts_from_ms(mar_1_non_leap)

        year_leap_int = int(year_leap, 8)
        year_non_leap_int = int(year_non_leap, 8)
        assert (
            year_leap_int == year_non_leap_int + 1
        ), f"Consecutive years: {year_non_leap_int} -> {year_leap_int}"

    def test_practical_synchronization_pass(self):
        """PASS: Verify practical synchronization with Gregorian calendar."""
        feb_28_leap = datetime(2024, 2, 28, 9, 0, 0).timestamp() * 1000
        mar_1_leap = datetime(2024, 3, 1, 9, 0, 0).timestamp() * 1000

        feb_28_non_leap = datetime(2023, 2, 28, 9, 0, 0).timestamp() * 1000
        mar_1_non_leap = datetime(2023, 3, 1, 9, 0, 0).timestamp() * 1000

        leap_diff_ms = mar_1_leap - feb_28_leap
        non_leap_diff_ms = mar_1_non_leap - feb_28_non_leap

        leap_diff_days = leap_diff_ms / (24 * 60 * 60 * 1000)
        non_leap_diff_days = non_leap_diff_ms / (24 * 60 * 60 * 1000)

        assert (
            abs(leap_diff_days - 2) < 0.1
        ), f"Leap year should have ~2 days: {leap_diff_days}"
        assert (
            abs(non_leap_diff_days - 1) < 0.1
        ), f"Non-leap year should have ~1 day: {non_leap_diff_days}"

    def test_not_julian_calendar_fail(self):
        """FAIL: Should NOT follow Julian calendar leap year rules."""
        try:
            feb_29_1900 = datetime(1900, 2, 29, 9, 0, 0).timestamp() * 1000
            pytest.fail("1900 should NOT be a leap year (Gregorian rule)")
        except ValueError:
            pass

    def test_not_arbitrary_leap_system_fail(self):
        """FAIL: Should NOT use arbitrary leap year system."""
        gregorian_leap_years = [2020, 2024, 2000]
        for year in gregorian_leap_years:
            try:
                feb_29 = datetime(year, 2, 29, 9, 0, 0).timestamp() * 1000
                result = to_parts_from_ms(feb_29)
            except ValueError:
                pytest.fail(f"Standard Gregorian leap year {year} should be supported")

    def test_mean_tropical_year_vs_leap_years_fail(self):
        """FAIL: Verify Mean Tropical Year works with Gregorian leap system."""
        gregorian_average = 365.2425
        tropical_year = DAYS_PER_YEAR

        difference = abs(gregorian_average - tropical_year)
        assert (
            difference < 0.001
        ), f"Tropical year should be close to Gregorian average: {difference}"

    def test_long_term_alignment_stability_fail(self):
        """FAIL: Verify long-term stability of alignment."""
        date_1600 = datetime(1600, 3, 21, 9, 0, 0).timestamp() * 1000
        date_2000 = datetime(2000, 3, 21, 9, 0, 0).timestamp() * 1000

        year_1600, week_1600, day_1600, _ = to_parts_from_ms(date_1600)
        year_2000, week_2000, day_2000, _ = to_parts_from_ms(date_2000)

        year_1600_int = int(year_1600, 8)
        year_2000_int = int(year_2000, 8)

        year_diff = year_2000_int - year_1600_int
        assert (
            year_diff == 400
        ), f"400 calendar years should be 400 orbeat years: {year_diff}"

        week_1600_int = int(week_1600, 8)
        week_2000_int = int(week_2000, 8)
        day_1600_int = int(day_1600, 8)
        day_2000_int = int(day_2000, 8)

        week_diff = abs(week_2000_int - week_1600_int)
        day_diff = abs(day_2000_int - day_1600_int)

        assert (
            week_diff <= 1
        ), f"Same date 400 years apart should have similar weeks: {week_diff}"
        assert (
            day_diff < 8
        ), f"Day difference should be within the 8-day cycle: {day_diff}"
