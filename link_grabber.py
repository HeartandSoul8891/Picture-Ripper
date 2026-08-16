import streamlit as st
import os
from settings import load_settings
from scripts.scraper_script import scrape_first_layer_urls

def link_grabber_tab():
    st.title("Link Grabber")
    
    # Text box for the primary link with a unique key
    main_page_url = st.text_input("Enter the primary link:", key="link_grabber_main_page_url")
    
    # Text box for the folder name with a unique key
    folder_name = st.text_input("Enter the folder name:", key="link_grabber_folder_name")
    
    # Process button
    if st.button("Process", key="link_grabber_process_button"):
        try:
            # Load the download folder from settings
            download_folder = load_settings()
            if not download_folder:
                st.error("Download folder not set. Please set the download folder in the Settings tab.")
                return
            
            # Create the folder if it doesn't exist
            folder_path = os.path.join(download_folder, folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            
            # Scrape the first layer URLs
            urls = scrape_first_layer_urls(main_page_url)
            
            # Save the scraped URLs to a file
            scrape_file_path = os.path.join(folder_path, "scrape.txt")
            with open(scrape_file_path, "w") as f:
                for url in urls:
                    f.write(url + "\n")
            
            # Display success message
            st.success(f"Scraped URLs saved to {scrape_file_path}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# If this script is run directly, call the link_grabber_tab function
if __name__ == "__main__":
    link_grabber_tab()