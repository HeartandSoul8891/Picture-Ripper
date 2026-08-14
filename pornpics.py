import streamlit as st
import re
from io import StringIO
import os

# Function to create the pornpics tab
def pornpics_tab():
    st.title("PornPics")
    st.write("Paste the URLs and descriptions of galleries here:")
    pasted_text = st.text_area("Paste URLs and descriptions", key="pasted_text", height=200)
    
    # Input field for the model name or folder name
    model_or_folder_name = st.text_input("Model Name or Folder Name", key="model_or_folder_name")
    
    # Create folder button
    if st.button("Create Folder First"):
        if model_or_folder_name:
            default_download_folder = st.session_state.get("download_folder", "")
            if default_download_folder:
                folder_path = os.path.join(default_download_folder, model_or_folder_name)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    st.success(f"Folder '{model_or_folder_name}' created at '{folder_path}'.")
                else:
                    st.warning(f"Folder '{model_or_folder_name}' already exists.")
            else:
                st.error("Please set the download folder in the Settings tab first.")
        else:
            st.error("Please enter a model name or folder name.")
    
    # Export button
    if st.button("Export"):
        if pasted_text:
            # Extract URLs from the pasted text
            urls = extract_urls(pasted_text)
            if urls:
                # Create a file-like object
                file_like = StringIO()
                for url in urls:
                    file_like.write(url + "\n")
                
                # Get the file content
                file_content = file_like.getvalue()
                
                # Determine the filename based on the model or folder name
                filename = f"{model_or_folder_name}_urls.txt"
                
                # Create a download button
                st.download_button(
                    label="Download File",
                    data=file_content,
                    file_name=filename,
                    mime="text/plain"
                )
            else:
                st.error("No URLs found in the pasted text.")
        else:
            st.error("Please paste some URLs and descriptions.")

# Function to extract URLs from the pasted text
def extract_urls(text):
    # Regular expression to find URLs
    url_pattern = re.compile(r'https?://[^\s]+')
    return url_pattern.findall(text)