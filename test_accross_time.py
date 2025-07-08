"""
Tests the Orbeat Time system's robustness and correctness across cosmological,
geological, and historical time scales. This ensures that the core logic is
stable and that formatting holds up under extreme values, from the approximate
age of the universe to the far future.
"""

import pytest
from orbeat_time import to_parts_from_ms, to_ucy, to_orbeat8

# Validated test vectors generated from debug_wide_time_range.py
# Format: (Test Name, Unix MS, Expected Parts Tuple, Expected UCY, Expected Orbeat8)
WIDE_TIME_RANGE_VECTORS = [
    (
        "Age of Universe (~13.8B BCE)",
        -434916000000000000000000,
        ("0310433423112226", "13", "3", "0000"),
        "0310433423112226_13_3.0000",
        "00003316",
    ),
    (
        "Age of Dinosaurs (~66M BCE)",
        -2081520000000000000000,
        ("0753344361424", "43", "7", "7520"),
        "0753344361424_43_7.7520",
        "02577344",
    ),
    (
        "JDN Epoch (4713 BCE)",
        -210866760000000,
        ("011075", "37", "7", "1000"),
        "011075_37_7.1000",
        "00017735",
    ),
    (
        "Bronze Age Start (~3300 BCE)",
        -159999273600000,
        ("05761", "33", "7", "1343"),
        "05761_33_7.1343",
        "34317331",
    ),
    (
        "Great Pyramid (~2560 BCE)",
        -136903651200000,
        ("04425", "26", "5", "5000"),
        "04425_26_5.5000",
        "00055625",
    ),
    (
        "Founding of Rome (~753 BCE)",
        -85908518400000,
        ("01305", "25", "3", "0434"),
        "01305_25_3.0434",
        "43403525",
    ),
    (
        "Pre-Orbeat Epoch (100 BCE)",
        -65281526400000,
        ("067", "04", "5", "3161"),
        "067_04_5.3161",
        "16135407",
    ),
    (
        "Pre-AD (20 BCE)",
        -62807126400000,
        ("26", "27", "4", "2252"),
        "26_27_4.2252",
        "25224726",
    ),
    (
        "Orbeat Epoch Era (44 BCE)",
        -63549936000000,
        ("01", "54", "6", "7525"),
        "01_54_6.7525",
        "52576451",
    ),
    (
        "Early AD Single Digit (5 AD)",
        -61985356800000,
        ("60", "31", "3", "4070"),
        "60_31_3.4070",
        "07043130",
    ),
    (
        "Early AD Double Digit (50 AD)",
        -60563116800000,
        ("135", "34", "0", "5000"),
        "135_34_0.5000",
        "00050435",
    ),
    (
        "Early AD Triple Digit (500 AD)",
        -46403222400000,
        ("1036", "17", "0", "2252"),
        "1036_17_0.2252",
        "25220716",
    ),
    (
        "Medieval (1000 AD)",
        -30578025600000,
        ("2023", "45", "2", "2252"),
        "2023_45_2.2252",
        "25222543",
    ),
    (
        "Renaissance (1500 AD)",
        -14831414400000,
        ("3006", "44", "6", "5707"),
        "3006_44_6.5707",
        "70756446",
    ),
    (
        "Modern Era (2000 AD)",
        946684800000,
        ("3772", "43", "7", "5000"),
        "3772_43_7.5000",
        "00057342",
    ),
    (
        "Distant Future (5000 AD)",
        95616249600000,
        ("11662", "42", "0", "1343"),
        "11662_42_0.1343",
        "34310242",
    ),
    (
        "Far Future (10000 AD)",
        253402300800000,
        ("23472", "44", "3", "5000"),
        "23472_44_3.5000",
        "00053442",
    ),
]

# Create a simplified list of tuples for parametrization, matching pytest's style
TEST_PARAMS = [(v[0], v[1], v[2], v[3], v[4]) for v in WIDE_TIME_RANGE_VECTORS]


@pytest.mark.parametrize(
    "test_name, unix_ms, expected_parts, expected_ucy, expected_orbeat8", TEST_PARAMS
)
def test_core_functions_accross_time(
    test_name, unix_ms, expected_parts, expected_ucy, expected_orbeat8
):
    """
    Tests the three core conversion functions against validated vectors
    from a wide range of time periods.
    """
    # Test the core parts calculation
    actual_parts = to_parts_from_ms(unix_ms)
    assert actual_parts == expected_parts, f"[{test_name}] Parts mismatch"

    # Test the human-readable UCY format
    actual_ucy = to_ucy(unix_ms)
    assert actual_ucy == expected_ucy, f"[{test_name}] UCY mismatch"

    # Test the compact 8-character Orbeat format
    actual_orbeat8 = to_orbeat8(unix_ms)
    assert actual_orbeat8 == expected_orbeat8, f"[{test_name}] Orbeat8 mismatch"
