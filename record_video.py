import os
import asyncio
import numpy as np
from playwright.async_api import async_playwright

async def record():
    # Will record directly using playwright or frames
    os.makedirs('video', exist_ok=True)
    html_path = os.path.abspath('dashboard/index.html')
    file_url = f'file:///{html_path.replace("\\", "/")}'

    async with async_playwright() as p:
        # Launch browser with recording enabled
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport={'width': 1440, 'height': 900},
            device_scale_factor=1,
            record_video_dir="video/",
            record_video_size={"width": 1440, "height": 900}
        )
        page = await context.new_page()

        print(f"Loading {file_url} for video walkthrough...")
        await page.goto(file_url, wait_until='networkidle')
        await asyncio.sleep(2) # Show header and KPIs

        # Hover over KPI cards one by one
        kpi_cards = await page.query_selector_all('.kpi-card')
        for card in kpi_cards:
            await card.hover()
            await asyncio.sleep(0.6)

        await asyncio.sleep(1)

        # Smooth scroll down to charts
        for y in range(0, 320, 20):
            await page.evaluate(f"window.scrollTo(0, {y})")
            await asyncio.sleep(0.04)

        await asyncio.sleep(1)

        # Hover over chart elements
        status_chart = await page.query_selector('#chart-status-card')
        if status_chart:
            await status_chart.hover()
            await asyncio.sleep(1.2)

        risk_chart = await page.query_selector('#chart-risk-card')
        if risk_chart:
            await risk_chart.hover()
            await asyncio.sleep(1.2)

        # Smooth scroll to Key Insight and Table
        for y in range(320, 750, 20):
            await page.evaluate(f"window.scrollTo(0, {y})")
            await asyncio.sleep(0.04)

        await asyncio.sleep(1)

        # Hover rows in table
        rows = await page.query_selector_all('#audit-table-body tr')
        for row in rows:
            await row.hover()
            await asyncio.sleep(0.7)

        await asyncio.sleep(1.5)

        # Smooth scroll back to top
        for y in range(750, -20, -30):
            await page.evaluate(f"window.scrollTo(0, {max(0, y)})")
            await asyncio.sleep(0.03)

        await asyncio.sleep(2)

        # Close page and context to finish video encoding
        await page.close()
        video_path = await page.video.path()
        print(f"Temporary video saved at: {video_path}")
        await context.close()
        await browser.close()

        # Rename to clean target name
        target_video = os.path.abspath('video/project_walkthrough.webm')
        if os.path.exists(target_video):
            os.remove(target_video)
        os.rename(video_path, target_video)
        print(f"Walkthrough video successfully saved to: {target_video}")

if __name__ == '__main__':
    asyncio.run(record())
