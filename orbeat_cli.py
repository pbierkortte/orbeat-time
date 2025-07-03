import json
import argparse
from datetime import datetime, timezone
from orbeat_time import to_orbeat8


def get_orbeat_time():
    now = datetime.now(timezone.utc)
    unix_ms = int(now.timestamp() * 1000)
    orbeat = to_orbeat8(unix_ms)
    iso = now.isoformat()
    return orbeat, iso


def parse_args(args=None):
    parser = argparse.ArgumentParser(
        prog="orbeat", description="Convert current time to Orbeat format"
    )
    parser.add_argument(
        "--output",
        metavar="FORMAT",
        choices=["json", "orbeat"],
        default="orbeat",
        help="Output format: json or orbeat (default: orbeat)",
    )
    return parser.parse_args(args)


def format_output(orbeat, iso, output_format):
    if output_format == "json":
        return json.dumps({"orbeat": orbeat, "iso": iso}, indent=2)
    return orbeat


if __name__ == "__main__":
    args = parse_args()
    orbeat, iso = get_orbeat_time()
    print(format_output(orbeat, iso, args.output))
