import json
import os
import streamlit as st

CONFIG_FILE = "config.json"


def load_config():
    """Loads configuration from file or falls back to defaults."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    # Default fallback path
    return {"download_folder": os.path.expanduser("~/Downloads")}


def save_config(config):
    """Saves configuration dictionary to file."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def init_session():
    """Initializes session state from config if not already present."""
    if "config" not in st.session_state:
        st.session_state.config = load_config()


def settings_tab():
    st.header("Settings")

    current_folder = st.session_state.config.get("download_folder", "")
    download_folder = st.text_input(
        "Download Folder Path",
        value=current_folder,
        help="Specify the absolute path where downloaded files will be saved.",
    )

    if st.button("Save Settings", type="primary"):
        if os.path.exists(download_folder):
            st.session_state.config["download_folder"] = download_folder
            save_config(st.session_state.config)
            st.success("Download folder path saved!")
        else:
            st.error("Folder path does not exist. Please create or check the path.")


def placeholder_tab(tab_name):
    st.header(tab_name)
    st.info(f"Input text/URL parsing logic for {tab_name} goes here.")


def main():
    st.set_page_config(page_title="Media Downloader", layout="wide")
    init_session()

    st.title("Media Downloader")

    tabs = st.tabs(["ImageFap", "PornPics", "Downloader Queue", "Settings"])

    with tabs[0]:
        placeholder_tab("ImageFap")
    with tabs[1]:
        placeholder_tab("PornPics")
    with tabs[2]:
        placeholder_tab("Downloader Queue")
    with tabs[3]:
        settings_tab()


if __name__ == "__main__":
    main()