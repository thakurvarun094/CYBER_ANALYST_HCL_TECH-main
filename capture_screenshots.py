import os
import asyncio
from playwright.async_api import async_playwright

async def capture():
    os.makedirs('screenshots', exist_ok=True)
    html_path = os.path.abspath('dashboard/index.html')
    file_url = f'file:///{html_path.replace("\\", "/")}'

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1440, 'height': 900}, device_scale_factor=2)
        
        print(f"Navigating to {file_url}...")
        await page.goto(file_url, wait_until='networkidle')
        await asyncio.sleep(1) # Ensure Chart.js animations finish

        # 1. Full page screenshot
        await page.screenshot(path='screenshots/dashboard_full.png', full_page=True)
        print("Saved screenshots/dashboard_full.png")

        # 2. Cropped: charts section
        charts_elem = await page.query_selector('.charts-grid')
        if charts_elem:
            await charts_elem.screenshot(path='screenshots/dashboard_charts.png')
            print("Saved screenshots/dashboard_charts.png")

        # 3. Cropped: table section
        table_elem = await page.query_selector('#table-card')
        if table_elem:
            await table_elem.screenshot(path='screenshots/dashboard_table.png')
            print("Saved screenshots/dashboard_table.png")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(capture())
