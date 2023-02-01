const puppeteer = require("puppeteer");

const DOMAIN = process.env.DOMAIN || 'localhost';
const FLAG = process.env.FLAG || 'FLAG{dummy_flag}'

const sleep = async s => new Promise(resolve => setTimeout(resolve, 1000 * s));

const visit = async url => {
	let browser
	try {
		browser = await puppeteer.launch({
			args: ["--disable-gpu", "--no-sandbox", "--js-flags=--noexpose_wasm", "--ignore-certificate-errors"],
			executablePath: "/usr/bin/chromium-browser",
		});
		const context = await browser.createIncognitoBrowserContext();
		const page = await context.newPage();
		
		await page.setCookie({
			name: "FLAG",
			value: FLAG,
			domain: DOMAIN,
			sameSite: "None",
			secure: true
		})

		page.goto(url);
		await page.waitForTimeout(1000);

		await browser.close();

	} catch (e) {
		console.log(e);
	} finally {
		if (browser) await browser.close();
	}
}

module.exports = visit
