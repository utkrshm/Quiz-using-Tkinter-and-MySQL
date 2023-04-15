from admin import admin
from guest import play_quiz

from tkinter import *               # for GUI  
import tkinter.messagebox as mb     # To display messages

from PIL import ImageTk, Image

from Global import *

from gameplay import randomise_questions

conn, cur = connect_mysql()

def verify_login(win: Tk, role: str, pwd: str):
    cred = [(role.strip().lower(), pwd)]
    
    cur.execute(f'SELECT * FROM LOGIN WHERE ROLE = "{role.lower()}"')
    auth = cur.fetchall()
        
    if cred == auth and role == 'admin'.casefold():
        win.destroy()
        
        admin()
    elif cred == auth and role == 'guest'.casefold():
        win.destroy()
        
        codes = randomise_questions(5)
        play_quiz(codes)
    elif cred != cur.fetchall():
        mb.showerror('Login failed!', 'The entered username and password are incorrect! \nPlease recheck them and try again')


login = Tk()
login.title('Quiz Login')
login.geometry('300x300')

username = StringVar()
password = StringVar()

Label(login, text='LOGIN', fg=head_lbl_font_color, bg=head_lbl_bg_color).pack(side=TOP, fill=X)

# Label(master, text='', fg=, bg=)

image = Image.open('person-vector-image.png')
image = image.resize((80, 80), Image.ANTIALIAS)  

img = ImageTk.PhotoImage(image)
Label(login, image=img).place(x=110, y=40)

Label(login, text='Username           :').place(x=20, y=165)
Entry(login, textvariable=username, width=20).place(x=150, y=165)

Label(login, text='Password            :').place(x=20, y=195)
Entry(login, textvariable=password, width=20).place(x=150, y=195)

Button(login, text='LOGIN', fg='White', bg='Black', width=15,
       command=lambda: verify_login(login, username.get(), password.get())).place(x=92, rely=0.85)

login.update()
login.mainloop()