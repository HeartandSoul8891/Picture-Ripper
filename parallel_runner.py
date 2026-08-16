import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
import streamlit as st

from settings import load_settings
from scripts.scraper_script import scrape_first_layer_urls
from scripts.clean_scrape_script import process_scrape_files


# Task 1: Web Scraper Worker
def scrape_worker(main_page_url, folder_name, status_container):
    if not main_page_url or not folder_name:
        status_container.warning("Scraper: Missing URL or Folder Name.")
        return

    status_container.info(f"Scraper: Fetching links from {main_page_url}...")
    download_folder = load_settings()
    if not download_folder:
        status_container.error("Scraper: Download folder not set in Settings.")
        return

    folder_path = os.path.join(download_folder, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    try:
        urls = scrape_first_layer_urls(main_page_url)
        scrape_file_path = os.path.join(folder_path, "scrape.txt")
        with open(scrape_file_path, "w", encoding="utf-8") as f:
            for url in urls:
                f.write(url + "\n")
        status_container.success(f"✔ Scraper: Saved {len(urls)} links to {scrape_file_path}")
    except Exception as e:
        status_container.error(f"✖ Scraper Error: {e}")


# Task 2: Scrape Cleaner Worker
def cleaner_worker(filter_keyword, status_container):
    status_container.info("Cleaner: Scanning for scrape.txt files...")
    download_folder = load_settings()
    if not download_folder:
        status_container.error("Cleaner: Download folder not set in Settings.")
        return

    try:
        files_processed = process_scrape_files(download_folder, filter_keyword=filter_keyword)
        if files_processed > 0:
            status_container.success(f"✔ Cleaner: Processed {files_processed} folder(s) into export.txt.")
        else:
            status_container.info("Cleaner: No scrape.txt files found to clean.")
    except Exception as e:
        status_container.error(f"✖ Cleaner Error: {e}")


# Task 3: Gallery-dl Downloader Worker
def download_worker(log_container):
    default_download_folder = load_settings()
    if not default_download_folder:
        log_container.error("Downloader: Download folder not set in Settings.")
        return

    logs = "=== Downloader Execution Log ===\n"
    log_container.code(logs, language="bash")

    for folder_name in os.listdir(default_download_folder):
        folder_path = os.path.join(default_download_folder, folder_name)
        export_file_path = os.path.join(folder_path, "export.txt")

        if not os.path.isdir(folder_path) or not os.path.exists(export_file_path):
            continue

        logs += f"\n[Downloading] Folder: {folder_name}\n"
        log_container.code(logs, language="bash")

        try:
            process = subprocess.Popen(
                ["gallery-dl", "-d", folder_path, "-i", export_file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            for line in iter(process.stdout.readline, ''):
                logs += line
                log_container.code(logs, language="bash")

            process.stdout.close()
            return_code = process.wait()

            if return_code == 0:
                logs += f"✔ Finished: {folder_name}\n"
                os.remove(export_file_path)
            else:
                logs += f"✖ Failed: {folder_name}\n"
            log_container.code(logs, language="bash")

        except Exception as e:
            logs += f"✖ Downloader Error: {e}\n"
            log_container.code(logs, language="bash")


# Streamlit Tab UI
def tri_runner_tab():
    st.title("Parallel Downloader, Scraper & Cleaner")

    # 3 Column Inputs
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("1. Scraper Inputs")
        url_input = st.text_input("Target URL:", key="tri_url")
        folder_input = st.text_input("Folder Name:", key="tri_folder")

    with col2:
        st.subheader("2. Cleaner Inputs")
        keyword_input = st.text_input("Filter Keyword:", value="galleries", key="tri_keyword")

    with col3:
        st.subheader("3. Downloader")
        st.caption("Scans download folder for ready `export.txt` files.")

    st.divider()

    if st.button("🚀 Run All 3 Tasks Parallel", type="primary"):
        # Output UI columns
        out1, out2, out3 = st.columns(3)
        scraper_ui = out1.empty()
        cleaner_ui = out2.empty()
        downloader_ui = out3.empty()

        # Execute 3 parallel threads
        with ThreadPoolExecutor(max_workers=3) as executor:
            fut_scraper = executor.submit(scrape_worker, url_input, folder_input, scraper_ui)
            fut_cleaner = executor.submit(cleaner_worker, keyword_input, cleaner_ui)
            fut_downloader = executor.submit(download_worker, downloader_ui)

            # Wait for all threads to complete
            fut_scraper.result()
            fut_cleaner.result()
            fut_downloader.result()

        st.success("All 3 parallel operations completed.")

if __name__ == "__main__":
    tri_runner_tab()