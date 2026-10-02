// dump the beat table (window.T) + typed strings to timeline.json, so audio.py follows any retiming
import { chromium } from "playwright";
import fs from "fs";
const b = await chromium.launch({ args: ["--allow-file-access-from-files"] }); const p = await b.newPage();
await p.goto("file://" + process.cwd() + "/index.html"); await p.evaluate(() => window.ready);
const tl = await p.evaluate(() => ({ T: window.T, JOB: window.JOB, BODY: window.BODY }));
fs.writeFileSync("timeline.json", JSON.stringify(tl, null, 1)); console.log("timeline.json written"); await b.close();
