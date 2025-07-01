from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from playwright.async_api import async_playwright

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/oglasi")
async def oglasi():
    oglasi = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(
            "https://www.willhaben.at/iad/gebrauchtwagen/auto/gebrauchtwagenboerse?sfId=ab61a23e-c7a1-4309-9d42-2076cbb7507f&isNavigation=true&DEALER=1&PRICE_FROM=0&PRICE_TO=15000&YEAR_MODEL_FROM=1990&YEAR_MODEL_TO=2025"
        )
        await page.wait_for_timeout(5000)

        ads = await page.query_selector_all("div[class*='AdWrapper']")
        for ad in ads:
            naslov = await ad.query_selector("h3")
            cijena = await ad.query_selector("strong[itemprop='price']")
            link_el = await ad.query_selector("a")
            opis = await ad.query_selector("div[class*='DescriptionContainer']")

            oglasi.append({
                "naslov": await naslov.inner_text() if naslov else None,
                "cijena": await cijena.inner_text() if cijena else None,
                "link": f"https://www.willhaben.at{await link_el.get_attribute('href')}" if link_el else None,
                "opis": await opis.inner_text() if opis else "",
                "kontaktInfo": None
            })

        await browser.close()

    return oglasi
