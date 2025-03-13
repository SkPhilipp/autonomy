const puppeteer = require('puppeteer');

async function takeScreenshot(url, outputPath) {
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    try {
        const page = await browser.newPage();
        await page.goto(url, { waitUntil: 'networkidle0' });
        await page.screenshot({ path: outputPath, fullPage: true });
        console.log(`Screenshot saved to ${outputPath}`);
    } catch (error) {
        console.error('Error taking screenshot:', error.message);
        process.exit(1);
    } finally {
        await browser.close();
    }
}

// Get URL and output path from command line arguments
const url = process.argv[2];
const outputPath = process.argv[3];

if (!url || !outputPath) {
    console.error('Usage: node screenshot.js <url> <output-path>');
    process.exit(1);
}

takeScreenshot(url, outputPath); 