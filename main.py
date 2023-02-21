from pathlib import Path
from tkinter import *
from tkinter import filedialog
from bs4 import BeautifulSoup
from PIL import ImageTk, Image
import requests
import time

def selectPath():
        path = filedialog.askdirectory()
        path_field.insert(0, path)
        
def doRequest():
    if(link_field.get()!="" and path_field.get()!="" and filename_field.get()!=""):
        url  = "https://ttsave.app/download"
        data = {
            "id" : str(link_field.get())    
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
                doDownload(link[0])
            else:
                print("[+]", req.status_code, ": Error Check your connection...")
        except:
            status_label.configure(text="Status : No Internet access!")
    else:
        status_label.configure(text="Status : Fill all form!")

def doDownload(link):
    print("[+]",link)
    download = requests.get(link)
    try:
        with open(f"{path_field.get()}/{filename_field.get()}.mp4", "wb") as files:
            for chunk in download.iter_content(chunk_size=8192):
                files.write(chunk)  
        status_label.configure(text="Status : Download completed!")
        print("[+] Download completed!")         
    except:
        print("[+] Path not found!")
        status_label.configure(text="Status : Download failed!")  
        print("[+] Download failed!")
    
screen = Tk()
screen.title("Tiktok Downloader")
screen.geometry("485x255")
screen.configure(background="#e0e0e0")
screen.resizable(False,False)
p = Path(__file__).with_name('icon.ico')
screen.iconbitmap(p)

# Logo
p = Path(__file__).with_name('logo.png')
logo = Image.open(p)
logo = logo.resize((160,50))
my = ImageTk.PhotoImage(logo)
logo_label = Label(screen, image=my, background="#e0e0e0")
logo_label.grid(column=0,row=0, columnspan=3,pady=15)

# Tiktok Link
link_label = Label(screen, text="Tiktok Link ", font=('arial',10), background="#e0e0e0")
link_label.grid(column=0,row=1, sticky="W",padx=5)
link_field = Entry(screen, width=54, font=('arial',10))
link_field.grid(column=1,row=1,columnspan=2, sticky="W",pady=5)

# Select Path
path_label = Label(screen, text="Select Folder ", font=('arial',10), background="#e0e0e0")
path_label.grid(column=0,row=2, sticky="W",padx=5)
path_field = Entry(screen, width=40, font=('arial',10))
path_field.grid(column=1,row=2, sticky="W")
path_button  = Button(screen, text="Browse",width=12, command=selectPath)
path_button.grid(column=2,row=2, sticky="W",pady=2)

# Filename
filename_label = Label(screen, text="File Name ", font=('arial',10), background="#e0e0e0")
filename_label.grid(column=0,row=3, sticky="W",padx=5)
filename_field = Entry(screen, width=54, font=('arial',10))
filename_field.grid(column=1,row=3, sticky="W",columnspan=2,pady=5)

# Status
status_label = Label(screen, text="Status : ", font=('arial',10), background="#e0e0e0")
status_label.grid(column=0,row=4,columnspan=3,pady=2)

check_button  = Button(screen, text="Download",width=30, command=doRequest, font=("arial",10,"bold"))
check_button.grid(column=0,row=5,pady=5,columnspan=3)
screen.mainloop()