import streamlit as st
import re
import os

# Callback function to clear the text inputs before the page re-renders
def reset_fields():
    st.session_state.pasted_text = ""
    st.session_state.model_or_folder_name = ""

def cleaner_tab():
    st.title("Cleaner")
    st.write("Paste the URLs and descriptions of galleries here:")

    # Initialize state variables if they don't exist yet
    if "pasted_text" not in st.session_state:
        st.session_state.pasted_text = ""
    if "model_or_folder_name" not in st.session_state:
        st.session_state.model_or_folder_name = ""

    # Input fields linked directly to session_state keys
    pasted_text = st.text_area(
        "Paste URLs and descriptions", 
        key="pasted_text", 
        height=200
    )
    
    model_or_folder_name = st.text_input(
        "Model Name or Folder Name", 
        key="model_or_folder_name"
    )

    # 3-column layout
    col1, col2, col3 = st.columns(3)

    # 1. CREATE FOLDER
    with col1:
        if st.button("Create Folder First", use_container_width=True):
            if model_or_folder_name:
                default_download_folder = st.session_state.get("download_folder", "")
                if default_download_folder:
                    folder_path = os.path.join(default_download_folder, model_or_folder_name)
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)
                        st.success(f"Folder '{model_or_folder_name}' created!")
                    else:
                        st.warning(f"Folder '{model_or_folder_name}' already exists.")
                else:
                    st.error("Please set the download folder in the Settings tab first.")
            else:
                st.error("Please enter a model name or folder name.")

    # 2. EXPORT (Moved to 2nd position)
    with col2:
        if st.button("Export", use_container_width=True):
            if pasted_text:
                urls = extract_urls(pasted_text)
                if urls:
                    filename = "export.txt"
                    file_content = "\n".join(urls)
                    default_download_folder = st.session_state.get("download_folder", "")
                    
                    if default_download_folder:
                        folder_path = os.path.join(default_download_folder, model_or_folder_name)
                        # Ensure folder exists before writing
                        os.makedirs(folder_path, exist_ok=True)
                        
                        file_path = os.path.join(folder_path, filename)
                        with open(file_path, "w", encoding="utf-8") as file:
                            file.write(file_content)

                        st.success(f"Exported {len(urls)} URLs to '{file_path}'.")
                    else:
                        st.error("Please set the download folder in the Settings tab first.")
                else:
                    st.error("No URLs found in the pasted text.")
            else:
                st.error("Please paste some URLs and descriptions.")

    # 3. CLEAN / RESET (Moved to 3rd position, using callback)
    with col3:
        st.button("Clean", on_click=reset_fields, use_container_width=True)


def extract_urls(text):
    """Extracts all http/https links from raw input text."""
    url_pattern = re.compile(r'https?://[^\s]+')
    return url_pattern.findall(text)


if __name__ == "__main__":
    cleaner_tab()