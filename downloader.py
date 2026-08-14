import streamlit as st
import os
import subprocess
from settings import load_settings

def downloader_tab():
    st.title("Downloader")
    st.write("Click the button below to download galleries from existing export.txt files in the default folders.")

    if st.button("Download Galleries"):
        download_galleries()

def download_galleries():
    default_download_folder = load_settings()
    if not default_download_folder:
        st.error("Please set the download folder in the Settings tab first.")
        return

    # Container to display the live scrolling log
    log_container = st.empty()
    logs = ""

    for folder_name in os.listdir(default_download_folder):
        folder_path = os.path.join(default_download_folder, folder_name)
        export_file_path = os.path.join(folder_path, "export.txt")

        # Skip if folder_path is a file instead of a directory
        if not os.path.isdir(folder_path):
            continue

        if os.path.exists(export_file_path):
            logs += f"=== Starting download for folder: {folder_name} ===\n"
            log_container.code(logs, language="bash")

            try:
                # Popen starts the process asynchronously and opens a pipe to stdout
                process = subprocess.Popen(
                    ["gallery-dl", "-d", folder_path, "-i", export_file_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,  # Redirect stderr to stdout so all logs are merged
                    text=True,
                    bufsize=1  # Line-buffered
                )

                # Read output line-by-line as gallery-dl prints it
                for line in iter(process.stdout.readline, ''):
                    logs += line
                    # Live update the text container in Streamlit
                    log_container.code(logs, language="bash")

                process.stdout.close()
                return_code = process.wait()

                if return_code == 0:
                    logs += f"✔ Finished downloads for folder: {folder_name}\n"
                    os.remove(export_file_path)
                    logs += f"✔ Removed export.txt from: {folder_name}\n\n"
                else:
                    logs += f"✖ gallery-dl failed on folder: {folder_name} (Exit code {return_code})\n\n"
                
                log_container.code(logs, language="bash")

            except Exception as e:
                logs += f"✖ Exception occurred: {str(e)}\n\n"
                log_container.code(logs, language="bash")
        else:
            logs += f"ℹ No export.txt found in folder: {folder_name}\n\n"
            log_container.code(logs, language="bash")

if __name__ == "__main__":
    downloader_tab()