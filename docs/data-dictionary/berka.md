# Berka dataset (PKDD'99 Financial)

Anonymized data from a Czech bank, released for the PKDD'99 Discovery Challenge.
Used as the core banking source (clients, accounts, transactions, loans, cards).

## Source

- Original site (offline): http://lisp.vse.cz/pkdd99/
- Web Archive copy of the original zip:
  https://web.archive.org/web/20070214120527/http://lisp.vse.cz:80/pkdd99/DATA/data_berka.zip
- Alternative (modified version, MariaDB): https://relational.fel.cvut.cz/dataset/Financial

## How to get it

1. Download `data_berka.zip` from the Web Archive link above.
2. Unzip it into `data/raw/` (git-ignored, never committed).

## Files

| File         | Data rows (excl. header) |
| ------------ | ------------------------ |
| account.asc  | 4,500                    |
| card.asc     | 892                      |
| client.asc   | 5,369                    |
| disp.asc     | 5,369                    |
| district.asc | 77                       |
| loan.asc     | 682                      |
| order.asc    | 6,471                    |
| trans.asc    | 1,056,320                |

## Format notes

- Separator `;`, text values in double quotes, CRLF line endings.
- Dates are `YYMMDD` numbers, e.g. `930101` = 1993-01-01.
- `client.birth_number` is `YYMMDD`, with +50 added to the month for women. It is PII: mask it in logs and samples.
- Some values are Czech codes, e.g. `PRIJEM` = credit, `VKLAD` = deposit.
- Missing values appear as `""` or as nothing between separators.
- `district.asc` has placeholder headers `A1`-`A16`; their meanings are in the original challenge description.
