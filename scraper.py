from playwright.sync_api import sync_playwright
import json


def scrape_amazon(asin):

    url = f"https://www.amazon.com/dp/{asin}"

    with sync_playwright() as p:

        browser = p.chromium.launch(

            headless=True,

            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage"
            ]

        )

        page = browser.new_page()

        # OPEN PRODUCT PAGE
        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

        page.wait_for_timeout(8000)

        # TITLE
        title = ""

        try:

            title = page.locator(
                "#productTitle"
            ).inner_text().strip()

        except:

            title = "Title Not Found"

        # PRICE
        price = ""

        try:

            price = page.locator(
                ".a-price .a-offscreen"
            ).first.inner_text()

        except:

            price = "Price Not Found"

        # DESCRIPTION
        description = ""

        try:

            bullets = page.locator(
                "#feature-bullets li"
            ).all()

            for item in bullets:

                text = item.inner_text().strip()

                if text:
                    description += text + "\n"

        except:

            description = "Description Not Found"

        # IMAGES
        images = []

        seen_images = set()

        try:

            thumbs = page.locator(
                "#altImages img"
            ).all()

            for img in thumbs:

                src = img.get_attribute("src")

                if src:

                    # CONVERT TO HIGH QUALITY

                    if "._AC_US40_" in src:

                        src = src.replace(
                            "._AC_US40_",
                            "._SL1500_"
                        )

                    if "._SS40_" in src:

                        src = src.replace(
                            "._SS40_",
                            "._SL1500_"
                        )

                    if "SS40" in src:

                        src = src.replace(
                            "SS40",
                            "SL1500"
                        )

                    # REMOVE DUPLICATE IMAGES

                    if src not in seen_images:

                        seen_images.add(src)

                        images.append(src)

        except:

            pass

        browser.close()

        # RETURN PRODUCT DATA
        return {

            "asin": asin,
            "title": title,
            "price": price,
            "description": description,
            "images": images

        }