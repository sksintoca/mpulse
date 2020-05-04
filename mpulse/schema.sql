DROP TABLE IF EXISTS members;

CREATE TABLE  IF NOT EXISTS members (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT  NOT NULL,
  last_name TEXT  NOT NULL,
  phone_number TEXT  NOT NULL UNIQUE,
  client_member_id TEXT NOT NULL UNIQUE,
  account_id INTEGER NOT NULL
);
