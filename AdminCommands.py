'''
Functionalities in the admin interface:
       - Add Question
       - Update Question
       - Delete Question
       - Delete Player Record (for redundant records in the Quiz_History table)
'''
# Importing the GUI elements from Tkinter
from tkinter import *
import tkinter.messagebox as mb
import tkinter.ttk as ttk

# Connecting the database with the gui screen
from Global import *

conn, cur = connect_mysql()

# Getting a list of all the codes from the QUESTIONS table   (It will be useful for our Update and Delete Question functions)
cur.execute('SELECT CODE FROM QUESTIONS')
codes = []
for row in cur.fetchall():
    codes.append(row[0])


def display_information_on_tree(tree_type, tree: ttk.Treeview):
    global cur, conn
    
    tree.delete(*tree.get_children())
    
    if tree_type == 'questions':
        cur.execute('SELECT * FROM QUESTIONS;')
        data = cur.fetchall()
    elif tree_type == 'results':
        cur.execute('SELECT * FROM QUIZ_HISTORY;')
        data = cur.fetchall()
            
    for record in data:
        tree.insert('', END, values=record)
        
    conn.commit()


def display_question_in_toplvl(code, q_text: Text, widget_state, *strvars: StringVar):
    cur.execute(f'SELECT * FROM QUESTIONS WHERE CODE = "{code}"')
    deets = cur.fetchall()[0]

    q_text.config(state='normal')    
    q_text.insert('1.0', deets[1])
    q_text.config(state=widget_state)
    
    for i in range(len(strvars)):
        strvars[i].set("")
        strvars[i].set(deets[i+2])


# Defining the GUI screen wherein the functions will be carried out
def initialize_toplevel(master: Tk, function, tree: ttk.Treeview):
    # All the customizations to be made in the GUI TopLevel
    cust = {
        "ADD": {
            "Title": "Add Question",
            "Header Label Text": "ADD QUESTION",
            'Code Dropdown': False,
            'Widget State': 'normal',                           # True for enabled, False for disabled
            'Submit Button text': 'Add this Question'
        },
        "DELETE": {
            "Title": "Delete Question",
            "Header Label Text": "DELETE QUESTION",
            "Code Dropdown": True,
            'Widget State': 'disabled',                         # True for enabled, False for disabled
            'Submit Button text': 'Delete this Question'
        },
        "UPDATE": {
            "Title": "Update Question",
            "Header Label Text": "UPDATE QUESTION",
            "Code Dropdown": True,
            'Widget State': 'normal' ,                          # True for enabled, False for disabled
            'Submit Button text': 'Update this Question'
        }
    }
    
    customs = cust[function]
    
    # Defining the Toplevel window
    toplvl = Toplevel(master)
    toplvl.geometry('400x400')
    toplvl.title(customs['Title'])
    
    # Defining the StringVar variables that will be used in our screen
    code = StringVar()
    optA = StringVar()
    optB = StringVar()
    optC = StringVar()
    optD = StringVar()
    right_answer = StringVar()
    
    Label(toplvl, text=customs['Header Label Text'], bg='Black', fg='white').pack(side=TOP, fill=X)
    
    lbl_text = ['Code', 'Question', 'Right Choice', 'Option A', 'Option B', 'Option C', 'Option D']
    y_pos = [30, 70, 150, 190, 230, 270, 310]
    strvars = [optA, optB, optC, optD]
    
    for i in range(len(lbl_text)):
        Label(toplvl, text=lbl_text[i]).place(x=30, y=y_pos[i])
        Label(toplvl, text=":").place(x=130, y=y_pos[i])
        
        if i > 2:
            Entry(toplvl, textvariable=strvars[i-3], width=35, state=customs['Widget State']).place(x=160, y=y_pos[i])
       
    question = Text(toplvl, height=3, width=26, wrap=WORD)
    question.place(x=160, y=y_pos[1])
    
    choice_dropdown = ttk.OptionMenu(toplvl, right_answer, *['', 'A', 'B', 'C', 'D'])
    choice_dropdown.config(width=15, state=customs['Widget State'])
    choice_dropdown.place(x=160, y=y_pos[2])
         
    if customs['Code Dropdown']:
        strvars.insert(0, right_answer)
        
        codes_dropdown = ttk.OptionMenu(toplvl, code, *codes, 
                                        command=lambda code: display_question_in_toplvl(code, question, customs['Widget State'], *strvars))
        codes_dropdown.config(width=25)
        codes_dropdown.place(x=160, y=y_pos[0])
    else:
        Entry(toplvl, textvariable=code, width=35, state=customs['Widget State']).place(x=160, y=y_pos[0])

    submit_btn = Button(toplvl, text=customs['Submit Button text'], width=20, 
           command=lambda: modify_db(tree, function, code.get(), question.get('1.0', 'end').strip(), optA.get(), optB.get(), optC.get(), optD.get(), right_answer.get()))
    submit_btn.place(x=125, y=355)
        
    toplvl.update()
    toplvl.mainloop()
    

# Defining a function to make the respective changes in the database
def modify_db(tree, command, code, question, optionA, optionB, optionC, optionD, right_answer):    
    if command == 'ADD':    
        cur.execute(f'INSERT INTO QUESTIONS VALUES ("{code}", "{question}", "{right_answer}", "{optionA}", "{optionB}", "{optionC}", "{optionD}");')
        conn.commit()
        mb.showinfo('Question Successfully Added!', f'Question with the ID "{code}" has been added successfully.')
    
    elif command == 'UPDATE':    
        q = f'''UPDATE QUESTIONS 
                    SET 
                        QUESTION = "{question}", 
                        RIGHT_ANSWER_CHOICE = "{right_answer}", 
                        OPTION_A = "{optionA}", 
                        OPTION_B = "{optionB}", 
                        OPTION_C = "{optionC}", 
                        OPTION_D = "{optionD}"
                    WHERE CODE = "{code}";'''
        cur.execute(q)
        conn.commit()
        mb.showinfo('Question Successfully Updated!', f'Question with the ID "{code}" has been updated successfully.')
    
    elif command == 'DELETE':
        cur.execute(f'DELETE FROM QUESTIONS WHERE CODE = "{code}";')
        conn.commit()
        mb.showinfo('Question Successfully Deleted!', f'Question with the ID \'{code}\' has been successfully removed from the database.')
    
    display_information_on_tree('questions', tree)


# Defining a function that will remove a player record from the database, in case it is a redundant record
def delete_player_record(tree: ttk.Treeview):
    if not tree.selection():
        mb.showerror('Error!', 'Please select the player whose record you want to delete.')
        return
 
    current_item = tree.focus()
    record = tree.item(current_item)    
    values = record["values"]  # ()
    
    try:
        cur.execute(f'DELETE FROM QUIZ_HISTORY WHERE PLAYER_CODE="{values[0]}"')
        conn.commit()
    except Exception as e:
        mb.showerror('Wrong Database!', 'Please select a record only from the Results table, as you cannot delete a question via this method!')
    
    tree.delete(current_item)
    
    mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.')
    
    display_information_on_tree('results', tree)

