import sqlite3
from datetime import datetime
from totp_key import TOTPManager

class SQLconnector():
    """Class to get connection to a database"""

    def __init__(self):

        self. path = 'local-dekstop-manager'
        self.db_name = 'my.db'
        self.full_path = f'{self.path}/{self.db_name}'

        self.create_users_table()
        self.create_default_user()

    def perform_query(self, query: str, values: tuple=None, mode: str='commit'):
        """Using for connect to database and make some interactions"""

        try:
            with sqlite3.connect(self.db_name) as conn:

                cur = conn.cursor()
                cur.execute(query, values or ())
                
                if mode == 'fetchall':
                    rows = cur.fetchall()
                    return rows
                
                elif mode == 'fetchone':
                    row = cur.fetchone()
                    return row
                
                else:
                    conn.commit()

        except sqlite3.OperationalError as e:
            print('Error has been happened:', e)    
    
    def create_users_table(self):
        return self.perform_query(query="CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY," \
        "username text NOT NULL UNIQUE,password text NOT NULL,otp_key text NOT NULL UNIQUE,registration_date DATE NOT NULL);")
       
    def create_default_user(self):
        """Create admin user for login first time and create your own account in user managment"""
        
        if not self.get_the_user('admin'):
            return self.perform_query(query='INSERT INTO Users (username,password,otp_key,registration_date) VALUES(?,?,?,?)', 
                                    values=('admin','admin', 'NO_OTP', datetime.today().strftime('%Y-%m-%d %H:%M:%S')))

    def create_new_user(self, username, password):
        return self.perform_query(query='INSERT INTO Users (username, password, otp_key, registration_date) VALUES (?, ?, ?, ?)', 
                                 values=(username, password,TOTPManager.generate_totp(),datetime.today().strftime('%Y-%m-%d %H:%M:%S')))
        
    def get_all_users(self):
        return self.perform_query(query='SELECT id, username, registration_date from Users',mode='fetchall')
    
    def get_the_user(self, username):
        return self.perform_query(query="SELECT username from Users WHERE username=?", values=(username,),mode='fetchone')[0]

    def get_secret_key(self, username):
        return self.perform_query(query="SELECT otp_key from Users WHERE username=?", values=(username,), mode='fetchone')[0]

    def check_login(self, username, password):
        return self.perform_query(query='SELECT COUNT(username) from Users WHERE username=? AND password=?', 
                                 values=(username, password), mode='fetchone')[0]

    def delete_user(self, id):
        return self.perform_query(query='DELETE FROM Users WHERE id=?', values=(id,))

#Temporary list that won't be needed
sql_statements = [
    """CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        username text NOT NULL UNIQUE,
        password text NOT NULL,
        otp_key text NOT NULL UNIQUE,
        registration_date DATE NOT NULL
    
    );""",
    """INSERT INTO Users (username,password,otp_key,registration_date) VALUES(?,?,?,?)
"""

]       

   
sql_connector = SQLconnector()

