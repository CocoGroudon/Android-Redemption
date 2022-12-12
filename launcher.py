import tkinter as tk
import launcher_settings as st
from tkinter import ttk
import subprocess
import sys
import socket

def run():
    
    launcher.title(st.Game_title)

    screen_width = launcher.winfo_screenwidth()
    screen_height = launcher.winfo_screenheight()

    # find the center point
    center_x = int(screen_width/2 - st.window_width / 2)
    center_y = int(screen_height/2 - st.window_height / 2)

    launcher.geometry(f'{st.window_width}x{st.window_height}+{center_x}+{center_y}')

    launcher.resizable(False, False)

    # launcher.attributes('-alpha', 0.8)
    launcher.attributes('-topmost', 1)
    launcher.iconbitmap(st.icon_href)


    # Add Frame 1
    Frame = ttk.Frame(launcher)

    


    img = tk.PhotoImage(file = "./launcher_assets/Androidredemptioncover.png")
    bg_img = tk.Label( launcher, image = img, bg='grey')
    bg_img.place(x=0, y=0)

    startgame_button = ttk.Button(launcher, text="Start", width = 19)
    startgame_button.place(x= 500, y=320)
    startgame_button.configure(command=startgame)
    

    launcher.mainloop()

def startgame():
    launcher.lower()
    subprocess.run(['python', 'Game/main.py'])

class Account:
    def __init__(self, nickname, pwd, high_score) -> None:
        self.nickname = nickname
        self.pwd = pwd
        self.high_score = high_score
        self.userquery = []

    def create_user(self, nickname, pwd, highscore) -> str:
        import socket   
        hostname=socket.gethostname()   
        IPAddr=socket.gethostbyname(hostname) 
        print(hostname + " " + IPAddr)
        print(nickname + " " + pwd + " " + str(highscore))
        with open('player.txt', 'w') as f:
            f.write(hostname + "\n" + IPAddr + "\n"+ nickname +"\n" + pwd +"\n" + str(highscore) )

    def exist_user(self, nickname, pwd, highscore)-> bool:
        with open('player.txt') as f:
            [self.userquery.append(line.strip()) for line in f.readlines()] 
        print(self.userquery)
if __name__ == '__main__':
    launcher = tk.Tk()
    acc = Account("EuleRacker", "12", 0)
    acc.exist_user("Player", "pwd", 0)
    run()