import streamlit as st
import settings  # Import the settings module
import cleaner  # Import the pornpics module
import downloader # Import the downloader module
import link_grabber  # Import the link_grabber module

# Main function to run the app
def main():
    # Set the page title
    st.title("Picture Downloader")
    
    # Create tabs in the desired order
    tabs = st.tabs(["Link Grabber", "Cleaner", "Downloader", "Settings"])
    
    # Fill each tab with content in the same order
    with tabs[0]:
        link_grabber.link_grabber_tab()  # link grabber tab for fetching links
    with tabs[1]:
        cleaner.cleaner_tab()  # tab with the cleaner for the urls      
    with tabs[2]:
        downloader.downloader_tab()  # call gallery-dl to download the galleries from the export.txt files in the default folders
    with tabs[3]:
        settings.settings_tab()  # settings tab for the default download folder and future settings

# Run the app
if __name__ == "__main__":
    main()