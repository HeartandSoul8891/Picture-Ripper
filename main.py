import streamlit as st
import settings
import cleaner
import downloader
import link_grabber

def main():
    st.set_page_config(page_title="Picture Downloader", layout="wide")
    st.title("Picture Downloader")
    
    tabs = st.tabs([
        "Link Grabber", 
        "Cleaner", 
        "Downloader", 
        "Settings"
    ])
    
    with tabs[0]:
        link_grabber.link_grabber_tab()
    with tabs[1]:
        cleaner.cleaner_tab()
    with tabs[2]:
        downloader.downloader_tab()
    with tabs[3]:
        settings.settings_tab()

if __name__ == "__main__":
    main()