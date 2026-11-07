-- Screenshots sent with feedback (added 2026-11-07): up to 3 per message,
-- shrunk by the testers' page before sending, kept beside the feedback in
-- the database (no separate file storage needed). Removing the feedback
-- removes them (the Worker deletes them too, in case foreign keys are off).
CREATE TABLE feedback_files (
  id INTEGER PRIMARY KEY,
  feedback_id INTEGER NOT NULL REFERENCES feedback(id) ON DELETE CASCADE,
  type TEXT NOT NULL, -- image/png, image/jpeg, image/webp or image/gif, from the file's first bytes
  data BLOB NOT NULL
);

CREATE INDEX feedback_files_by_feedback ON feedback_files (feedback_id);
