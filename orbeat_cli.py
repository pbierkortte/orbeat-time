from datetime import datetime, timezone
from orbeat_time import encode_orbeat_time
import json, argparse, sys
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO

def get_orbeat_time():
    now = datetime.now(timezone.utc)
    orbeat = encode_orbeat_time(int(now.timestamp() * 1000))
    iso = now.isoformat()
    return orbeat, iso

def parse_args(args=None):
    parser = argparse.ArgumentParser(prog='orbeat', description='Convert current time to Orbeat format')
    parser.add_argument('--output', metavar='FORMAT', choices=['json', 'orbeat'],
                      help='Output format: json or orbeat (default: orbeat)')
    return parser.parse_args(args)

def format_output(orbeat, iso, output_format):
    if output_format == 'json':
        return json.dumps({"orbeat": orbeat, "iso": iso}, indent=2)
    return orbeat

def run_cli(*cli_args, is_test=False):
    if is_test:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                args = parse_args(cli_args)
                orbeat, iso = get_orbeat_time()
                print(format_output(orbeat, iso, args.output))
            except SystemExit:
                pass
        return stdout.getvalue().strip(), stderr.getvalue().strip()
    else:
        args = parse_args()
        orbeat, iso = get_orbeat_time()
        print(format_output(orbeat, iso, args.output))

if __name__ == '__main__':
    run_cli()
