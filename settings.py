import streamlit as st

def settings_tab():
    st.title("Settings")
    st.write("Specify the main download folder.")
    
    # Initialize default state
    if "download_folder" not in st.session_state:
        st.session_state.download_folder = ""

    # Use a different key for the widget (e.g., "input_folder")
    input_val = st.text_input(
        "Download Folder", 
        value=st.session_state.download_folder, 
        key="input_folder"
    )
    
    if st.button("Save Settings"):
        st.session_state.download_folder = input_val
        st.success("Download folder saved successfully!")