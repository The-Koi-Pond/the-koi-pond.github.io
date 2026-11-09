-- How the Play closed test is going, for the testers' page: how many
-- testers Play Console says have opted in (Xel types it in on the admin
-- page: Play offers no way to fetch it), and the day Google's 14 days
-- started (empty until 12 are in). Always exactly one row.
CREATE TABLE test_status (
  id INTEGER PRIMARY KEY CHECK (id = 1),
  opted_in INTEGER NOT NULL DEFAULT 0,
  started TEXT -- YYYY-MM-DD, or NULL before the 14 days start
);

INSERT INTO test_status (id, opted_in) VALUES (1, 0);
