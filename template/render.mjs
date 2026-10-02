// render frames [a, b) at 60fps with 4 motion-blur subframes → out/frames/f#####.png
import { chromium } from "playwright";
import fs from "fs";
const [a, b] = process.argv.slice(2).map(Number);
const browser = await chromium.launch({ args: ["--allow-file-access-from-files", "--enable-gpu-rasterization", "--ignore-gpu-blocklist"] });
const page = await browser.newPage({ viewport: { width: 760, height: 760 } });
const errs = []; page.on("pageerror", e => errs.push(String(e))); page.on("console", m => m.type() === "error" && errs.push(m.text()));
await page.goto("file://" + process.cwd() + "/index.html");
await page.evaluate(() => window.ready);
fs.mkdirSync("out/frames", { recursive: true });
const t0 = Date.now();
for (let f = a; f < b; f++) {
  const url = await page.evaluate(f => { frame(f / 60, 4); return document.getElementById("c").toDataURL("image/png"); }, f);
  fs.writeFileSync(`out/frames/f${String(f).padStart(5, "0")}.png`, Buffer.from(url.slice(22), "base64"));
}
console.log(`frames ${a}-${b} done in ${((Date.now() - t0) / 1000).toFixed(1)}s`, errs.length ? errs : "");
await browser.close();
