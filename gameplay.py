from tkinter import *
import tkinter.messagebox as mb

import random
from time import sleep

from Global import *

from ResultAnalysis import *

conn, cur = connect_mysql()

def randomise_questions(n: int):
    cur.execute('SELECT CODE FROM QUESTIONS;')

    codes = []
    for row in cur.fetchall():
        codes.append(row[0])

    qs_for_this_round = random.sample(codes, n)
    
    return qs_for_this_round


def make_player_code(name: str):
    cur.execute(f'SELECT PLAYER_CODE FROM QUIZ_HISTORY WHERE NAME LIKE "{name[:4]}%"')
    
    code = name[:4].upper() + '-' + str(len(cur.fetchall())+1)
    
    return code


def insert_player_details(window: Tk, player_code: StringVar, *strvars: StringVar):
    'The StringVars provided as *args need to be in the order: Name, Class & Section'
        
    rules = '''
                    YOU ARE NOW ABOUT TO BEGIN THE QUIZ. \n\n
The quiz has only 5 questions, and you have only 5 minutes to complete them.
    
All questions are MCQ-based, and are based on various categories.
    
Once you select an option and click on the "Next" button, you WILL NOT be able to edit that response, so click that button very carefully.

When you reach the 5th question, you will not be able to click the "Next" button. 
At that point you'll have to end the quiz with the "End Quiz" button.

If at any point you click the "End Quiz" button or your time runs out before you have completed, 
your score only until that point will be considered, and your response to the current question will be dismissed.
                                \n\nALL THE BEST!
    '''
    try:
        player_code_str = make_player_code(strvars[0].get())
        
        for i in range(len(strvars)):
            assert strvars[i].get() != ''
        
        cur.execute(f'INSERT INTO QUIZ_HISTORY VALUES ("{player_code_str}", CURDATE(), "{strvars[0].get()}", "{strvars[1].get()}", 0, 0, 0)')
        conn.commit()
        
        player_code.set(player_code_str)
        
        mb.showinfo('Rules of the quiz', rules)
        window.destroy()
    except AssertionError:
        mb.showerror("Fields empty!", 'Please fill in all your details to start with the quiz!')


def get_ques_details(codes: list[str], q_no: int):
    code = codes[q_no-1]
    
    cur.execute(f'SELECT QUESTION, OPTION_A, OPTION_B, OPTION_C, OPTION_D, RIGHT_ANSWER_CHOICE FROM QUESTIONS WHERE CODE = "{code}"')
    
    return cur.fetchall()[0]


def append_player_record(q_code: str, q_no: int, player_choice: str):    
    # To get the details of the current question
    q, opta, optb, optc, optd, right_ans = get_ques_details([q_code], 1)
    
    if player_choice == right_ans:
        status = 1
    else:
        status = 0
    
    cur.execute(f'INSERT INTO PLAYER_RESULT VALUES ({q_no}, \"{q}\", "{player_choice}", "{right_ans}", "{opta}", "{optb}", "{optc}", "{optd}", {status})')
    conn.commit()


def display_next_question(player_code, q_codes, player_opt: str, window, next_btn: Button, VarNames: tuple):
    '''
    player_opt - The name of the StrVar responsible for noting the Player's chosen choice \n
    VarNames order - <Question No IntVar>, <Question StrVar>, <Option A StrVar>, <Option B StrVar>, <Option C StrVar>, <Option D StrVar>
    '''
    curr_q_no = window.getvar(name=VarNames[0])
    curr_q_code = q_codes[curr_q_no-1]
    player_choice = window.getvar(name=player_opt)
    
    if curr_q_no == len(q_codes)-1: 
        next_btn.config(text='Finish Quiz', 
                        command=lambda: finish_quiz(window, curr_q_code, player_choice, player_code))
    
    append_player_record(curr_q_code, curr_q_no, player_choice)
    
    new_q_no = curr_q_no + 1
    
    q_deets = get_ques_details(q_codes, new_q_no)
    
    window.setvar(name=VarNames[0], value=new_q_no)
    
    sleep(1)
    
    for i in range(1, len(VarNames)):
        window.setvar(name=VarNames[i], value=q_deets[i-1])
    
    window.update()


def exit_quiz(window, player_code, exit_status):
    if exit_status == 1:
        surety = mb.askyesno("Are you sure you want to exit the quiz?")
        
        if not surety:
            return
    
    cur.execute('SELECT * FROM PLAYER_RESULT')
    exit_q_no = cur.fetchall()[-1][0]
    
    cur.execute('SELECT SUM(status) FROM PLAYER_RESULT;')
    no_right_answers = cur.fetchall()[0][0]    
    
    no_wrong_answers = exit_q_no - no_right_answers

    cur.execute('SELECT ROUND(AVG(status)*100, 2) FROM PLAYER_RESULT;')
    percent_right_answers = cur.fetchall()[0][0]
    

    cur.execute(f'''UPDATE QUIZ_HISTORY 
                    SET NO_RIGHT_ANSWERS = {no_right_answers}, NO_WRONG_ANSWERS = {no_wrong_answers}, PERCENT = {percent_right_answers}
                    WHERE PLAYER_CODE = "{player_code}"''')
    conn.commit()
    
    mb.showinfo("Your result has being processed", 'We will now display you your result.')
    
    window.destroy()
    
    result_analysis_gui(player_code)


def finish_quiz(window, q_code, player_choice, player_code):
    append_player_record(q_code, 5, player_choice)
    exit_quiz(window, player_code, 0)

