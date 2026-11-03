-- Who signed up to test Bentotachi, and what testers sent back.
-- No emails and no IP addresses: only what people typed in.
CREATE TABLE signups (
  id INTEGER PRIMARY KEY,
  created TEXT NOT NULL, -- when, in UTC (ISO 8601)
  name TEXT NOT NULL, -- their name on Discord
  server TEXT NOT NULL, -- the Discord server to find them in
  note TEXT NOT NULL DEFAULT ''
);

CREATE TABLE feedback (
  id INTEGER PRIMARY KEY,
  created TEXT NOT NULL,
  name TEXT NOT NULL DEFAULT '', -- optional: who sent it
  kind TEXT NOT NULL, -- broke, idea or thought
  message TEXT NOT NULL
);
