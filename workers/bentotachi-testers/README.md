# Bentotachi testers (Cloudflare Worker)

Saves what people send from Bentotachi's tester pages, which are plain HTML
on GitHub Pages and can't store anything themselves:

- `thekoipond.dev/bentotachi/join/`: the signup form (name on Discord,
  which server, an optional note, "I've got an Android phone"). No emails.
- `thekoipond.dev/bentotachi/testers/`: what happens next, and the feedback
  form. Not secret: anyone with the address can open it, but it's kept out
  of search results and only linked from the signup.

Both forms post to this Worker at `https://api.thekoipond.dev`. It saves
them in a D1 database (Cloudflare's SQLite), then sends the browser back to
the website (`#welcome`, `#thanks`, or `#oops` when something was wrong).

**Reading the lists:** https://api.thekoipond.dev/bentotachi/admin, with the
admin password (any username). Each entry has a Remove button, for anyone
who asks to be deleted.

**How the test is going:** the testers' page shows how many testers are in
and counts down Google's 14 days, from `/bentotachi/status` (counts and a
date only, readable by the website). Play Console's opted-in number can't
be fetched, so Xel copies it into the box at the top of the admin page. The
start date fills itself in the day it reaches 12 and clears below 12; a date
typed in wins, to match Play Console.

Spam protection: a hidden box only bots fill in (they're told it worked,
and nothing is saved), at most 5 signups and 5 feedback forms a minute from
one address, and a cap on the total (1000 signups, 5000 feedback, 1500
screenshots). The admin page allows 100 loads a minute from one address
(each screenshot shown on it counts as one). Someone with many
addresses gets more tries, so the password must be long (20+ characters:
a few random words plus numbers is fine), used nowhere else, and not built
from facts about Xel.

Launch order: deploy the Worker first, then push the pages, then share the
link. Pages that go live first can't send their forms anywhere.

## Commands

From this folder. Wrangler is Cloudflare's tool; `npx` fetches it.

```
npx wrangler@4 login                                   # once per PC: opens the browser
npx wrangler@4 d1 create bentotachi-testers            # once: put the database_id in wrangler.toml
npx wrangler@4 d1 migrations apply DB --remote         # create the tables (and any new migrations/)
npx wrangler@4 secret put ADMIN_PASSWORD               # set or change the admin password (long, and used nowhere else)
npx wrangler@4 deploy                                  # publish src/index.js
```

To read the lists without the page:
`npx wrangler@4 d1 execute DB --remote --command "SELECT * FROM signups"`.

## Testing

`test.mjs` checks the Worker end to end against a local copy with its own
empty database (nothing touches the real one):

```
npx wrangler@4 d1 migrations apply DB --local --persist-to <empty folder>
npx wrangler@4 dev --persist-to <same folder> --var SITE:http://localhost:8000 --var ADMIN_PASSWORD:test-password
node test.mjs
```

It needs a fresh folder each run (it counts entries and uses up the rate
limits).
