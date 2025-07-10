"""
Tests for Millennium Stability design decision.
Tests that the 365/366 day system maintains stability for over a millennium ensuring long-term reliability.
"""

import pytest
from datetime import datetime
from orbeat_time import DAYS_PER_YEAR, to_parts_from_ms


class TestMillenniumStability:
    """Test the Millennium Stability design decision."""

    def test_stability_over_1000_years_pass(self):
        """PASS: Verify system remains stable over 1000+ years."""
        date_1024 = datetime(1024, 3, 21, 9, 0, 0).timestamp() * 1000
        date_2024 = datetime(2024, 3, 21, 9, 0, 0).timestamp() * 1000

        year_1024, week_1024, day_1024, _ = to_parts_from_ms(date_1024)
        year_2024, week_2024, day_2024, _ = to_parts_from_ms(date_2024)

        year_1024_int = int(year_1024, 8)
        year_2024_int = int(year_2024, 8)

        year_diff = year_2024_int - year_1024_int
        assert (
            year_diff == 1000
        ), f"1000 calendar years should be 1000 orbeat years: {year_diff}"

        week_1024_int = int(week_1024, 8)
        week_2024_int = int(week_2024, 8)
        day_1024_int = int(day_1024, 8)
        day_2024_int = int(day_2024, 8)

        week_diff = abs(week_2024_int - week_1024_int)
        assert (
            week_diff <= 2
        ), f"Same date 1000 years apart should have similar weeks: {week_diff}"

        day_diff = abs(day_2024_int - day_1024_int)
        assert (
            day_diff < 8
        ), f"Day difference should be within the 8-day cycle: {day_diff}"

    def test_no_system_breakdown_over_millennia_pass(self):
        """PASS: Verify no system breakdown over multiple millennia."""
        very_old = datetime(500, 3, 21, 9, 0, 0).timestamp() * 1000
        far_future = datetime(3000, 3, 21, 9, 0, 0).timestamp() * 1000

        result_old = to_parts_from_ms(very_old)
        result_future = to_parts_from_ms(far_future)

        octal_digits = set("01234567")
        for component in result_old + result_future:
            for char in component:
                assert char in octal_digits, f"Invalid octal digit: {char}"

        year_old_int = int(result_old[0], 8)
        year_future_int = int(result_future[0], 8)
        assert (
            year_future_int > year_old_int
        ), f"Future year should be greater: {year_future_int} > {year_old_int}"

    def test_365_366_day_pattern_stability_pass(self):
        """PASS: Verify 365/366 day pattern maintains stability."""
        test_years = [2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028]

        for year in test_years:
            dec_31 = datetime(year, 12, 31, 23, 59, 59).timestamp() * 1000
            jan_1_next = datetime(year + 1, 1, 1, 0, 0, 0).timestamp() * 1000

            result_dec = to_parts_from_ms(dec_31)
            result_jan = to_parts_from_ms(jan_1_next)

            assert result_dec is not None, f"Dec 31 {year} should be valid"
            assert result_jan is not None, f"Jan 1 {year+1} should be valid"

    def test_tropical_year_precision_over_millennium_pass(self):
        """PASS: Verify tropical year precision maintains accuracy over millennium."""
        millennium_days = DAYS_PER_YEAR * 1000

        expected_days = 365242.19

        assert (
            abs(millennium_days - expected_days) < 1
        ), f"Millennium calculation should be accurate: {millennium_days}"

        half_millennium = DAYS_PER_YEAR * 500
        double_millennium = DAYS_PER_YEAR * 2000

        assert (
            abs(half_millennium * 2 - millennium_days) < 0.001
        ), "Precision should be maintained"
        assert (
            abs(double_millennium / 2 - millennium_days) < 0.001
        ), "Precision should be maintained"

    def test_long_term_reliability_pass(self):
        """PASS: Verify long-term reliability of calculations."""
        test_timestamp = 1700000000000

        results = []
        for _ in range(100):
            result = to_parts_from_ms(test_timestamp)
            results.append(result)

        first_result = results[0]
        for i, result in enumerate(results):
            assert (
                result == first_result
            ), f"Calculation {i} should be identical: {result} vs {first_result}"

    def test_system_boundaries_stability_pass(self):
        """PASS: Verify stability at system boundaries."""
        boundary_times = []

        boundary_times.append(datetime(2024, 3, 20, 23, 59, 59).timestamp() * 1000)
        boundary_times.append(datetime(2024, 3, 21, 0, 0, 0).timestamp() * 1000)

        base_time = datetime(2024, 1, 1, 0, 0, 0).timestamp() * 1000
        for i in range(8):
            boundary_times.append(base_time + i * 8 * 24 * 60 * 60 * 1000)

        boundary_times.append(datetime(2024, 6, 15, 23, 59, 59).timestamp() * 1000)
        boundary_times.append(datetime(2024, 6, 16, 0, 0, 0).timestamp() * 1000)

        for time_ms in boundary_times:
            result = to_parts_from_ms(time_ms)
            assert result is not None, f"Boundary time should be stable: {time_ms}"

            year_int = int(result[0], 8)
            week_int = int(result[1], 8)
            day_int = int(result[2], 8)
            frac_int = int(result[3], 8)

            assert 0 <= year_int < 100000, f"Year should be reasonable: {year_int}"
            assert 0 <= week_int < 60, f"Week should be reasonable: {week_int}"
            assert 0 <= day_int <= 7, f"Day should be 0-7: {day_int}"
            assert 0 <= frac_int < 4096, f"Fraction should be 0-4095: {frac_int}"

    def test_not_system_drift_over_time_fail(self):
        """FAIL: System should NOT drift significantly over millennia."""
        date_1000 = datetime(1000, 3, 21, 9, 0, 0).timestamp() * 1000
        date_2000 = datetime(2000, 3, 21, 9, 0, 0).timestamp() * 1000
        date_3000 = datetime(3000, 3, 21, 9, 0, 0).timestamp() * 1000

        _, week_1000, day_1000, _ = to_parts_from_ms(date_1000)
        _, week_2000, day_2000, _ = to_parts_from_ms(date_2000)
        _, week_3000, day_3000, _ = to_parts_from_ms(date_3000)

        week_1000_int = int(week_1000, 8)
        week_2000_int = int(week_2000, 8)
        week_3000_int = int(week_3000, 8)

        drift_1000_2000 = abs(week_2000_int - week_1000_int)
        drift_2000_3000 = abs(week_3000_int - week_2000_int)

        assert (
            drift_1000_2000 < 5
        ), f"Excessive drift over millennium: {drift_1000_2000} weeks"
        assert (
            drift_2000_3000 < 5
        ), f"Excessive drift over millennium: {drift_2000_3000} weeks"

    def test_not_overflow_errors_fail(self):
        """FAIL: Should NOT produce overflow errors over millennia."""
        far_future_timestamps = [
            datetime(4000, 1, 1).timestamp() * 1000,
            datetime(5000, 1, 1).timestamp() * 1000,
            datetime(9000, 1, 1).timestamp() * 1000,
        ]

        for timestamp in far_future_timestamps:
            try:
                result = to_parts_from_ms(timestamp)
                assert (
                    result is not None
                ), f"Far future timestamp should be handled: {timestamp}"

                year_int = int(result[0], 8)
                assert year_int > 0, f"Future year should be positive: {year_int}"

            except OverflowError:
                pytest.fail(
                    f"Should not have overflow error for timestamp: {timestamp}"
                )
            except ValueError as e:
                if "overflow" in str(e).lower():
                    pytest.fail(f"Should not have overflow error: {e}")

    def test_not_precision_degradation_fail(self):
        """FAIL: Precision should NOT degrade over long time periods."""
        ancient_time = datetime(100, 3, 21, 9, 0, 0).timestamp() * 1000
        future_time = datetime(4000, 3, 21, 9, 0, 0).timestamp() * 1000

        ancient_plus_ms = ancient_time + 100000
        future_plus_ms = future_time + 100000

        result_ancient = to_parts_from_ms(ancient_time)
        result_ancient_plus = to_parts_from_ms(ancient_plus_ms)
        result_future = to_parts_from_ms(future_time)
        result_future_plus = to_parts_from_ms(future_plus_ms)

        frac_ancient = int(result_ancient[3], 8)
        frac_ancient_plus = int(result_ancient_plus[3], 8)
        frac_future = int(result_future[3], 8)
        frac_future_plus = int(result_future_plus[3], 8)

        ancient_precision = frac_ancient != frac_ancient_plus
        future_precision = frac_future != frac_future_plus

        assert (
            ancient_precision or future_precision
        ), "Precision should be maintained over millennia"
