import sqlite3
from datetime import datetime
from totp_key import TOTPManager

class SQLconnector():
    """Class to get connection to a database"""

    path = 'local-dekstop-manager'
    db_name = 'my.db'
    full_path = f'{path}/{db_name}'

    @classmethod    
    def perform_query(cls, query: str, values: tuple=None, mode: str='commit'):
        """Using for connect to database and make some interactions"""

        try:
            with sqlite3.connect(cls.db_name) as conn:

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
    
    @classmethod
    def create_db(cls):
        return cls.perform_query(query="CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY," \
        "username text NOT NULL UNIQUE,password text NOT NULL,otp_key text NOT NULL UNIQUE,registration_date DATE NOT NULL);")
       
    
    @classmethod
    def default_user(cls):
        """Create admin user for login first time and create your own account in user managment"""
        #TODO create a class for datetime if it'll be needed
        return cls.perform_query(query='INSERT INTO Users (username,password,otp_key,registration_date) VALUES(?,?,?,?)', 
                                 values=('admin','admin', 'NO_OTP', datetime.today().strftime('%Y-%m-%d %H:%M:%S')))

    @classmethod
    def create_new_user(cls, username, password):
        return cls.perform_query(query='INSERT INTO Users (username, password, otp_key, registration_date) VALUES (?, ?, ?, ?)', 
                                 values=(username, password,TOTPManager.generate_totp(),datetime.today().strftime('%Y-%m-%d %H:%M:%S')))
        
    @classmethod
    def get_all_users(cls):
        return cls.perform_query(query='SELECT id, username, registration_date from Users',mode='fetchall')
    
    @classmethod
    def get_secret_key(cls, username):
        return (cls.perform_query(query="SELECT otp_key from Users WHERE username=?", values=(username,), mode='fetchone')[0])

    @classmethod
    def check_login(cls, username, password):
        return cls.perform_query(query='SELECT COUNT(username) from Users WHERE username=? AND password=?', 
                                 values=(username, password), mode='fetchone')

    @classmethod
    def delete_user(cls, id):
        return cls.perform_query(query='DELETE FROM Users WHERE id=?', values=(id,))

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

   


