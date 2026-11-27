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

## Column meanings

Source: https://webpages.charlotte.edu/mirsad/itcs6265/group1/domain.html
(secondary copy; the original PKDD'99 description could not be reached).
Code values were checked against the files in `data/raw/`.

### district

| Column | Meaning                                          |
| ------ | ------------------------------------------------ |
| A1     | District identifier (`district_id`)              |
| A2     | District name                                    |
| A3     | Region                                           |
| A4     | No. of inhabitants                               |
| A5     | No. of municipalities with inhabitants < 499     |
| A6     | No. of municipalities with inhabitants 500-1999  |
| A7     | No. of municipalities with inhabitants 2000-9999 |
| A8     | No. of municipalities with inhabitants > 10000   |
| A9     | No. of cities                                    |
| A10    | Ratio of urban inhabitants                       |
| A11    | Average salary                                   |
| A12    | Unemployment rate in 1995                        |
| A13    | Unemployment rate in 1996                        |
| A14    | No. of entrepreneurs per 1000 inhabitants        |
| A15    | No. of crimes committed in 1995                  |
| A16    | No. of crimes committed in 1996                  |

### Code values

| Table.column      | Value                   | Meaning                                                    |
| ----------------- | ----------------------- | ---------------------------------------------------------- |
| account.frequency | POPLATEK MESICNE        | Monthly statement                                          |
| account.frequency | POPLATEK TYDNE          | Weekly statement                                           |
| account.frequency | POPLATEK PO OBRATU      | Statement after transaction                                |
| disp.type         | OWNER                   | Owner (only the owner can issue orders and ask for a loan) |
| disp.type         | DISPONENT               | User                                                       |
| order.k_symbol    | POJISTNE                | Insurance payment                                          |
| order.k_symbol    | SIPO                    | Household payment                                          |
| order.k_symbol    | LEASING                 | Leasing payment                                            |
| order.k_symbol    | UVER                    | Loan payment                                               |
| trans.type        | PRIJEM                  | Credit                                                     |
| trans.type        | VYDAJ                   | Debit (withdrawal)                                         |
| trans.type        | VYBER                   | Not documented; 16,666 rows, looks like a withdrawal       |
| trans.operation   | VYBER KARTOU            | Credit card withdrawal                                     |
| trans.operation   | VKLAD                   | Credit in cash                                             |
| trans.operation   | PREVOD Z UCTU           | Collection from another bank                               |
| trans.operation   | VYBER                   | Withdrawal in cash                                         |
| trans.operation   | PREVOD NA UCET          | Remittance to another bank                                 |
| trans.k_symbol    | POJISTNE                | Insurance payment                                          |
| trans.k_symbol    | SLUZBY                  | Payment of statement                                       |
| trans.k_symbol    | UROK                    | Interest credited                                          |
| trans.k_symbol    | SANKC. UROK             | Sanction interest if negative balance                      |
| trans.k_symbol    | SIPO                    | Household payment                                          |
| trans.k_symbol    | DUCHOD                  | Old-age pension payment                                    |
| trans.k_symbol    | UVER                    | Loan payment                                               |
| loan.status       | A                       | Contract finished, no problems                             |
| loan.status       | B                       | Contract finished, loan not paid                           |
| loan.status       | C                       | Running contract, OK so far                                |
| loan.status       | D                       | Running contract, client in debt                           |
| card.type         | junior / classic / gold | Card type (lowercase in the data)                          |

### Data quirks

- `trans.operation` is empty for interest rows (`k_symbol` = `UROK`).
- Missing `k_symbol` appears as empty or as a single space, in both `trans` and `order`.
- `order.bank_to` and `trans.bank` are two-letter bank codes.
