from bs4 import BeautifulSoup
import requests
import time
import os
import pyfiglet

def doRequest(requestedLink,n):
    url  = "https://ttsave.app/download"
    data = {
        "id" : str(requestedLink)    
    }
    try:
        req = requests.post(url, json=data)    
        soup = BeautifulSoup(req.content, "html.parser")
        link = []
        if (req.status_code==200):
            print("[+]", req.status_code, "OK downloading...")
            time.sleep(2)
            res1 = soup.find(id='button-download-ready')
            for value in res1.find_all('a'):
                link.append(value['href'])
            doDownload(link[0],n)
        else:
            print("[+]", req.status_code, ": Error Check your connection...")
    except:
        print("[+] No Internet access!")
    
def doDownload(link,n):
    print("[+]",link)
    download = requests.get(link)
    try:
        check_dir = "../storage/shared/HammaTTD/" # change this directory output
        if (os.path.exists(check_dir)==True):
            with open(f"../storage/shared/HammaTTD/{str(n)}.mp4", "wb") as files: # change this directory output
                for chunk in download.iter_content(chunk_size=8192):
                    files.write(chunk)  
            print("[+] Download completed!")  
        else:
            parent_directory = "../storage/shared/" # change this directory output
            directory = "HammaTTD" # change this directory output
            full_directory = os.path.join(parent_directory, directory)
            os.mkdir(full_directory)
            with open(f"../storage/shared/HammaTTD/{str(n)}.mp4", "wb") as files: # change this directory output
                for chunk in download.iter_content(chunk_size=8192):
                    files.write(chunk)  
            print("[+] Download completed!")         
    except:
        print("[+] Path not found!")
        print("[+] Download failed!")
    
title = pyfiglet.Figlet(font="big", width=110)
print()
print(title.renderText("Tiktok Downloader"))
print("--------------------------------------")
print("https://github.com/Hamma-nyk")
print("--------------------------------------")

a = input("Tiktok Link : ")
n = input("Name file   : ")

doRequest(a,n)