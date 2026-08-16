import time
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright

def scrape_first_layer_urls(main_page_url, allow_external=True, max_scrolls=15, scroll_delay=1.5):
    """
    Launches a browser, scrolls down to load dynamic/lazy-loaded content,
    and extracts all links from the fully rendered page.
    """
    first_layer_urls = set()
    parsed_main = urlparse(main_page_url)
    base_domain = f"{parsed_main.scheme}://{parsed_main.netloc}"

    with sync_playwright() as p:
        # Launch headless Chromium browser with a realistic user-agent
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()

        print(f"Navigating to {main_page_url}...")
        page.goto(main_page_url, wait_until="domcontentloaded", timeout=30000)

        # Infinite Scroll Loop
        last_height = page.evaluate("document.body.scrollHeight")
        for i in range(max_scrolls):
            # Scroll to bottom of page
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(scroll_delay)  # Wait for AJAX/JS to fetch and render new elements

            new_height = page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                print("Reached end of scroll or no new content loaded.")
                break
            
            last_height = new_height
            print(f"Scrolled {i + 1}/{max_scrolls} times...")

        # Extract all rendered href links
        raw_hrefs = page.eval_on_selector_all('a[href]', 'elements => elements.map(e => e.getAttribute("href"))')
        browser.close()

    # Filter and format extracted links
    for href in raw_hrefs:
        if not href or href.startswith(('javascript:', '#', 'mailto:')):
            continue

        abs_url = urljoin(main_page_url, href)

        if allow_external:
            if abs_url.startswith(('http://', 'https://')):
                first_layer_urls.add(abs_url)
        else:
            if abs_url.startswith(base_domain):
                first_layer_urls.add(abs_url)

    return list(first_layer_urls)