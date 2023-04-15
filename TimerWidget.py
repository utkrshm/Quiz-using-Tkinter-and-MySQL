# Import the Analyze Results function from another file for when the timer reaches 0

from tkinter import Tk, Label, messagebox as mb
import time
from gameplay import exit_quiz

def timer_widget(window: Tk, x_pos: int, y_pos: int, total_time: int, font_style: tuple, player_code):    
    while total_time:
        mins, secs = divmod(total_time, 60)
        timeformat = "{:02d}:{:02d}".format(mins, secs)         # ":02d" tells the computer to display that number in 2 digits, so 1 becomes 01
        
        Label(window, text=timeformat, font=font_style, bg='Grey34').place(x=x_pos, y=y_pos)
        
        window.update()
        
        total_time = total_time -1
        time.sleep(1)
    else:
        mb.showinfo(title='Time Elapsed!', message='Your time has elapsed, we will now analyze your results.')
        # Call the function that exits the quiz
        exit_quiz(player_code)
    