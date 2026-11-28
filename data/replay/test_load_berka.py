from datetime import date

import pytest
from load_berka import clean_value, parse_date


def test_parse_date_yymmdd() -> None:
    assert parse_date("930101") == date(1993, 1, 1)


def test_parse_date_with_time_part() -> None:
    # card.issued looks like "931107 00:00:00"
    assert parse_date("931107 00:00:00") == date(1993, 11, 7)


def test_parse_date_rejects_invalid_date() -> None:
    with pytest.raises(ValueError):
        parse_date("931332")


@pytest.mark.parametrize("raw", ["", " ", "?"])
def test_clean_value_missing_markers_become_none(raw: str) -> None:
    assert clean_value(raw) is None


def test_clean_value_keeps_real_values() -> None:
    assert clean_value("POPLATEK MESICNE") == "POPLATEK MESICNE"
    # trans.account contains "0"; it is a real value, not missing
    assert clean_value("0") == "0"
