import os
import re

# Matches standard web URLs (http/https) inside any surrounding text
URL_REGEX = r'https?://[^\s<>"{}|\\^`\[\]]+'

def clean_urls(raw_text: str) -> list[str]:
    """Extracts valid URLs from text, strips trailing punctuation, and removes duplicates."""
    if not raw_text:
        return []
    
    extracted_urls = re.findall(URL_REGEX, raw_text)
    
    # Strip common trailing punctuation accidentally matched by regex
    cleaned_urls = [re.sub(r'[.,;)]+$', '', url) for url in extracted_urls]
    
    # Return unique URLs while keeping original order
    return list(dict.fromkeys(cleaned_urls))

def find_and_clean_files(base_directory: str) -> int:
    """
    Recursively searches base_directory for 'export.txt' or 'scrape.txt' files,
    strips non-URL text, and overwrites/saves them as clean 'export.txt' files.
    """
    processed_count = 0
    
    for root, _, files in os.walk(base_directory):
        for file_name in files:
            if file_name in ("export.txt", "scrape.txt"):
                file_path = os.path.join(root, file_name)
                
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                
                cleaned = clean_urls(content)
                export_path = os.path.join(root, "export.txt")
                
                with open(export_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(cleaned) + ("\n" if cleaned else ""))
                    
                processed_count += 1
                
    return processed_count