import re
from datetime import datetime, timezone
import sys, os

# Add the project root to the Python path to allow imports from orbeat_time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from orbeat_time import to_ucy, to_eastern


def update_file(filepath, replacement_string):
    """Finds a placeholder in a file and replaces it."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        placeholder_pattern = re.compile(
            r"<!-- LAST_UPDATED_START -->.*<!-- LAST_UPDATED_END -->"
        )

        new_content = placeholder_pattern.sub(
            f"<!-- LAST_UPDATED_START -->{replacement_string}<!-- LAST_UPDATED_END -->",
            content,
        )

        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            return True
    except FileNotFoundError:
        print(f"Warning: {filepath} not found. Skipping.")
    return False


if __name__ == "__main__":
    now = datetime.now(timezone.utc)
    now_ms = int(now.timestamp() * 1000)
    ucy_time = to_ucy(now_ms)
    eastern_time = to_eastern(now_ms)

    update_string_readme = f"**Last Updated:** `{ucy_time}` UCY | {eastern_time}"
    update_string_html = f"Last Updated: {ucy_time} UCY | {eastern_time}"

    readme_changed = update_file("README.md", update_string_readme)
    html_changed = update_file("index.html", update_string_html)

    if readme_changed or html_changed:
        print(update_string_readme)
