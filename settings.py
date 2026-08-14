import os
import xml.etree.ElementTree as ET
import streamlit as st

SETTINGS_FILE = "settings.xml"

def load_settings() -> str:
    """
    Safely loads the download folder path from the XML file.
    Returns an empty string if the file doesn't exist, is corrupted, or empty.
    """
    if os.path.exists(SETTINGS_FILE):
        try:
            tree = ET.parse(SETTINGS_FILE)
            root = tree.getroot()
            folder_node = root.find("download_folder")
            
            # Ensure the node exists and contains text (handles empty tags safely)
            if folder_node is not None and folder_node.text:
                return folder_node.text
        except ET.ParseError:
            # Fallback gracefully if XML file is malformed
            pass
            
    return ""

def save_settings(download_folder: str) -> None:
    """
    Writes the download folder setting into the XML configuration file.
    """
    root = ET.Element("settings")
    download_folder_element = ET.SubElement(root, "download_folder")
    download_folder_element.text = download_folder
    
    tree = ET.ElementTree(root)
    tree.write(SETTINGS_FILE)

def settings_tab():
    st.title("Settings")
    st.write("Specify the main download folder.")
    
    # Initialize session_state ONLY ONCE when the app loads.
    # Prevents reading settings.xml on every single render/click.
    if "download_folder" not in st.session_state:
        st.session_state.download_folder = load_settings()
    
    # Input widget prepopulated with the persistent session state
    input_val = st.text_input(
        "Download Folder", 
        value=st.session_state.download_folder, 
        key="input_folder"
    )
    
    # Update both runtime memory and disk storage on user submission
    if st.button("Save Settings"):
        st.session_state.download_folder = input_val
        save_settings(input_val)
        st.success("Download folder saved successfully!")