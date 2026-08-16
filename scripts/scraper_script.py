import time
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright

def scrape_first_layer_urls(main_page_url, allow_external=True, max_scrolls=300, max_retries=3, idle_timeout=1.5):
    """
    Dynamically scrolls galleries until no new content loads (handling 60 to 2000+ items),
    using retries and network-idle checks before stopping.
    """
    first_layer_urls = set()
    parsed_main = urlparse(main_page_url)
    base_domain = f"{parsed_main.scheme}://{parsed_main.netloc}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()

        print(f"Navigating to {main_page_url}...")
        page.goto(main_page_url, wait_until="domcontentloaded", timeout=30000)

        last_height = page.evaluate("document.body.scrollHeight")
        retries = 0
        scroll_count = 0

        while scroll_count < max_scrolls:
            # Scroll down to bottom
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            scroll_count += 1

            # Wait for active network requests to finish
            try:
                page.wait_for_load_state("networkidle", timeout=3000)
            except Exception:
                time.sleep(idle_timeout)

            new_height = page.evaluate("document.body.scrollHeight")

            # Check if page height stopped expanding
            if new_height == last_height:
                retries += 1
                print(f"No new content yet (retry {retries}/{max_retries})...")
                time.sleep(1.5)
                
                if retries >= max_retries:
                    print("Reached true end of gallery.")
                    break
            else:
                retries = 0
                last_height = new_height
                print(f"Scroll {scroll_count}: Page expanded (Height: {new_height}px)")

        # Extract all rendered links
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

    print(f"Successfully scraped {len(first_layer_urls)} unique URLs.")
    return list(first_layer_urls)

# Alias so both function names work across all scripts
scrape_gallery_urls = scrape_first_layer_urls