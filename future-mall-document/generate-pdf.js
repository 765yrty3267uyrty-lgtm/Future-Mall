const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

async function generatePDF() {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();

  // Set viewport for A4 at 96 DPI (794 x 1123 px) or use print media
  await page.setViewport({
    width: 794,
    height: 1123,
    deviceScaleFactor: 2
  });

  const filePath = path.resolve(__dirname, 'index.html');
  const fileUrl = `file://${filePath}`;

  console.log('Loading document...');
  await page.goto(fileUrl, { waitUntil: 'networkidle0' });

  // Wait for fonts to load
  await page.evaluateHandle(() => document.fonts.ready);

  console.log('Generating PDF...');
  await page.pdf({
    path: path.resolve(__dirname, 'FUTURE-MALL-Specification.pdf'),
    format: 'A4',
    printBackground: true,
    margin: {
      top: '0',
      right: '0',
      bottom: '0',
      left: '0'
    },
    preferCSSPageSize: true,
    scale: 1.0
  });

  console.log('PDF generated: FUTURE-MALL-Specification.pdf');
  await browser.close();
}

generatePDF().catch(console.error);