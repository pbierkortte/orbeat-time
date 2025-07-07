"""
Tests for Spring Equinox Foundation design decision.
Tests that the year begins on the Spring Equinox for practical alignment with natural cycles.
"""

import pytest
from datetime import datetime
from orbeat_time import to_parts_from_ms


class TestSpringEquinoxFoundation:
    """Test the Spring Equinox Foundation design decision."""

    def test_epoch_starts_at_spring_equinox_pass(self):
        """PASS: Verify epoch starts at March 21, 44 BCE at 09:00 UTC."""
        epoch_approximation_ms = -63549936000000
        year_oct, week_oct, day_oct, frac_oct = to_parts_from_ms(epoch_approximation_ms)
        year_int = int(year_oct, 8)
        assert year_int < 10, f"Expected year close to 0, got {year_int}"

    def test_spring_equinox_year_boundary_pass(self):
        """PASS: Verify new year starts around spring equinox."""
        march_21_2024 = datetime(2024, 3, 21, 9, 0, 0).timestamp() * 1000
        year_oct, week_oct, day_oct, frac_oct = to_parts_from_ms(march_21_2024)
        week_int = int(week_oct, 8)
        assert week_int < 5, f"Expected early week, got {week_int}"

    def test_winter_vs_spring_year_difference_pass(self):
        """PASS: Verify winter and spring are in different orbeat years."""
        dec_21_2023 = datetime(2023, 12, 21, 9, 0, 0).timestamp() * 1000
        march_21_2024 = datetime(2024, 3, 21, 9, 0, 0).timestamp() * 1000

        year_dec, _, _, _ = to_parts_from_ms(dec_21_2023)
        year_mar, _, _, _ = to_parts_from_ms(march_21_2024)

        year_dec_int = int(year_dec, 8)
        year_mar_int = int(year_mar, 8)

        assert (
            year_mar_int > year_dec_int
        ), f"March year {year_mar_int} should be > December year {year_dec_int}"

    def test_january_in_previous_orbeat_year_fail(self):
        """FAIL: January should NOT be in the same orbeat year as the following March."""
        jan_15_2024 = datetime(2024, 1, 15, 9, 0, 0).timestamp() * 1000
        march_21_2024 = datetime(2024, 3, 21, 9, 0, 0).timestamp() * 1000

        year_jan, _, _, _ = to_parts_from_ms(jan_15_2024)
        year_mar, _, _, _ = to_parts_from_ms(march_21_2024)

        year_jan_int = int(year_jan, 8)
        year_mar_int = int(year_mar, 8)

        with pytest.raises(AssertionError):
            assert (
                year_jan_int == year_mar_int
            ), f"January and March should NOT be in same orbeat year"
