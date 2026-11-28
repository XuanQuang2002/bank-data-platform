from datetime import date

import pytest
from load_berka import clean_value, convert_row, mask_birth_number, mask_row, parse_date


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


def test_convert_row_parses_dates_and_missing_values() -> None:
    header = [
        "trans_id",
        "account_id",
        "date",
        "type",
        "operation",
        "amount",
        "balance",
        "k_symbol",
        "bank",
        "account",
    ]
    row = [
        "695247",
        "2378",
        "930101",
        "PRIJEM",
        "VKLAD",
        "700.00",
        "700.00",
        "",
        "",
        "",
    ]
    assert convert_row(header, row) == [
        "695247",
        "2378",
        date(1993, 1, 1),
        "PRIJEM",
        "VKLAD",
        "700.00",
        "700.00",
        None,
        None,
        None,
    ]


def test_mask_birth_number_hides_all_digits() -> None:
    assert mask_birth_number("706213") == "******"


def test_mask_row_masks_only_birth_number() -> None:
    header = ["client_id", "birth_number", "district_id"]
    assert mask_row(header, ["1", "706213", "18"]) == ["1", "******", "18"]
