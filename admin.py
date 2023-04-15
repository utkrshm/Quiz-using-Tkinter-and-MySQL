# Status -- Completed with the frontend and backend, only color scheme and font scheme remaining
from tkinter import *
import tkinter.ttk as ttk  # Themed Tkinter Widgets
from tkinter.font import Font

from AdminCommands import *

from Global import *

def admin():
       # Initializing the main GUI window
       root = Tk()
       root.title('Admin Quiz Management System')
       root.geometry('800x530')
       root.resizable(0, 0)

       # Variables - Colors and Fonts
       rtf_bg = 'Turquoise1'     # Right Top Frame Background Color
       btn_bg = 'SteelBlue'  # Background color for Buttons

       lbl_font = ('Georgia', 13)          # Font for all labels
       btn_font = ('Gill Sans MT', 13)     # Font for all buttons

       # Adding elements to the screen
       Label(root, text='ADMIN QUIZ MANAGEMENT', font=("Arial", 16, 'bold'), fg=head_lbl_font_color, bg=head_lbl_bg_color).pack(side=TOP, fill=X)

       # Frames
       RT_frame = Frame(root, bg=rtf_bg)
       RT_frame.place(y=30, relheight=0.2, relwidth=1)

       RB_frame = Frame(root)
       RB_frame.place(rely=0.24, relheight=0.785, relwidth=1)

       # Right Bottom Frame
       style = ttk.Style()
       style.theme_use('classic')
       style.map("TNotebook.Tab", background=[('selected', 'Aquamarine'), ('active', 'Red')])
       style.configure('TNotebook', background='LightSteelBlue')

       nb = ttk.Notebook(RB_frame)

       qs_nb = Frame(nb) 
       results_nb = Frame(nb) 
       b = Frame(nb)

       nb.add(results_nb, text='View all Results') 
       nb.add(qs_nb, text='All the Questions') 
       nb.add(b, text='All the')

       nb.pack(expand=1, fill='both')

       ## Notebook 1 - All the Results
       results_tree = ttk.Treeview(results_nb, selectmode=BROWSE, columns=('Player Code', 'Date', 'Name', 'Class', 'Right Answers', 'Wrong Answers', 'Percentage'))

       YScrollbar = Scrollbar(results_tree, orient=VERTICAL, command=results_tree.yview)
       YScrollbar.pack(side=RIGHT, fill=Y)

       results_tree.config(yscrollcommand=YScrollbar.set)

       results_tree.heading('Player Code', text='Player Code', anchor=CENTER)
       results_tree.heading('Date', text='Date', anchor=CENTER)
       results_tree.heading('Name', text='Name', anchor=CENTER)
       results_tree.heading('Class', text='Class & Section', anchor=CENTER)
       results_tree.heading('Right Answers', text='No. of Right Answers', anchor=CENTER)
       results_tree.heading('Wrong Answers', text='No. of Wrong Answers', anchor=CENTER)
       results_tree.heading('Percentage', text='Percentage', anchor=CENTER)

       results_tree.column('#0', width=0, stretch=NO)
       results_tree.column('#1', width=80, stretch=NO)
       results_tree.column('#2', width=85, stretch=NO)
       results_tree.column('#3', width=200, stretch=NO)
       results_tree.column('#4', width=110, stretch=NO)
       results_tree.column('#5', width=150, stretch=NO)
       results_tree.column('#6', width=150, stretch=NO)
       results_tree.column('#7', width=84, stretch=NO)

       results_tree.place(y=0, x=0, relheight=0.97, relwidth=1)
       
       display_information_on_tree('results', results_tree)


       ## Notebook 2 - All The Questions
       qs_tree = ttk.Treeview(qs_nb, selectmode=BROWSE, columns=('Code', 'Question', 'Right Answer', 'Option A', 'Option B', 'Option C', 'Option D'))

       XScrollbar = Scrollbar(qs_tree, orient=HORIZONTAL, command=qs_tree.xview)
       YScrollbar = Scrollbar(qs_tree, orient=VERTICAL, command=qs_tree.yview)
       XScrollbar.pack(side=BOTTOM, fill=X)
       YScrollbar.pack(side=RIGHT, fill=Y)

       qs_tree.config(xscrollcommand=XScrollbar.set, yscrollcommand=YScrollbar.set)

       qs_tree.heading('Code', text='Code', anchor=CENTER)
       qs_tree.heading('Question', text='Question', anchor=CENTER)
       qs_tree.heading('Right Answer', text='Right Answer', anchor=CENTER)
       qs_tree.heading('Option A', text='Option A', anchor=CENTER)
       qs_tree.heading('Option B', text='Option B', anchor=CENTER)
       qs_tree.heading('Option C', text='Option C', anchor=CENTER)
       qs_tree.heading('Option D', text='Option D', anchor=CENTER)

       qs_tree.column('#0', width=0, stretch=NO)
       qs_tree.column('#1', width=70, stretch=NO)
       qs_tree.column('#2', width=500, stretch=NO)
       qs_tree.column('#3', width=85, stretch=NO)
       qs_tree.column('#4', width=200, stretch=NO)
       qs_tree.column('#5', width=200, stretch=NO)
       qs_tree.column('#6', width=200, stretch=NO)
       qs_tree.column('#7', width=200, stretch=NO)

       qs_tree.place(y=0, x=0, relheight=0.95, relwidth=1)
       
       display_information_on_tree('questions', qs_tree)

       # Right Top Frame
       Button(RT_frame, text='Delete Question', font=btn_font, bg=btn_bg, width=17,
              command=lambda: initialize_toplevel(root, 'DELETE', qs_tree)).place(x=30, y=30)
       Button(RT_frame, text='Add Question', font=btn_font, bg=btn_bg, width=17,
              command=lambda: initialize_toplevel(root, 'ADD', qs_tree)).place(x=220, y=30)
       Button(RT_frame, text='Update Question', font=btn_font, bg=btn_bg, width=17,
              command=lambda: initialize_toplevel(root, 'UPDATE', qs_tree)).place(x=410, y=30)
       Button(RT_frame, text='Delete Player Record', font=btn_font, bg=btn_bg, width=17,
              command=lambda: delete_player_record(results_tree)).place(x=600, y=30)

       ### ----------------------------------------------------------

       # Finalizing the window
       root.update()
       root.mainloop()


admin()