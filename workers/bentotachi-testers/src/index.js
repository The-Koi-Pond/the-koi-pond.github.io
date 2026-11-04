// Bentotachi's tester signups and feedback.
//
// The pages are plain HTML forms on the website (thekoipond.dev/bentotachi/
// join/ and /testers/, on GitHub Pages), which can't store anything. They
// send their forms here. This saves what was typed in D1 (Cloudflare's
// SQLite database) and sends the browser back to the website. Only Xel can
// read the lists, at /bentotachi/admin, with the password saved as the
// ADMIN_PASSWORD secret (README.md).

// The longest text each box takes: the same as the forms' maxlength.
const MAX = { name: 60, server: 80, note: 500, message: 4000 };

const KINDS = { broke: "Something broke", idea: "An idea", thought: "Just a thought" };

// Even a flood that gets past the rate limit can't fill the database.
const MAX_ROWS = { signups: 1000, feedback: 5000 };

// For every page this Worker shows: never cached or indexed, and no scripts
// or outside files at all, so text someone typed can never run as code.
const HEADERS = {
  "Content-Type": "text/html; charset=utf-8",
  "Cache-Control": "no-store",
  "X-Robots-Tag": "noindex",
  "Content-Security-Policy":
    "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'",
  // Not "no-referrer": under that, browsers send "Origin: null" even on the
  // admin page's own Remove forms, so remove() would refuse every click.
  // "same-origin" still tells other sites nothing.
  "Referrer-Policy": "same-origin",
  "X-Content-Type-Options": "nosniff",
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const post = request.method === "POST";
    switch (url.pathname) {
      case "/bentotachi/join":
        return post ? join(request, env) : back(env, "/bentotachi/join/");
      case "/bentotachi/feedback":
        return post ? feedback(request, env) : back(env, "/bentotachi/testers/");
      case "/bentotachi/admin":
        return admin(request, env, url);
      case "/":
        return back(env, "/");
      default:
        return new Response("Nothing here.", { status: 404, headers: HEADERS });
    }
  },
};

// Send the browser back to a page on the website. "See other" (303) makes
// it load that page normally, instead of sending the form again.
function back(env, page) {
  return Response.redirect(new URL(page, env.SITE).href, 303);
}

async function join(request, env) {
  try {
    const form = await request.formData();
    // Bots fill in every box, even the hidden one people never see.
    // Pretend it worked (the same answer as a real signup), so they don't
    // learn to skip it.
    if (form.get("website")) return back(env, "/bentotachi/testers/#welcome");
    if (!(await allowed(env.LIMITER, request, "join"))) return back(env, "/bentotachi/join/#oops");

    const name = clean(form.get("name"), MAX.name);
    const server = clean(form.get("server"), MAX.server);
    const note = clean(form.get("note"), MAX.note, true);
    if (!name || !server || note === null || form.get("android") !== "yes") {
      return back(env, "/bentotachi/join/#oops");
    }
    if (await full(env, "signups")) return back(env, "/bentotachi/join/#oops");

    await env.DB.prepare("INSERT INTO signups (created, name, server, note) VALUES (?, ?, ?, ?)")
      .bind(new Date().toISOString(), name, server, note)
      .run();
    return back(env, "/bentotachi/testers/#welcome");
  } catch (error) {
    console.error(error);
    return back(env, "/bentotachi/join/#oops");
  }
}

async function feedback(request, env) {
  try {
    const form = await request.formData();
    if (form.get("website")) return back(env, "/bentotachi/testers/#thanks");
    if (!(await allowed(env.LIMITER, request, "feedback"))) return back(env, "/bentotachi/testers/#oops");

    const name = clean(form.get("name"), MAX.name);
    const kind = form.get("kind");
    const message = clean(form.get("message"), MAX.message, true);
    if (name === null || !message || typeof kind !== "string" || !Object.hasOwn(KINDS, kind)) {
      return back(env, "/bentotachi/testers/#oops");
    }
    if (await full(env, "feedback")) return back(env, "/bentotachi/testers/#oops");

    await env.DB.prepare("INSERT INTO feedback (created, name, kind, message) VALUES (?, ?, ?, ?)")
      .bind(new Date().toISOString(), name, kind, message)
      .run();
    return back(env, "/bentotachi/testers/#thanks");
  } catch (error) {
    console.error(error);
    return back(env, "/bentotachi/testers/#oops");
  }
}

// The invisible writing-direction marks and overrides (U+061C, U+200E,
// U+200F, U+202A to U+202E, U+2066 to U+2069), by their code numbers.
const DIRECTION_MARKS = new RegExp(
  "[" + [[0x61c], [0x200e, 0x200f], [0x202a, 0x202e], [0x2066, 0x2069]]
    .map(([from, to = from]) => String.fromCharCode(from) + "-" + String.fromCharCode(to))
    .join("") + "]",
  "g",
);

// Text from a form box, tidied: trimmed, control characters dropped (or
// made spaces), and line breaks kept only where the box takes several
// lines. Returns null for anything the form itself can't send (too long,
// or a file), which means it didn't come from the form.
function clean(value, max, lines = false) {
  if (value === null) return "";
  if (typeof value !== "string") return null;
  let text = value.replace(/\r\n?/g, "\n").replace(/\t/g, " ");
  text = text.replace(lines ? /[\u0000-\u0009\u000b-\u001f\u007f]/g : /[\u0000-\u001f\u007f]/g, lines ? "" : " ");
  // Writing-direction overrides can make a name show backwards in the
  // admin list. Other invisible characters stay: emoji need them.
  text = text.replace(DIRECTION_MARKS, "");
  text = text.trim();
  return text.length > max ? null : text;
}

// Cloudflare counts requests per visitor address for us (wrangler.toml);
// nothing about the visitor is saved.
async function allowed(limiter, request, what) {
  const address = request.headers.get("cf-connecting-ip") ?? "unknown";
  const { success } = await limiter.limit({ key: `${what}:${address}` });
  return success;
}

async function full(env, table) {
  const row = await env.DB.prepare(`SELECT COUNT(*) AS n FROM ${table}`).first();
  return row.n >= MAX_ROWS[table];
}

// ---------------------------------------------------------------------------
// Xel's private page: who signed up, and the feedback.

async function admin(request, env, url) {
  if (!env.ADMIN_PASSWORD) {
    return page("Not set up yet", "<p>The admin password isn't set yet: see README.md next to this Worker.</p>", 503);
  }
  const given = request.headers.get("Authorization");
  // Every load with a password counts toward its own rate limit, so the
  // password can't be guessed by trying lots of them quickly.
  if (given && !(await allowed(env.ADMIN_LIMITER, request, "admin"))) {
    return page("Slow down", "<p>Too many tries. Wait a minute, then reload.</p>", 429);
  }
  if (!given || !(await rightPassword(given, env.ADMIN_PASSWORD))) {
    return new Response("Password needed.", {
      status: 401,
      headers: { ...HEADERS, "WWW-Authenticate": 'Basic realm="Bentotachi testers", charset="UTF-8"' },
    });
  }
  if (request.method === "POST") return remove(request, env, url);
  if (request.method !== "GET") return new Response("Not allowed.", { status: 405, headers: HEADERS });

  const [signups, notes] = await Promise.all([
    env.DB.prepare("SELECT * FROM signups ORDER BY id DESC").all(),
    env.DB.prepare("SELECT * FROM feedback ORDER BY id DESC").all(),
  ]);
  const zone = request.cf?.timezone ?? "UTC"; // the viewer's time zone, from Cloudflare
  return page("Bentotachi testers", adminBody(signups.results, notes.results, zone));
}

// The browser sends the password as "Basic " + base64 of "anything:password".
// Both sides are hashed first so the comparison takes the same time however
// much of the password is right.
async function rightPassword(header, password) {
  const [scheme, encoded] = header.split(" ");
  if (scheme !== "Basic" || !encoded) return false;
  let decoded;
  try {
    decoded = new TextDecoder().decode(Uint8Array.from(atob(encoded), (c) => c.charCodeAt(0)));
  } catch {
    return false;
  }
  const given = decoded.slice(decoded.indexOf(":") + 1);
  const hash = (s) => crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  const [a, b] = await Promise.all([hash(given), hash(password)]);
  return crypto.subtle.timingSafeEqual(a, b);
}

// A Remove button. Browsers say which site a form came from (Origin), so
// another website can't make Xel's signed-in browser remove things.
async function remove(request, env, url) {
  if (request.headers.get("Origin") !== url.origin) {
    return page("Refused", "<p>That didn't come from this page.</p>", 403);
  }
  const form = await request.formData();
  const name = form.get("table");
  // hasOwn, not just MAX_ROWS[name]: "constructor" and such are on every object.
  const table = typeof name === "string" && Object.hasOwn(MAX_ROWS, name) ? name : null;
  const id = Number(form.get("id"));
  if (!table || !Number.isInteger(id)) return page("Hmm", "<p>Nothing to remove.</p>", 400);
  await env.DB.prepare(`DELETE FROM ${table} WHERE id = ?`).bind(id).run();
  return Response.redirect(`${url.origin}/bentotachi/admin`, 303);
}

function adminBody(signups, notes, zone) {
  const when = (iso) =>
    new Date(iso).toLocaleString("en-GB", { timeZone: zone, dateStyle: "medium", timeStyle: "short" });
  const removeButton = (table, id) =>
    `<details class="remove"><summary>Remove</summary><form method="post">` +
    `<input type="hidden" name="table" value="${table}"><input type="hidden" name="id" value="${id}">` +
    `<button>Yes, remove it</button></form></details>`;

  const rows = signups
    .map(
      (s) =>
        `<tr><td>${esc(when(s.created))}</td><td>${esc(s.name)}</td><td>${esc(s.server)}</td>` +
        `<td class="text">${esc(s.note)}</td><td>${removeButton("signups", s.id)}</td></tr>`,
    )
    .join("");
  const cards = notes
    .map(
      (f) =>
        `<li><p class="meta"><strong>${esc(KINDS[f.kind] ?? f.kind)}</strong> · ${esc(when(f.created))} · ` +
        `${f.name ? esc(f.name) : "<em>no name</em>"}</p><p class="text">${esc(f.message)}</p>` +
        `${removeButton("feedback", f.id)}</li>`,
    )
    .join("");

  return `<h1>Bentotachi testers</h1>
<p class="count">${signups.length} signed up · ${notes.length} feedback</p>
<h2>Signed up</h2>
${
  signups.length
    ? `<div class="scroll"><table><thead><tr><th>When</th><th>Name on Discord</th><th>Server</th><th>Note</th><th></th></tr></thead><tbody>${rows}</tbody></table></div>`
    : "<p>Nobody yet.</p>"
}
<h2>Feedback</h2>
${notes.length ? `<ul class="feedback">${cards}</ul>` : "<p>None yet.</p>"}`;
}

// Makes typed text safe to put in a page: shown as text, never as HTML.
function esc(value) {
  return String(value ?? "").replace(
    /[&<>"']/g,
    (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c],
  );
}

// The admin page's look: Bentotachi's colours, light and dark.
function page(title, body, status = 200) {
  const html = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title>
<style>
:root { --bg: #f3f6f4; --surface: #fff; --text: #2b2420; --muted: #5f6b67; --border: #d8dddb; --accent: #a82d4a; --soft: #e2efeb; color-scheme: light; }
@media (prefers-color-scheme: dark) { :root { --bg: #141b1b; --surface: #202928; --text: #f1ebe5; --muted: #a9b3ae; --border: #34403e; --accent: #ee7d92; --soft: #1d3330; color-scheme: dark; } }
body { margin: 0; background: var(--bg); color: var(--text); font: 16px/1.5 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
main { max-width: 960px; margin: 0 auto; padding: 24px 16px 48px; }
h1 { margin: 0; color: var(--accent); }
h2 { margin-top: 32px; }
.count { color: var(--muted); margin: 4px 0 0; }
.scroll { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; background: var(--surface); }
th, td { text-align: left; vertical-align: top; padding: 8px 10px; border-bottom: 1px solid var(--border); }
th { color: var(--muted); font-weight: 600; white-space: nowrap; }
td:first-child { white-space: nowrap; color: var(--muted); }
.text { white-space: pre-wrap; overflow-wrap: anywhere; }
.feedback { list-style: none; padding: 0; margin: 0; display: grid; gap: 12px; }
.feedback li { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 12px 14px; }
.feedback p { margin: 0; }
.meta { color: var(--muted); margin-bottom: 6px !important; }
.meta strong { color: var(--accent); }
.remove summary { color: var(--muted); cursor: pointer; font-size: 0.9rem; }
.remove button { margin-top: 6px; font: inherit; padding: 4px 12px; border-radius: 999px; border: 1px solid var(--accent); background: var(--soft); color: var(--text); cursor: pointer; }
</style></head>
<body><main>${body}</main></body></html>`;
  return new Response(html, { status, headers: HEADERS });
}
