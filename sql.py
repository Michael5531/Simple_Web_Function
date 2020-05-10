import sqlite3
from datetime import datetime
# This class is a simple handler for all of our SQL database actions
# Practicing a good separation of concerns, we should only ever call 
# These functions from our models

# If you notice anything out of place here, consider it to your advantage and don't spoil the surprise

class SQLDatabase():
    '''
        Our SQL Database

    '''

    # Get the database running
    def __init__(self):
        self.conn = sqlite3.connect("Users.db")
        self.cur = self.conn.cursor()

    # SQLite 3 does not natively support multiple commands in a single statement
    # Using this handler restores this functionality
    # This only returns the output of the last command
    def execute(self, sql_string):
        out = None
        for string in sql_string.split(";"):
            try:
                out = self.cur.execute(string)
            except:
                print("?????")
                pass
        return out

    # Commit changes to the database
    def commit(self):
        self.conn.commit()

    #-----------------------------------------------------------------------------
    
    # Sets up the database
    # Default admin password
    def database_setup(self, admin_password='admin'):

        # Clear the database if needed
        self.execute("DROP TABLE IF EXISTS Users")
        self.commit()

        # Create the users table

        self.execute("""CREATE TABLE Users(
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            admin INTEGER DEFAULT 0
        )""")

        self.commit()

        # Add our admin user
        self.add_user('admin', 'admin', admin=1)
        self.add_user('qiuyu','12345')

    #-----------------------------------------------------------------------------
    # User handling
    #-----------------------------------------------------------------------------

    # Add a user to the database
    def add_user(self, username, password, admin=0):

        self.cur.execute("select * from users where username='{}' ".format(username))
        if self.cur.fetchone():
            print("not successful")
            return False

        sql_cmd = """
                INSERT INTO Users(username,password,admin)
                VALUES( '{username}', '{password}', {admin})
            """

        sql_cmd = sql_cmd.format(username=username, password=password, admin=admin)

        self.execute(sql_cmd)
        self.commit()
        return True

    #-----------------------------------------------------------------------------

    # Check login credentials
    def check_credentials(self, username, password):
        sql_query = """
                SELECT 1 
                FROM Users
                WHERE username = '{username}' AND password = '{password}'
            """

        sql_query = sql_query.format(username=username, password=password)
        self.execute(sql_query)

        # If our query returns
        if self.cur.fetchone():
            return True
        else:
            return False

    def change_password(self,username,password):

        self.cur.execute("select * from users where username='{}' ".format(username) )

        if self.cur.fetchone()[2] == password:
            print("same password")
            return

        sql_query = """
                UPDATE Users
                SET password={password}
                WHERE username = '{username}'
            """
        sql_query = sql_query.format(username=username, password=password)
        self.execute(sql_query)
        self.commit()

    def message_data_setup(self):
        self.execute("DROP TABLE IF EXISTS Message")
        self.commit()
        self.execute("""CREATE TABLE Message(
            send_on TEXT, 
            username TEXT,
            content TEXT,
            send_to TEXT
        )""")
        self.commit()
    
    def send_to_public(self,username,content):
        cur_time = datetime.now().strftime("%D %H:%M:%S")
        self.execute("""
            INSERT INTO Message(send_on,username,content,send_to)
            VALUES('{}','{}','{}','public')
        """.format(cur_time,username,content))
        self.commit()

    def send_to_user(self,username,content,send_to):
        cur_time = datetime.now().strftime("%D %H:%M:%S")
        self.execute("""
            INSERT INTO Message(send_on,username,content,send_to)
            VALUES('{}','{}','{}','{}')
        """.format(cur_time,username,content,send_to))
        self.commit()
    
    def find_forum_message(self):
        self.execute("SELECT * FROM Message WHERE send_to = 'public' order by send_on")
        return(self.cur.fetchall())

    def find_chat(self,username):
        self.execute("""SELECT * FROM Message WHERE (username='{}') 
        or (send_to = '{}')  order by send_on""".format(username,username))
        return(self.cur.fetchall())


sql_db = SQLDatabase()
sql_db.message_data_setup()
sql_db.send_to_public('YU','HI')
sql_db.send_to_user('aa','bb','cc')
sql_db.send_to_user('cc','bb','aa')
print(sql_db.find_chat('aa'))


