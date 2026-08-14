import streamlit as st
import settings  # Import the settings module
import cleaner  # Import the pornpics module
import downloader # Import the downloader module

# Main function to run the app
def main():
    # Set the page title
    st.title("Picture Downloader")
    
    # Create tabs
    tabs = st.tabs(["Cleaner", "Downloader", "settings"])
    
    # Fill each tab with content
    with tabs[0]:
        cleaner.cleaner_tab()  # tab with the cleaner for the urls      
    with tabs[1]:
        downloader.downloader_tab()  # call gallery-dl to download the galleries from the export.txt files in the default folders
    with tabs[2]:
        settings.settings_tab()  # setings tab for the default download folder and future settings

# Run the app
if __name__ == "__main__":
    main()