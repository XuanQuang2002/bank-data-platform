-- Berka source tables (PKDD'99). Safe to re-run: existing objects are skipped.
create schema if not exists berka;

-- Source headers are A1-A16; names come from docs/data-dictionary/berka.md
create table if not exists berka.district (
    district_id               integer primary key,  -- A1
    district_name             text not null,        -- A2
    region                    text not null,        -- A3
    inhabitants               integer,              -- A4
    municipalities_under_500  integer,              -- A5
    municipalities_500_1999   integer,              -- A6
    municipalities_2000_9999  integer,              -- A7
    municipalities_over_10000 integer,              -- A8
    cities                    integer,              -- A9
    urban_ratio               numeric(4, 1),        -- A10
    average_salary            integer,              -- A11
    unemployment_rate_1995    numeric(4, 2),        -- A12 ('?' in source -> null)
    unemployment_rate_1996    numeric(4, 2),        -- A13
    entrepreneurs_per_1000    integer,              -- A14
    crimes_1995               integer,              -- A15 ('?' in source -> null)
    crimes_1996               integer               -- A16
);

create table if not exists berka.account (
    account_id  integer primary key,
    district_id integer not null references berka.district (district_id),
    frequency   text not null,
    date        date not null
);

create table if not exists berka.client (
    client_id    integer primary key,
    birth_number text not null,  -- PII: YYMMDD, month +50 for women
    district_id  integer not null references berka.district (district_id)
);

create table if not exists berka.disp (
    disp_id    integer primary key,
    client_id  integer not null references berka.client (client_id),
    account_id integer not null references berka.account (account_id),
    type       text not null
);

create table if not exists berka.card (
    card_id integer primary key,
    disp_id integer not null references berka.disp (disp_id),
    type    text not null,
    issued  date not null
);

create table if not exists berka.loan (
    loan_id    integer primary key,
    account_id integer not null references berka.account (account_id),
    date       date not null,
    amount     numeric(12, 2) not null,
    duration   integer not null,
    payments   numeric(12, 2) not null,
    status     text not null
);

-- Source file is order.asc; renamed because "order" is a reserved word
create table if not exists berka.permanent_order (
    order_id   integer primary key,
    account_id integer not null references berka.account (account_id),
    bank_to    text not null,
    account_to text not null,
    amount     numeric(12, 2) not null,
    k_symbol   text
);

create table if not exists berka.trans (
    trans_id   integer primary key,
    account_id integer not null references berka.account (account_id),
    date       date not null,
    type       text not null,
    operation  text,
    amount     numeric(12, 2) not null,
    balance    numeric(12, 2) not null,
    k_symbol   text,
    bank       text,
    account    text
);