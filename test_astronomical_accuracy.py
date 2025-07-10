"""
Tests for Astronomical Accuracy design decision.
Tests the Mean Tropical Year of 365.24219 days prevents seasonal drift and ensures perpetual accuracy.
"""

import pytest
from datetime import datetime
from orbeat_time import DAYS_PER_YEAR, to_parts_from_ms


class TestAstronomicalAccuracy:
    """Test the Astronomical Accuracy design decision."""

    def test_mean_tropical_year_constant_pass(self):
        """PASS: Verify Mean Tropical Year is exactly 365.24219 days."""
        assert (
            DAYS_PER_YEAR == 365.24219
        ), f"DAYS_PER_YEAR should be 365.24219, got {DAYS_PER_YEAR}"

        assert isinstance(
            DAYS_PER_YEAR, float
        ), f"DAYS_PER_YEAR should be float for precision"

        assert (
            abs(DAYS_PER_YEAR - 365.24219) < 0.000001
        ), f"Insufficient precision in DAYS_PER_YEAR"

    def test_year_length_accuracy_prevents_drift_pass(self):
        """PASS: Verify year calculations use astronomical accuracy to prevent drift."""
        base_time = 1700000000000

        one_tropical_year_ms = int(DAYS_PER_YEAR * 24 * 60 * 60 * 1000)
        time_plus_year = base_time + one_tropical_year_ms

        year1, _, _, _ = to_parts_from_ms(base_time)
        year2, _, _, _ = to_parts_from_ms(time_plus_year)

        year1_int = int(year1, 8)
        year2_int = int(year2, 8)

        year_diff = year2_int - year1_int
        assert (
            year_diff == 1
        ), f"One tropical year should advance exactly 1 orbeat year: {year_diff}"

    def test_not_calendar_year_365_days_pass(self):
        """PASS: Verify we don't use simple 365-day calendar year."""
        assert DAYS_PER_YEAR > 365, f"Tropical year should be longer than calendar year"

        assert DAYS_PER_YEAR < 366, f"Tropical year should be less than leap year"

        fractional_part = DAYS_PER_YEAR - 365
        assert (
            fractional_part > 0.2
        ), f"Fractional part should be significant: {fractional_part}"
        assert (
            fractional_part < 0.3
        ), f"Fractional part should be reasonable: {fractional_part}"

    def test_seasonal_alignment_maintained_pass(self):
        """PASS: Verify seasonal alignment is maintained over long periods."""

        march_21_2024 = datetime(2024, 3, 21, 9, 0, 0).timestamp() * 1000
        march_21_2025 = datetime(2025, 3, 21, 9, 0, 0).timestamp() * 1000
        march_21_2026 = datetime(2026, 3, 21, 9, 0, 0).timestamp() * 1000

        _, week1, day1, _ = to_parts_from_ms(march_21_2024)
        _, week2, day2, _ = to_parts_from_ms(march_21_2025)
        _, week3, day3, _ = to_parts_from_ms(march_21_2026)

        week1_int = int(week1, 8)
        week2_int = int(week2, 8)
        week3_int = int(week3, 8)

        max_week_diff = max(week1_int, week2_int, week3_int) - min(
            week1_int, week2_int, week3_int
        )
        assert (
            max_week_diff <= 2
        ), f"March 21st should be consistent across years: weeks {week1_int}, {week2_int}, {week3_int}"

    def test_long_term_accuracy_pass(self):
        """PASS: Verify accuracy is maintained over centuries."""

        march_21_1924 = datetime(1924, 3, 21, 9, 0, 0).timestamp() * 1000
        march_21_2024 = datetime(2024, 3, 21, 9, 0, 0).timestamp() * 1000

        year1, week1, _, _ = to_parts_from_ms(march_21_1924)
        year2, week2, _, _ = to_parts_from_ms(march_21_2024)

        year1_int = int(year1, 8)
        year2_int = int(year2, 8)
        week1_int = int(week1, 8)
        week2_int = int(week2, 8)

        year_diff = year2_int - year1_int
        assert (
            year_diff == 100
        ), f"100 calendar years should be 100 orbeat years: {year_diff}"

        week_diff = abs(week2_int - week1_int)
        assert (
            week_diff <= 2
        ), f"Century apart March 21st should have similar weeks: {week1_int} vs {week2_int}"

    def test_not_simple_365_25_approximation_fail(self):
        """FAIL: Should NOT use simple 365.25 leap year approximation."""
        simple_approximation = 365.25

        with pytest.raises(AssertionError):
            assert (
                DAYS_PER_YEAR == simple_approximation
            ), f"Should NOT use simple 365.25 approximation"

    def test_not_integer_days_per_year_fail(self):
        """FAIL: Year length should NOT be an integer number of days."""
        with pytest.raises(AssertionError):
            assert DAYS_PER_YEAR == int(
                DAYS_PER_YEAR
            ), f"Year length should NOT be integer days"

    def test_not_sidereal_year_fail(self):
        """FAIL: Should NOT use sidereal year (365.25636 days)."""
        sidereal_year = 365.25636

        with pytest.raises(AssertionError):
            assert (
                abs(DAYS_PER_YEAR - sidereal_year) < 0.001
            ), f"Should NOT use sidereal year"

    def test_precision_prevents_drift_fail(self):
        """FAIL: Verify insufficient precision would cause drift."""
        low_precision = 365.24
        high_precision = DAYS_PER_YEAR

        years = 1000
        low_precision_total_days = low_precision * years
        high_precision_total_days = high_precision * years

        day_difference = abs(high_precision_total_days - low_precision_total_days)

        assert (
            day_difference > 2
        ), f"Precision matters for long-term accuracy: {day_difference} days difference"

    def test_tropical_year_definition_accuracy_fail(self):
        """FAIL: Verify we use the correct definition of tropical year."""
        historical_approximations = [365.242199, 365.2422, 365.242]

        for approx in historical_approximations:
            if abs(DAYS_PER_YEAR - approx) < 0.00001:
                continue
            else:
                with pytest.raises(AssertionError):
                    assert (
                        DAYS_PER_YEAR == approx
                    ), f"Should use precise modern tropical year value"
