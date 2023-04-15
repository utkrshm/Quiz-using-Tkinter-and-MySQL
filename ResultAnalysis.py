'''
Most functions on this page assume that the player who is asking for their results just took the
quiz, and his details have been added to the QUIZ_HISTORY table.
'''

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from tkinter import *
import tkinter.filedialog as fd
import tkinter.messagebox as mb

import pandas.io.sql as pd_sql

from Global import *

conn, cur = connect_mysql()

# Creating a function that turns the number of right and wrong answers the user had into a pie chart, 
# and embed that chart in the Results GUI screen.
def visualize_result(frame, player_code):
    q = f'''SELECT NO_RIGHT_ANSWERS, NO_WRONG_ANSWERS 
            FROM QUIZ_HISTORY 
            WHERE PLAYER_CODE = "{player_code}";'''
        
    fig = Figure(figsize=(6, 5), dpi=75)
    ax = fig.add_subplot(1, 1, 1)
    
    cur.execute(q)
    data = cur.fetchall()[0]
        
    ax.pie(data, labels=['No of Right Answers', 'No of Wrong Answers'], radius=1)
    
    chart = FigureCanvasTkAgg(fig, frame)
    chart.draw()
    chart.get_tk_widget().pack(fill=BOTH, expand=TRUE)
    

'''
Creating a function to allow the user to download a detailed record of their result
that allows them to see what questions they attempted, the choices they choose, 
the correct choice and the options they had.
''' 
def download_workbook():
    q = f'SELECT * FROM PLAYER_RESULT;'
    
    df = pd_sql.read_sql(q, conn)
    
    df.drop('status', axis=1, inplace=True)
    df.rename(columns={'q_no': "Q. No.", 'question': "Question", "player_choice": "Your Choice", 'right_choice': "Right Choice",
                       'option_a': "Option A", 'option_b': "Option B", 'option_c': "Option C", 'option_d': "Option D"}, inplace=True)
    try:
        path = fd.asksaveasfilename(defaultextension='.xlsx', filetypes=[('Excel Workbook', '*.xlsx'), ('Excel Worksheet', '*.xls')])
        df.to_excel(path, index=False)
        
        mb.showinfo('Download successfully!', 'Your result has been successfully downloaded as an Excel Workbook!')
    except:
        mb.showerror('No file location selected!', 'No file location has been selected to download the chart in, Please choose a location.')


# Creating a function that will allow the user to download the chart that they see on the Results screen.
def download_chart(player_code):
    q = f'''SELECT NO_RIGHT_ANSWERS, NO_WRONG_ANSWERS 
            FROM QUIZ_HISTORY 
            WHERE PLAYER_CODE = "{player_code}";'''
    cur.execute(q)
    
    plt.pie(cur.fetchall()[0], labels=['No of Right Answers', 'No of Wrong Answers'])
    plt.title('Your Result')
    
    try:
        path = fd.asksaveasfilename(confirmoverwrite=False, initialdir='shell:Downloads',
                            defaultextension='.png', 
                            filetypes=[('Portable Network Graphics', '*.png'), ('JPEG Format', '*.jpg')])
        plt.savefig(path)
        mb.showinfo('Download successfully!', 'Your result chart has been successfully downloaded!')
    except:
        mb.showerror('No file location selected!', 'No file location has been selected to download the result in, Please choose a location.')

   

# Defining the Results GUI screen.
def result_analysis_gui(player_code):
    res = Tk()
    res.geometry('700x400')
    res.title('Your Result')
    res.config(bg='White')
    
    Label(res, text='YOUR RESULT', fg='White', bg='Black', font=('Helvetica', 18, 'bold')).pack(side=TOP, fill=X)
    
    chart_frame = Frame(res, height=300, width=400, bg='Blue')
    chart_frame.place(x=0, y=35)
    
    visualize_result(chart_frame, player_code)
    
    Button(res, text='Download your detailed result', width=25, font=('Trebuchet MS', 12), height=2,
           command=download_workbook).place(x=450, y=70)
    Button(res, text='Download this chart', width=25, font=('Trebuchet MS', 12), height=2,
           command=lambda: download_chart(player_code)).place(x=450, y=180)
    Button(res, text='Exit the Quiz', width=25, font=('Trebuchet MS', 12), height=2,
           command=res.destroy).place(x=450, y=290)
        
    res.update()
    
    res.protocol("WM_DELETE_WINDOW", res.destroy)
    
    res.mainloop()


result_analysis_gui('UTKA-4')