// Checks the Worker end to end against a local copy (README.md, "Testing"):
//   node test.mjs [http://127.0.0.1:8787]
// It needs a fresh local database: the counts and rate limits assume one.
import assert from "node:assert/strict";

const API = process.argv[2] ?? "http://127.0.0.1:8787";
const SITE = "http://localhost:8000";
const PASSWORD = "test-password";
const auth = (pw) => ({ Authorization: "Basic " + Buffer.from("xel:" + pw).toString("base64") });

async function send(path, fields, headers = {}) {
  const res = await fetch(API + path, { method: "POST", body: new URLSearchParams(fields), headers, redirect: "manual" });
  return { status: res.status, to: res.headers.get("location"), text: await res.text() };
}

async function adminPage(pw = PASSWORD) {
  const res = await fetch(API + "/bentotachi/admin", { headers: pw ? auth(pw) : {}, redirect: "manual" });
  return { status: res.status, text: await res.text(), headers: res.headers };
}

const tests = [];
const test = (name, fn) => tests.push([name, fn]);
const good = { name: "Sam", server: "Pond friends", note: "", android: "yes" };

test("a signup is saved and goes on to the testers' page", async () => {
  const r = await send("/bentotachi/join", good);
  assert.equal(r.status, 303);
  assert.equal(r.to, `${SITE}/bentotachi/testers/#welcome`);
});

test("without the Android tick it's refused", async () => {
  const r = await send("/bentotachi/join", { ...good, android: "" });
  assert.equal(r.to, `${SITE}/bentotachi/join/#oops`);
});

test("too long for the form is refused", async () => {
  const r = await send("/bentotachi/join", { ...good, name: "x".repeat(61) });
  assert.equal(r.to, `${SITE}/bentotachi/join/#oops`);
});

// Typed into every box of both forms, to check none of it reaches the
// admin page as real HTML.
const EVIL = '<img src=x onerror="alert(1)">';
const EVIL_SHOWN = "&lt;img src=x onerror=&quot;alert(1)&quot;&gt;";

test("HTML in every signup box is accepted as text", async () => {
  const r = await send("/bentotachi/join", { ...good, name: EVIL, server: EVIL, note: `line one\r\nline two ${EVIL}` });
  assert.equal(r.to, `${SITE}/bentotachi/testers/#welcome`);
});

test("a writing-direction override is taken out of a name", async () => {
  const r = await send("/bentotachi/join", { ...good, name: "abc" + String.fromCharCode(0x202e) + "def" });
  assert.equal(r.to, `${SITE}/bentotachi/testers/#welcome`);
});

test("a bot that fills the hidden box gets the same answer as a person, and nothing is saved", async () => {
  const r = await send("/bentotachi/join", { ...good, name: "Bot", website: "http://spam.example" });
  assert.equal(r.to, `${SITE}/bentotachi/testers/#welcome`);
});

test("feedback is saved and comes back with #thanks", async () => {
  const r = await send("/bentotachi/feedback", { kind: "broke", message: "The timer\nscreamed", name: "" });
  assert.equal(r.to, `${SITE}/bentotachi/testers/#thanks`);
});

test("HTML in both feedback boxes is accepted as text", async () => {
  const r = await send("/bentotachi/feedback", { kind: "idea", message: EVIL, name: EVIL });
  assert.equal(r.to, `${SITE}/bentotachi/testers/#thanks`);
});

test("feedback with a made-up kind is refused", async () => {
  const r = await send("/bentotachi/feedback", { kind: "toString", message: "hi" });
  assert.equal(r.to, `${SITE}/bentotachi/testers/#oops`);
});

test("empty feedback is refused", async () => {
  const r = await send("/bentotachi/feedback", { kind: "idea", message: "   " });
  assert.equal(r.to, `${SITE}/bentotachi/testers/#oops`);
});

test("the admin page asks for a password", async () => {
  const r = await adminPage(null);
  assert.equal(r.status, 401);
  assert.match(r.headers.get("www-authenticate"), /^Basic /);
  assert.ok(!r.text.includes("Sam"));
});

test("a wrong password doesn't get in", async () => {
  const r = await adminPage("nope");
  assert.equal(r.status, 401);
  assert.ok(!r.text.includes("Sam"));
});

test("the right password shows the lists, with typed HTML made harmless", async () => {
  const r = await adminPage();
  assert.equal(r.status, 200);
  assert.match(r.text, /3 signed up · 2 feedback/);
  assert.ok(r.text.includes("<td>Sam</td>"));
  assert.ok(r.text.includes("Pond friends"));
  assert.ok(r.text.includes("<td>abcdef</td>"));
  // All five boxes that got HTML show it as text, and none as real HTML.
  assert.equal(r.text.split(EVIL_SHOWN).length - 1, 5);
  assert.ok(!r.text.includes("<img"));
  assert.ok(!r.text.includes("Bot"));
  assert.ok(r.text.includes("line one\nline two"));
  assert.ok(r.text.includes("Something broke"));
  assert.equal(r.headers.get("cache-control"), "no-store");
  // Exactly this: no scripts at all, even if escaping ever slips; images
  // only from here (the screenshots).
  assert.equal(
    r.headers.get("content-security-policy"),
    "default-src 'none'; style-src 'unsafe-inline'; img-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'",
  );
  // "no-referrer" would make browsers send "Origin: null" on the Remove
  // forms, and every Remove would be refused. These tests set Origin by
  // hand, so they can't see that: this header check guards it.
  assert.equal(r.headers.get("referrer-policy"), "same-origin");
});

test("Remove without the password is refused", async () => {
  const r = await send("/bentotachi/admin", { table: "signups", id: "1" }, { Origin: API });
  assert.equal(r.status, 401);
  assert.match((await adminPage()).text, /3 signed up/);
});

test("Remove from another website is refused", async () => {
  const r = await send("/bentotachi/admin", { table: "signups", id: "1" }, { ...auth(PASSWORD), Origin: "https://evil.example" });
  assert.equal(r.status, 403);
  assert.match((await adminPage()).text, /3 signed up/);
});

test("Remove from the admin page removes it", async () => {
  const r = await send("/bentotachi/admin", { table: "signups", id: "1" }, { ...auth(PASSWORD), Origin: API });
  assert.equal(r.status, 303);
  const page = (await adminPage()).text;
  assert.match(page, /2 signed up/);
  assert.ok(!page.includes("<td>Sam</td>"));
});

test("Remove can't reach other tables, or names every object has", async () => {
  for (const table of ["sqlite_master", "constructor", "__proto__", "toString"]) {
    const r = await send("/bentotachi/admin", { table, id: "1" }, { ...auth(PASSWORD), Origin: API });
    assert.equal(r.status, 400, table);
  }
});

// Screenshots with feedback, from another address (the feedback limit for
// this one is used up by now). The page shrinks them before sending; here
// they're sent as they are.
const PNG = Buffer.from("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==", "base64");
async function sendWithFiles(fields, files, address) {
  const form = new FormData();
  for (const [key, value] of Object.entries(fields)) form.append(key, value);
  for (const [name, bytes, type] of files) form.append("screenshot", new Blob([bytes], { type }), name);
  const res = await fetch(API + "/bentotachi/feedback", { method: "POST", body: form, headers: { "cf-connecting-ip": address }, redirect: "manual" });
  return { status: res.status, to: res.headers.get("location") };
}

test("feedback with a screenshot keeps both, and the admin page shows it behind the password", async () => {
  const r = await sendWithFiles({ kind: "broke", message: "Look at this" }, [["shot.png", PNG, "image/png"]], "10.9.0.1");
  assert.equal(r.to, `${SITE}/bentotachi/testers/#thanks`);
  const page = (await adminPage()).text;
  const id = page.match(/\/bentotachi\/admin\/screenshot\?id=(\d+)/)?.[1];
  assert.ok(id, "a screenshot link on the admin page");
  const shot = await fetch(`${API}/bentotachi/admin/screenshot?id=${id}`, { headers: auth(PASSWORD) });
  assert.equal(shot.status, 200);
  assert.equal(shot.headers.get("content-type"), "image/png");
  assert.equal(shot.headers.get("x-content-type-options"), "nosniff");
  assert.deepEqual(Buffer.from(await shot.arrayBuffer()), PNG);
  const locked = await fetch(`${API}/bentotachi/admin/screenshot?id=${id}`, { redirect: "manual" });
  assert.equal(locked.status, 401);
});

test("a file that isn't a picture, or too big, is left out, the message kept, and the page says so", async () => {
  const fake = await sendWithFiles({ kind: "idea", message: "Not a picture" }, [["evil.png", Buffer.from("<svg onload=alert(1)>"), "image/png"]], "10.9.0.2");
  assert.equal(fake.to, `${SITE}/bentotachi/testers/#thanks-no-screenshot`);
  const big = Buffer.concat([PNG, Buffer.alloc(1_600_000)]);
  const large = await sendWithFiles({ kind: "idea", message: "Too big" }, [["big.png", big, "image/png"]], "10.9.0.3");
  assert.equal(large.to, `${SITE}/bentotachi/testers/#thanks-no-screenshot`);
  const page = (await adminPage()).text;
  assert.ok(page.includes("Not a picture") && page.includes("Too big"));
});

test("only 3 screenshots a message are kept", async () => {
  const four = [1, 2, 3, 4].map((n) => [`s${n}.png`, PNG, "image/png"]);
  const r = await sendWithFiles({ kind: "thought", message: "Four shots" }, four, "10.9.0.4");
  assert.equal(r.to, `${SITE}/bentotachi/testers/#thanks-no-screenshot`);
  const page = (await adminPage()).text;
  const card = page.slice(page.indexOf("Four shots"));
  assert.equal(card.slice(0, card.indexOf("</li>")).split("<img").length - 1, 3);
});

test("removing feedback removes its screenshots", async () => {
  const page = (await adminPage()).text;
  const card = page.slice(0, page.indexOf("Look at this"));
  const shotId = page.slice(page.indexOf("Look at this")).match(/screenshot\?id=(\d+)/)[1];
  const feedbackId = page.slice(page.indexOf("Look at this")).match(/name="table" value="feedback"><input type="hidden" name="id" value="(\d+)"/)[1];
  assert.ok(card.length > 0);
  const r = await send("/bentotachi/admin", { table: "feedback", id: feedbackId }, { ...auth(PASSWORD), Origin: API });
  assert.equal(r.status, 303);
  const gone = await fetch(`${API}/bentotachi/admin/screenshot?id=${shotId}`, { headers: auth(PASSWORD) });
  assert.equal(gone.status, 404);
});

test("wrong passwords stop being checked after 100 tries a minute", async () => {
  const statuses = [];
  for (let i = 0; i < 101; i++) statuses.push((await adminPage("nope")).status);
  assert.ok(statuses.includes(429), statuses.join(" "));
});

// Last, because it uses up this address's signups for the next minute.
test("too many signups in a minute are turned away", async () => {
  const results = [];
  for (let i = 0; i < 4; i++) results.push((await send("/bentotachi/join", { ...good, name: `Flood ${i}` })).to);
  assert.ok(results.includes(`${SITE}/bentotachi/join/#oops`), results.join("\n"));
});

let failed = 0;
for (const [name, fn] of tests) {
  try {
    await fn();
    console.log("ok  ", name);
  } catch (error) {
    failed++;
    console.log("FAIL", name, "\n     ", error.message.split("\n").join("\n      "));
  }
}
console.log(failed ? `${failed} failed` : "all passed");
process.exit(failed ? 1 : 0);
