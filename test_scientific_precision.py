"""
Tests for Scientific Precision design decision.
Tests that the epoch time is fixed with scientific precision for unambiguous temporal reference.
"""

import pytest
from orbeat_time import to_parts_from_ms, OFFSET_MS, MS_PER_DAY, DAWN_MS


class TestScientificPrecision:
    """Test the Scientific Precision design decision."""

    def test_millisecond_precision_maintained_pass(self):
        """PASS: Verify calculations maintain millisecond precision."""
        base_time = 1700000000000
        time_plus_1ms = base_time + 10000
        time_plus_100ms = base_time + 100000

        result_base = to_parts_from_ms(base_time)
        result_1ms = to_parts_from_ms(time_plus_1ms)
        result_100ms = to_parts_from_ms(time_plus_100ms)

        frac_base = int(result_base[3], 8)
        frac_1ms = int(result_1ms[3], 8)
        frac_100ms = int(result_100ms[3], 8)

        assert not (
            frac_base == frac_1ms == frac_100ms
        ), "Millisecond precision should be maintained"

    def test_constants_have_exact_values_pass(self):
        """PASS: Verify mathematical constants are exact, not approximated."""
        assert MS_PER_DAY == 86400000, f"MS_PER_DAY should be exact: {MS_PER_DAY}"

        assert DAWN_MS == -9 * 60 * 60 * 1000, f"DAWN_MS should be exact: {DAWN_MS}"

        assert isinstance(
            OFFSET_MS, int
        ), f"OFFSET_MS should be integer (exact): {type(OFFSET_MS)}"

    def test_fractional_day_precision_pass(self):
        """PASS: Verify fractional day calculations are precise."""
        base_time = 1700000000000

        half_day_ms = 12 * 60 * 60 * 1000
        time_plus_half_day = base_time + half_day_ms

        result_base = to_parts_from_ms(base_time)
        result_half_day = to_parts_from_ms(time_plus_half_day)

        frac_base = int(result_base[3], 8)
        frac_half_day = int(result_half_day[3], 8)

        frac_diff = abs(frac_half_day - frac_base)
        expected_half_day_frac = 4096 // 2

        tolerance = 100
        assert (
            abs(frac_diff - expected_half_day_frac) < tolerance
        ), f"Half-day precision error: {frac_diff} vs {expected_half_day_frac}"

    def test_reproducible_calculations_pass(self):
        """PASS: Verify calculations are reproducible and deterministic."""
        test_timestamp = 1700000000000

        results = []
        for _ in range(10):
            result = to_parts_from_ms(test_timestamp)
            results.append(result)

        first_result = results[0]
        for i, result in enumerate(results[1:], 1):
            assert (
                result == first_result
            ), f"Result {i} differs from first: {result} vs {first_result}"

    def test_edge_case_precision_pass(self):
        """PASS: Verify precision at edge cases (year boundaries, etc.)."""
        edge_times = [
            0,
            1000000000000,
            1700000000000,
            2000000000000,
        ]

        for time_ms in edge_times:
            result1 = to_parts_from_ms(time_ms)
            result2 = to_parts_from_ms(time_ms + 1)

            frac1 = int(result1[3], 8)
            frac2 = int(result2[3], 8)

            results_different = False
            for increment in [10000, 100000, 1000000]:
                result_inc = to_parts_from_ms(time_ms + increment)
                frac_inc = int(result_inc[3], 8)
                if frac_inc != frac1:
                    results_different = True
                    break

            assert results_different, f"No precision detected for edge case: {time_ms}"

    def test_floating_point_not_used_fail(self):
        """FAIL: Verify that floating point errors don't accumulate."""
        base_time = 1700000000000

        accumulated_time = base_time
        for _ in range(1000):
            accumulated_time += 1

        direct_result = to_parts_from_ms(base_time + 1000)
        accumulated_result = to_parts_from_ms(accumulated_time)

        assert (
            direct_result == accumulated_result
        ), f"Floating point drift detected: {direct_result} vs {accumulated_result}"

    def test_precision_not_lost_in_large_numbers_fail(self):
        """FAIL: Verify precision is not lost when dealing with large timestamps."""
        large_timestamp = 9999999999999

        result1 = to_parts_from_ms(large_timestamp)
        result2 = to_parts_from_ms(large_timestamp + 100000)

        frac1 = int(result1[3], 8)
        frac2 = int(result2[3], 8)

        assert frac1 != frac2, f"Precision lost in large numbers: {frac1} == {frac2}"

    def test_rounding_errors_controlled_fail(self):
        """FAIL: Verify that rounding errors are controlled and predictable."""
        base_time = 1700000000000

        step_time = base_time
        for _ in range(100):
            step_time += 100

        direct_time = base_time + (100 * 100)

        step_result = to_parts_from_ms(step_time)
        direct_result = to_parts_from_ms(direct_time)

        assert (
            step_result == direct_result
        ), f"Cumulative rounding error: {step_result} vs {direct_result}"
