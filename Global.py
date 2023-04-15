# Fonts
lbl_font = ()
btn_font = ()
head_lbl_font = ()

# Colors
head_lbl_bg_color = 'Black'     # Head Label Background Color
head_lbl_font_color = 'White'   # Head Label Font Color
btn_color = 'Grey25'            # Color of buttons

def connect_mysql():
    import mysql.connector as connector
    
    conn = connector.connect(host='localhost', username='root', password='root', database='ip_project')
    cur = conn.cursor()
    
    return conn, cur