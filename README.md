# Picture-Ripper
a basic picture ripper


make sure you have python installed any version 3.10 <> 3.14

clone the repo and create a venv folder with:

python -m venv venv

activate the venv folder: venv\scripts\activate.bat

run: pip install -r requirements.txt

afterwards run

streamlit run main.py

The app has 3 tabs: 

Cleaner:
paste all urls you like to rip
fill in a folder name
-> create folder -> export -> clean "clears the field for another model/girl/subject"

Downloader:

hit the Download Galleries -> it will download all the exports made earlier...so be carefull if you crate exports, it may take a while :D
the background app for the downloader is gallery-dl


Settings:
    a empty field to place the default location where you like the app to download your galleries to


used sources:

https://github.com/mikf/gallery-dl -> special thanks for such amazing app
https://streamlit.io/ -> for the lovley UI 
