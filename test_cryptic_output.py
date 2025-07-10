"""
Tests for Cryptic Output design decision.
Tests that the output is made cryptic via reversal and truncation to 8 characters for a compact code.
"""

import pytest, re
from orbeat_time import to_orbeat8, to_parts_from_ms


class TestCrypticOutput:
    """Test the Cryptic Output design decision."""

    def test_output_exactly_8_characters_pass(self):
        """PASS: Verify output is exactly 8 characters long."""
        test_times = [1700000000000, 1600000000000, 1800000000000, 0, 2000000000000]

        for test_time in test_times:
            orbeat_output = to_orbeat8(test_time)
            assert (
                len(orbeat_output) == 8
            ), f"Output should be exactly 8 chars: '{orbeat_output}' (len={len(orbeat_output)})"

    def test_string_reversal_applied_pass(self):
        """PASS: Verify string reversal is applied before truncation."""
        test_time = 1700000000000
        year_oct, week_oct, day_oct, frac_oct = to_parts_from_ms(test_time)

        original_concat = f"{year_oct}{week_oct}{day_oct}{frac_oct}"

        orbeat_output = to_orbeat8(test_time)

        expected_output = original_concat[::-1][:8]

        assert (
            orbeat_output == expected_output
        ), f"Expected {expected_output}, got {orbeat_output}"

    def test_truncation_to_8_chars_pass(self):
        """PASS: Verify truncation occurs after reversal."""
        test_time = 1700000000000
        year_oct, week_oct, day_oct, frac_oct = to_parts_from_ms(test_time)

        full_concat = f"{year_oct}{week_oct}{day_oct}{frac_oct}"
        assert (
            len(full_concat) > 8
        ), f"Full string should be longer than 8 chars: {full_concat}"

        orbeat_output = to_orbeat8(test_time)
        assert (
            len(orbeat_output) == 8
        ), f"After truncation should be 8 chars: {orbeat_output}"

    def test_compact_code_achieved_pass(self):
        """PASS: Verify the result is a compact code."""
        test_time = 1700000000000
        orbeat_output = to_orbeat8(test_time)

        assert len(orbeat_output) == 8, f"Should be compact 8 chars: {orbeat_output}"
        assert orbeat_output.isalnum(), f"Should be alphanumeric only: {orbeat_output}"
        assert " " not in orbeat_output, f"Should contain no spaces: {orbeat_output}"
        assert (
            "_" not in orbeat_output
        ), f"Should contain no underscores: {orbeat_output}"
        assert "." not in orbeat_output, f"Should contain no periods: {orbeat_output}"

    def test_cryptic_nature_obscures_meaning_pass(self):
        """PASS: Verify the output is cryptic and obscures meaning."""
        test_time = 1700000000000
        orbeat_output = to_orbeat8(test_time)
        year_oct, week_oct, day_oct, frac_oct = to_parts_from_ms(test_time)

        assert not orbeat_output.startswith(
            year_oct
        ), f"Output should not start with year: {orbeat_output}"

        assert not orbeat_output.startswith(
            week_oct
        ), f"Output should not start with week: {orbeat_output}"
        assert not orbeat_output.startswith(
            day_oct
        ), f"Output should not start with day: {orbeat_output}"

    def test_reversal_changes_order_pass(self):
        """PASS: Verify reversal actually changes the character order."""
        test_time = 1700000000000
        year_oct, week_oct, day_oct, frac_oct = to_parts_from_ms(test_time)

        original_concat = f"{year_oct}{week_oct}{day_oct}{frac_oct}"
        orbeat_output = to_orbeat8(test_time)

        original_first_8 = original_concat[:8]
        assert (
            orbeat_output != original_first_8
        ), f"Reversal should change order: {orbeat_output} vs {original_first_8}"

        reversed_concat = original_concat[::-1]
        expected_output = reversed_concat[:8]
        assert (
            orbeat_output == expected_output
        ), f"Should be reversed and truncated: {orbeat_output} vs {expected_output}"

    def test_different_times_produce_different_outputs_pass(self):
        """PASS: Verify different timestamps produce different cryptic outputs."""
        test_times = [1700000000000, 1700000001000, 1700001000000, 1701000000000]
        test_times[1] += 10000000
        outputs = []

        for test_time in test_times:
            output = to_orbeat8(test_time)
            outputs.append(output)

        unique_outputs = set(outputs)
        assert len(unique_outputs) == len(
            outputs
        ), f"Different times should produce different outputs: {outputs}"

    def test_not_human_readable_format_fail(self):
        """FAIL: Output should NOT be in human-readable format."""
        test_time = 1700000000000
        orbeat_output = to_orbeat8(test_time)

        human_readable_patterns = [
            r"\d{4}-\d{2}-\d{2}",
            r"\d{2}/\d{2}/\d{4}",
            r"\d{4}_\d{2}_\d",
        ]

        for pattern in human_readable_patterns:
            with pytest.raises(AssertionError):
                assert re.match(
                    pattern, orbeat_output
                ), f"Should NOT match human-readable pattern {pattern}"

    def test_not_just_truncation_fail(self):
        """FAIL: Should NOT be just truncation without reversal."""
        test_time = 1700000000000
        year_oct, week_oct, day_oct, frac_oct = to_parts_from_ms(test_time)

        original_concat = f"{year_oct}{week_oct}{day_oct}{frac_oct}"
        orbeat_output = to_orbeat8(test_time)

        just_truncated = original_concat[:8]
        with pytest.raises(AssertionError):
            assert (
                orbeat_output == just_truncated
            ), f"Should NOT be just truncation: {orbeat_output} vs {just_truncated}"

    def test_not_longer_than_8_chars_fail(self):
        """FAIL: Output should NOT be longer than 8 characters."""
        test_times = [1700000000000, 0, 9999999999999]

        for test_time in test_times:
            orbeat_output = to_orbeat8(test_time)

            assert (
                len(orbeat_output) <= 8
            ), f"Should never exceed 8 chars: '{orbeat_output}' (len={len(orbeat_output)})"

            with pytest.raises(AssertionError):
                assert (
                    len(orbeat_output) < 8
                ), f"Should be exactly 8 chars, not less: '{orbeat_output}'"

    def test_reversal_algorithm_deterministic_fail(self):
        """FAIL: Verify reversal is deterministic and repeatable."""
        test_time = 1700000000000

        outputs = []
        for _ in range(5):
            output = to_orbeat8(test_time)
            outputs.append(output)

        first_output = outputs[0]
        for i, output in enumerate(outputs[1:], 1):
            assert (
                output == first_output
            ), f"Reversal should be deterministic: call {i} differs"

        year_oct, week_oct, day_oct, frac_oct = to_parts_from_ms(test_time)
        full_concat = f"{year_oct}{week_oct}{day_oct}{frac_oct}"
        manual_reversal = full_concat[::-1][:8]

        assert (
            first_output == manual_reversal
        ), f"Should match manual reversal: {first_output} vs {manual_reversal}"
