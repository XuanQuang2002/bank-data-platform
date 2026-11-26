import sys


def test_python_is_3_12() -> None:
    # Guards the version pinned in CI, so local and CI never drift apart
    assert sys.version_info[:2] == (3, 12)
