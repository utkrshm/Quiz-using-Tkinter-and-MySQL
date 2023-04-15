from TimerWidget import timer_widget
from gameplay import *

from tkinter import *
import tkinter.messagebox as mb

from Global import *

def details_screen_closing_protocol(screen: Tk):
    mb.showinfo('Game exited!', 'We have exited the quiz as you do not want to enter your details.')
    screen.destroy()


def player_details_screen():
    details = Tk()
    details.title('Enter Player Details')
    details.geometry('294x225')
    
    player_code = StringVar()
    
    name = StringVar()
    cls_sec = StringVar()

    Label(details, text='ENTER PLAYER\'S DETAILS', font=('Arial', 15, 'bold'), fg=head_lbl_font_color, bg=head_lbl_bg_color, width=24).place(x=0, y=20)
    Label(details, text='To continue to play the quiz', font=('Arial', 11), fg=head_lbl_font_color, bg=head_lbl_bg_color, width=32).place(x=0, y=50)
        
    Label(details, text='Name:').place(x=45, y=100)
    Entry(details, textvariable=name).place(x=150, y=100)
    
    Label(details, text='Class And Section:').place(x=15, y=140)
    Entry(details, textvariable=cls_sec).place(x=150, y=140)
    
    Button(details, text='Start Quiz', command=lambda: insert_player_details(details, player_code, name, cls_sec)).place(x=70, y=180)
    Button(details, text='Exit', command=details.destroy).place(x=180, y=180)
        
    details.update()
    
    details.protocol('WM_DELETE_WINDOW', lambda: details_screen_closing_protocol(details))

    details.mainloop()
    
    
    return player_code.get()
    

def play_quiz(q_codes):    
    player_code = player_details_screen()

    if player_code == '':
        mb.showerror('Enter a valid name!', 'Please enter a valid name to play this quiz, and try again!!')
        return

    # Emptying the the player_result table in our database
    cur.execute('DELETE FROM PLAYER_RESULT')
    conn.commit()
    
    # Initializing the "Guest" screen, the screen where the player will play the quiz.
    guest = Tk()
    guest.title('Let\'s Play the Quiz')
    guest.geometry('400x375')
    guest.resizable(0, 0)
    
    # Adding the screen title
    Label(guest, text='PLAY QUIZ', font=('TkDefaultFont', 20, 'bold'), fg=head_lbl_font_color, bg=head_lbl_bg_color).pack(side=TOP, fill=X)

    # Adding the Question Details
    ques = StringVar(guest, name='question')

    optA = StringVar(guest, name='optionA')
    optB = StringVar(guest, name='optionB')
    optC = StringVar(guest, name='optionC')
    optD = StringVar(guest, name='optionD')
    q_no = IntVar(guest, name='questionNo.', value=1)

    # Adding the Question to the window
    Label(guest, text='Q      .').place(x=10, y=80)
    Label(guest, textvariable=q_no).place(x=25, y=80)
    Label(guest, textvariable=ques, height=2, wraplength=325, justify=LEFT).place(x=60, y=110)

    player_opt = StringVar(guest, name='Player Choice')

    Radio_A = Radiobutton(guest, textvariable=optA, variable=player_opt, value='A')
    Radio_A.place(x=60, y=165)

    Radio_B = Radiobutton(guest, textvariable=optB, variable=player_opt, value='B')
    Radio_B.place(x=60, y=190)

    Radio_C = Radiobutton(guest, textvariable=optC, variable=player_opt, value='C')
    Radio_C.place(x=60, y=215)

    Radio_D = Radiobutton(guest, textvariable=optD, variable=player_opt, value='D')
    Radio_D.place(x=60, y=240)

    # Adding the details of the first question to the screen
    details = get_ques_details(q_codes, 1)
    guest.setvar('question', details[0])
    guest.setvar('optionA', details[1])
    guest.setvar('optionB', details[2])
    guest.setvar('optionC', details[3])
    guest.setvar('optionD', details[4])

    tkVarNames = ('questionNo.', 'question', 'optionA', 'optionB', 'optionC', 'optionD')
        
    # Adding the buttons to the bottom of the screen
    next_btn = Button(guest, text='Next', width=15,
           command=lambda: display_next_question(player_code, q_codes, 'Player Choice', guest, next_btn, tkVarNames))
    next_btn.place(x=220, y=300)

    Button(guest, text='End Quiz', width=15, 
           command=lambda: exit_quiz(guest, player_code, 1)).place(x=50, y=300)
    
    # Adding the Timer Widget to our Quiz screen
    timer_widget(guest, 325, 38, 90, ('TkDefaultFont', 20, 'bold'), player_code)

    guest.mainloop()
    # We will not be doing "guest.update()" here as the timer_widget already enforces this function during its course, and it would return an
    # error if the screen was exited while the timer was running.`

