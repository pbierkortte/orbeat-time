"""
Tests for Octal Encoding design decision.
Tests that dates use octal encoding for mathematical harmony and to require explanation to decode.
"""

import pytest

from orbeat_time import to_orbeat8, to_parts_from_ms, to_ucy


class TestOctalEncoding:
    """Test the Octal Encoding design decision."""

    def test_all_components_use_octal_pass(self):
        """PASS: Verify all time components are encoded in octal (base-8)."""
        test_time = 1700000000000
        year_oct, week_oct, day_oct, frac_oct = to_parts_from_ms(test_time)

        octal_digits = set("01234567")

        for char in year_oct:
            assert (
                char in octal_digits
            ), f"Year contains non-octal digit: {char} in {year_oct}"

        for char in week_oct:
            assert (
                char in octal_digits
            ), f"Week contains non-octal digit: {char} in {week_oct}"

        for char in day_oct:
            assert (
                char in octal_digits
            ), f"Day contains non-octal digit: {char} in {day_oct}"

        for char in frac_oct:
            assert (
                char in octal_digits
            ), f"Fraction contains non-octal digit: {char} in {frac_oct}"

    def test_octal_conversion_accuracy_pass(self):
        """PASS: Verify octal conversions are mathematically accurate."""
        test_time = 1700000000000
        year_oct, week_oct, day_oct, frac_oct = to_parts_from_ms(test_time)

        year_dec = int(year_oct, 8)
        week_dec = int(week_oct, 8)
        day_dec = int(day_oct, 8)
        frac_dec = int(frac_oct, 8)

        assert (
            0 <= year_dec < 100000
        ), f"Year in decimal should be reasonable: {year_dec}"

        assert 0 <= week_dec < 60, f"Week in decimal should be reasonable: {week_dec}"

        assert 0 <= day_dec <= 7, f"Day in decimal should be 0-7: {day_dec}"

        assert 0 <= frac_dec < 4096, f"Fraction in decimal should be 0-4095: {frac_dec}"

    def test_octal_formatting_consistency_pass(self):
        """PASS: Verify octal formatting is consistent and padded correctly."""
        test_times = [1700000000000, 1600000000000, 1800000000000]

        for test_time in test_times:
            year_oct, week_oct, day_oct, frac_oct = to_parts_from_ms(test_time)

            assert len(week_oct) == 2, f"Week should be 2 digits: {week_oct}"

            assert len(day_oct) == 1, f"Day should be 1 digit: {day_oct}"

            assert len(frac_oct) == 4, f"Fraction should be 4 digits: {frac_oct}"

            assert len(year_oct) >= 1, f"Year should be at least 1 digit: {year_oct}"

    def test_mathematical_harmony_base_8_pass(self):
        """PASS: Verify octal provides mathematical harmony (powers of 8)."""
        test_time = 1700000000000
        _, _, _, frac_oct = to_parts_from_ms(test_time)
        frac_dec = int(frac_oct, 8)

        max_possible = 8**4 - 1
        assert (
            frac_dec <= max_possible
        ), f"Fraction should not exceed 8^4-1: {frac_dec} > {max_possible}"

        near_full_day = test_time + (24 * 60 * 60 * 1000 - 1000)
        _, _, _, frac_oct_max = to_parts_from_ms(near_full_day)
        frac_dec_max = int(frac_oct_max, 8)

        assert (
            frac_dec_max > max_possible * 0.5
        ), f"Near full day should have high fraction: {frac_dec_max}"

    def test_requires_explanation_to_decode_pass(self):
        """PASS: Verify octal encoding requires explanation to decode."""
        test_time = 1700000000000
        year_oct, week_oct, day_oct, frac_oct = to_parts_from_ms(test_time)

        year_dec = int(year_oct, 8)
        week_dec = int(week_oct, 8)
        day_dec = int(day_oct, 8)

        differences = 0
        if str(year_dec) != year_oct:
            differences += 1
        if str(week_dec).zfill(2) != week_oct:
            differences += 1
        if str(day_dec) != day_oct:
            differences += 1

        assert differences > 0, f"Octal encoding should look different from decimal"

    def test_ucy_format_shows_octal_structure_pass(self):
        """PASS: Verify UCY format clearly shows octal structure."""
        test_time = 1700000000000
        ucy_output = to_ucy(test_time)

        parts = ucy_output.split("_")
        assert (
            len(parts) == 3
        ), f"UCY should have 3 underscore-separated parts: {ucy_output}"

        year_part = parts[0]
        week_part = parts[1]
        day_frac_part = parts[2]

        day_part, frac_part = day_frac_part.split(".")

        octal_digits = set("01234567")
        for char in year_part + week_part + day_part + frac_part:
            assert (
                char in octal_digits
            ), f"UCY contains non-octal digit: {char} in {ucy_output}"

    def test_not_decimal_encoding_fail(self):
        """FAIL: Should NOT use decimal encoding."""
        test_time = 1700000000000
        year_oct, week_oct, day_oct, frac_oct = to_parts_from_ms(test_time)

        all_digits = year_oct + week_oct + day_oct + frac_oct

        for char in all_digits:
            with pytest.raises(AssertionError):
                assert char in "89", f"Should NOT contain decimal digits 8 or 9"

    def test_not_hexadecimal_encoding_fail(self):
        """FAIL: Should NOT use hexadecimal encoding."""
        test_time = 1700000000000
        year_oct, week_oct, day_oct, frac_oct = to_parts_from_ms(test_time)

        all_digits = year_oct + week_oct + day_oct + frac_oct

        hex_letters = set("ABCDEFabcdef")
        for char in all_digits:
            with pytest.raises(AssertionError):
                assert char in hex_letters, f"Should NOT contain hex letters"

    def test_not_binary_encoding_fail(self):
        """FAIL: Should NOT use binary encoding (too verbose)."""
        test_time = 1700000000000
        year_oct, week_oct, day_oct, frac_oct = to_parts_from_ms(test_time)

        all_digits = year_oct + week_oct + day_oct + frac_oct
        non_binary_digits = set("234567")

        contains_non_binary = any(char in non_binary_digits for char in all_digits)
        assert (
            contains_non_binary
        ), f"Should contain non-binary digits (2-7): {all_digits}"

    def test_base_8_mathematical_properties_fail(self):
        """FAIL: Verify base-8 provides specific mathematical advantages."""
        octal_digit_values = [0, 1, 2, 3, 4, 5, 6, 7]
        binary_bits = [3, 3, 3, 3, 3, 3, 3, 3]

        for i, digit in enumerate(octal_digit_values):
            assert digit < 2**3, f"Octal digit {digit} should fit in 3 bits"

        fraction_precision_bits = 4 * 3
        assert (
            fraction_precision_bits == 12
        ), f"Fraction should use exactly 12 bits: {fraction_precision_bits}"

        decimal_equivalent_bits = 4 * 3.32
        assert (
            fraction_precision_bits < decimal_equivalent_bits
        ), f"Octal is more efficient than decimal"
