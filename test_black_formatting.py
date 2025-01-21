from black.cli import main


def test_black_formatting():
    """Test that all Python files are formatted according to black standards."""
    black.main(["--check", "--line-length=120", "."])
