from datetime import datetime, timezone
from orbeat_time import decode_orbeat_time, MILLISECONDS_PER_DAY, DAWN_OFFSET_MS

# Original edge cases from test_orbeat_time.py
# Each tuple is (original_reference_dt_str, target_orbeat_code)
ORIGINAL_EDGE_CASES_DATA = [
    ("1970-01-06T00:02:38.203+00:00", "70000000"),
    ("1970-01-06T00:19:51.796+00:00", "07000000"),
    ("1970-01-06T02:37:40.546+00:00", "00700000"),
    ("1970-01-06T21:00:10.546+00:00", "00070000"),
    ("1970-01-05T00:00:10.546+00:00", "00007000"), # This was for a time before 10:00 UTC
    ("1970-02-15T00:00:10.546+00:00", "00000700"),
    ("1970-11-22T00:00:10.546+00:00", "00000070"),
    ("1977-01-01T00:00:10.546+00:00", "00000007"),
]

print("Finding new timestamps for original Orbeat codes with 10-hour (UTC) offset:")
print(f"DAWN_OFFSET_MS = {DAWN_OFFSET_MS} ({DAWN_OFFSET_MS / (60*60*1000)} hours)")
print("-" * 70)
print(f"{'Orbeat Code':<12} | {'Original Ref DT':<30} | {'New Decoded Timestamp (ms)':<28} | {'New Decoded ISO DT':<30}")
print("-" * 70)

for original_dt_str, orbeat_code in ORIGINAL_EDGE_CASES_DATA:
    original_dt = datetime.fromisoformat(original_dt_str)
    # Use the original datetime as a reference point for decoding.
    # Add a small buffer (e.g., half a day) to ensure the reference is after the target,
    # as decode_orbeat_time finds the *most recent* occurrence *before* the reference.
    # Given the 10-hour shift, the actual time might be up to 10 hours earlier or 14 hours later
    # than the original timestamp to produce the same Orbeat day fraction.
    # A slightly later reference point is safer.
    reference_unix_ms = (original_dt.timestamp() * 1000) + (MILLISECONDS_PER_DAY / 2)

    try:
        decoded_ms = decode_orbeat_time(orbeat_code, reference_unix_ms)
        decoded_dt = datetime.fromtimestamp(decoded_ms / 1000, tz=timezone.utc)
        print(f"{orbeat_code:<12} | {original_dt_str:<30} | {decoded_ms:<28.3f} | {decoded_dt.isoformat():<30}")
    except ValueError as e:
        print(f"{orbeat_code:<12} | {original_dt_str:<30} | ERROR: {e}")

print("-" * 70)
print("\nNote: The 'New Decoded ISO DT' is the UTC timestamp that, when encoded with the 10-hour offset,")
print("should produce the given 'Orbeat Code'. This is the start of the Orbeat 'beat' interval.")
print("The original reference datetime was used to guide the search for this new timestamp.")
