import streamlit as st
from settings import load_settings
from scripts.clean_script import clean_urls
from scripts.clean_scrape_script import process_scrape_files

def cleaner_tab():
    st.title("URL Cleaner")
    
    # Manual Text Area Cleaner
    main_page_url = st.text_area(
        "Enter text containing URLs:", 
        key="cleaner_main_page_url", 
        height=200, 
        help="Paste raw text here to quickly extract valid links."
    )
    
    if st.button("Clean URLs", key="cleaner_process_button"):
        if not main_page_url.strip():
            st.warning("Please enter some text or URLs first.")
        else:
            cleaned = clean_urls(main_page_url)
            st.text_area("Cleaned URLs", value="\n".join(cleaned), height=300, key="cleaner_cleaned_urls")
            st.success(f"Extracted {len(cleaned)} unique URL(s).")

    st.divider()

    # Batch File Processing Section
    st.subheader("Batch Scrape Cleaner")
    
    filter_keyword = st.text_input(
        "URL Filter Keyword:", 
        value="galleries", 
        help="Only URLs containing this string (e.g., 'galleries') will be kept in export.txt. Leave blank to keep all non-homepage links."
    )
    
    if st.button("Search scrape.txt & Save as export.txt", key="cleaner_search_button"):
        try:
            download_folder = load_settings()
            if not download_folder:
                st.error("Download folder not set. Please set it in the Settings tab.")
                return
            
            files_processed = process_scrape_files(download_folder, filter_keyword=filter_keyword)
            
            if files_processed > 0:
                st.success(f"Processed {files_processed} 'scrape.txt' file(s) and saved filtered URLs to 'export.txt'.")
            else:
                st.info("No 'scrape.txt' files were found in your download folder.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    cleaner_tab()