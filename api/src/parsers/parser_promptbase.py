import re

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, expect


CLEANR = re.compile("<.*?>")

cookies = {
    "_ga_5X3KHQGQBX": "GS1.1.1745312462.2.1.1745314358.0.0.0",
    "_ga": "GA1.1.1770056567.1745305856",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ru,ru-MD;q=0.8,en-US;q=0.5,en;q=0.3",
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    "Referer": "https://promptbase.com/art-and-illustrations",
    "Sec-GPC": "1",
    "Alt-Used": "promptbase.com",
    "Connection": "keep-alive",
    # 'Cookie': '_ga_5X3KHQGQBX=GS1.1.1745312462.2.1.1745314358.0.0.0; _ga=GA1.1.1770056567.1745305856',
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "If-None-Match": "W/1a916-+a82UPHvYpZ9BP6ij76Ib02Ihho",
    "Priority": "u=0, i",
}


def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, " ", raw_html)
    return cleantext


async def scroll_page(page, count: int):
    """Прокручивает страницу"""
    for _ in range(count):
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
        await page.wait_for_timeout(5000)


async def get_categories():
    url = f"https://promptbase.com/"
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome", args=["--start-maximized"])
        context = await browser.new_context(
            extra_http_headers=headers, no_viewport=True
        )
        page = await context.new_page()
        await page.goto(url)
        await page.wait_for_timeout(1000)
        buttons = await page.get_by_text("Categories").all()
        button = buttons[0]
        await button.click()
        await page.wait_for_timeout(1000)
        categories = await page.locator("li.second-nav-item").all()

        categories = [await category.inner_text() for category in categories]
        await context.close()
        return categories


async def get_promt_by_category(category: str, count: int) -> list:

    categories = {
        "Art": "art,illustration,cartoon,drawing,sketch,style",
        "Logos": "logos,icons",
        "Graphics": "graphics,patterns,wallpaper,avatars",
        "Productivity": "coach,finance,ideas,health,study,travel,email,writing",
        "Marketing": "marketing,business,finance,ads,copy,seo,social",
        "Photo": "photograph",
        "Games": "3d,games",
    }
    url = f"https://promptbase.com/marketplace?sortBy=hotness&domain=image&tags={categories[category]}"
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome")
        context = await browser.new_context(extra_http_headers=headers)
        page = await context.new_page()
        await page.goto(url)
        count_page = count // 20
        await scroll_page(page=page, count=count_page)
        flag = page.locator("a.tile-title").last
        await expect(flag).to_be_visible(timeout=50000)
        locator = await page.locator("div.item-tile").all()
        promts = []
        for i in locator[:count]:
            promt = {}
            l = await i.inner_html()
            soup = BeautifulSoup(l, "html.parser")
            if soup.find("a", {"class": "tile-title"}):
                promt["title"] = soup.find("a", {"class": "tile-title"}).text
            if soup.find("img"):
                promt["img_link"] = soup.find("img").get("src")
            if soup.find("a", {"class": "tile-title"}):
                promt["link"] = soup.find("a").get("href")
            if soup.find("span", {"class": "rating-text"}):
                promt["rating"] = soup.find("span", {"class": "rating-text"}).text
            if soup.find("div", {"class": "item-price"}):
                promt["price"] = soup.find("div", {"class": "item-price"}).text

            if not promt.get("rating") and promt.get("link"):
                page = await context.new_page()
                await page.goto("https://promptbase.com" + promt["link"])
                await page.wait_for_timeout(5000)
                if await page.query_selector("div.rating-wrapper"):
                    rating = page.locator("div.rating-wrapper").first
                    await expect(rating).to_be_visible()
                    promt["rating"] = await rating.text_content()
                else:
                    promt["rating"] = 0
                await page.close()
            if promt:
                promts.append(promt)
        await browser.close()
        return promts
