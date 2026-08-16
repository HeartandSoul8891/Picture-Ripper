import os
from urllib.parse import urlparse

# File extensions to ignore only if they aren't part of a gallery path
IGNORE_EXTENSIONS = ('.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.webp')

def is_valid_url(url: str, filter_keyword: str = "galleri") -> bool:
    """
    Validates URLs containing the filter keyword (e.g., 'galleries' or 'gallery').
    Handles relative paths and keeps valid gallery endpoints.
    """
    url_lower = url.lower()

    # Matches both 'gallery' and 'galleries' using stem 'galleri'
    if filter_keyword and filter_keyword.lower() not in url_lower:
        return False

    # Check scheme for full URLs; allow relative paths starting with '/'
    if url.startswith(('http://', 'https://')):
        try:
            parsed = urlparse(url)
            if not parsed.netloc:
                return False
        except Exception:
            return False

    # Only drop static assets if 'gallery'/'galleries' isn't explicitly in the endpoint path
    parsed_path = urlparse(url if url.startswith('http') else f"https://dummy.com{url}").path
    if parsed_path.lower().endswith(IGNORE_EXTENSIONS) and not any(k in url_lower for k in ('/galleries/', '/gallery/')):
        return False

    return True

def clean_and_format_url(url: str) -> str:
    """Normalizes whitespace and strips fragment anchors (#top)."""
    return url.split('#')[0].strip()

def process_scrape_files(base_directory: str, filter_keyword: str = "galleri") -> int:
    """
    Processes scrape.txt files with console feedback showing total lines,
    filter matches, and unique exported URLs.
    """
    processed_count = 0

    for root, _, files in os.walk(base_directory):
        if "scrape.txt" in files:
            scrape_path = os.path.join(root, "scrape.txt")

            with open(scrape_path, "r", encoding="utf-8", errors="ignore") as f:
                raw_lines = [line.strip() for line in f if line.strip()]

            matched_urls = []
            for raw_url in raw_lines:
                if is_valid_url(raw_url, filter_keyword=filter_keyword):
                    matched_urls.append(clean_and_format_url(raw_url))

            unique_urls = sorted(set(matched_urls))

            # Diagnostic breakdown printed to console
            print(f"[{scrape_path}]")
            print(f"  ├── Total lines in scrape.txt: {len(raw_lines)}")
            print(f"  ├── Lines matching gallery keyword: {len(matched_urls)}")
            print(f"  └── Unique URLs written to export.txt: {len(unique_urls)}")

            export_path = os.path.join(root, "export.txt")
            with open(export_path, "w", encoding="utf-8") as f:
                for url in unique_urls:
                    f.write(url + "\n")

            processed_count += 1

    return processed_count