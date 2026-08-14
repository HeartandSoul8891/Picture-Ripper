import streamlit as st
import settings  # Import the settings module
import pornpics  # Import the pornpics module

# Main function to run the app
def main():
    # Set the page title
    st.title("ImageFap Downloader")
    
    # Create tabs
    tabs = st.tabs(["imagefap", "pornpics", "downloader", "settings"])
    
    # Fill each tab with content
    with tabs[0]:
        st.title("imagefap")
        st.write("This is the imagefap tab. It will be implemented later.")
    with tabs[1]:
        pornpics.pornpics_tab()  # Call the function from the pornpics module
    with tabs[2]:
        st.title("downloader")
        st.write("This is the downloader tab. It will be implemented later.")
    with tabs[3]:
        settings.settings_tab()  # Call the function from the settings module

# Run the app
if __name__ == "__main__":
    main()