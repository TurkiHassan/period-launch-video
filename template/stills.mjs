import { chromium } from "playwright";
import fs from "fs";
const times = process.argv.slice(2).map(Number);
const browser = await chromium.launch({ args: ["--allow-file-access-from-files"] });
const page = await browser.newPage({ viewport: { width: 760, height: 760 } });
const errs = []; page.on("console", m => { if (m.type() === "error") errs.push(m.text()); }); page.on("pageerror", e => errs.push(String(e)));
await page.goto("file://" + process.cwd() + "/index.html");
await page.evaluate(() => window.ready);
fs.mkdirSync("out/stills", { recursive: true });
for (const t of times) {
  const url = await page.evaluate(t => { frame(t, 4); return document.getElementById("c").toDataURL("image/png"); }, t);
  fs.writeFileSync(`out/stills/t${t.toFixed(2)}.png`, Buffer.from(url.split(",")[1], "base64"));
}
if (errs.length) console.log("ERRORS:\n" + errs.join("\n"));
await browser.close();
