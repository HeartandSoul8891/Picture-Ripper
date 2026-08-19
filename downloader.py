import os
import subprocess
import threading
import streamlit as st
from settings import load_settings

def run_gallery_dl():
    """Runs in the background thread."""
    default_download_folder = load_settings()
    if not default_download_folder:
        return

    for folder_name in os.listdir(default_download_folder):
        folder_path = os.path.join(default_download_folder, folder_name)
        export_file_path = os.path.join(folder_path, "export.txt")
        scrape_file_path = os.path.join(folder_path, "scrape.txt")

        if os.path.isdir(folder_path) and os.path.exists(export_file_path):
            process = subprocess.Popen(
                ["gallery-dl", "-d", folder_path, "-i", export_file_path]
            )
            process.wait()
            
            if process.returncode == 0:
                # Remove export.txt if it exists
                if os.path.exists(export_file_path):
                    os.remove(export_file_path)
                
                # Remove scrape.txt if it exists
                if os.path.exists(scrape_file_path):
                    os.remove(scrape_file_path)

def downloader_tab():
    st.title("Downloader")
    st.write("Click below to start downloading galleries in the background.")

    if "download_thread" not in st.session_state:
        st.session_state.download_thread = None

    is_running = st.session_state.download_thread and st.session_state.download_thread.is_alive()

    if is_running:
        st.info("⏳ Download process is currently running in the background...")
    else:
        if st.button("Start Downloading"):
            # Launch thread so UI remains interactive
            thread = threading.Thread(target=run_gallery_dl, daemon=True)
            thread.start()
            st.session_state.download_thread = thread
            st.success("🚀 Download started! You can freely switch tabs and continue scraping.")