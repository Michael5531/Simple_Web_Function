import sqlite3

# This class is a simple handler for all of our SQL database actions
# Practicing a good separation of concerns, we should only ever call 
# These functions from our models

# If you notice anything out of place here, consider it to your advantage and don't spoil the surprise

class SQLDatabase():
    '''
        Our SQL Database

    '''

    # Get the database running
    def __init__(self, database_arg="users.db"):
        self.conn = sqlite3.connect(database_arg)
        self.cur = self.conn.cursor()

    # SQLite 3 does not natively support multiple commands in a single statement
    # Using this handler restores this functionality
    # This only returns the output of the last command
    # Don't end commands with ;
    def execute(self, sql_string):
        out = None
        for string in sql_string.split(";"):
            try:
                self.cur.execute(string)
                out = self.cur.fetchall()
            except:
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
        self.execute("DROP TABLE IF EXISTS Comments")
        self.execute("DROP TABLE IF EXISTS Users")
        self.commit()

        # Create the users table
        self.execute("""CREATE TABLE IF NOT EXISTS Users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            email TEXT,
            admin INTEGER DEFAULT 0, 
            banned INTEGER DEFAULT 0,
            muted INTEGER DEFAULT 0,
            staff INTEGER DEFAULT 0,
            student INTEGER DEFAULT 0
        )""")

        self.execute("""CREATE TABLE IF NOT EXISTS Comments(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            text TEXT,
            page TEXT,
            FOREIGN KEY(user_id) REFERENCES Users(id)
        )""")

        self.commit()

        # Add some default users to show functionality
        self.add_user('admin', admin_password, 'admin@admin.edu.au', admin=1)
        self.add_user('joe', 'treelearn', 'joe@uni.edu.au', student=1)
        self.add_user('bad_boy', 'treelearn', 'bad_boy@uni.edu.au', banned=1, student=1)
        self.add_user('loud_mouth', 'treelearn', 'loud_mouth@uni.edu.au', muted=1, student=1)
        self.add_user('Dr Prof', 'treelearn', 'prof@uni.edu.au', staff=1)
        self.commit()

        # Add example comments
        self.add_comment('loud_mouth', 'hello', 'python')
        self.add_comment('loud_mouth', 'hello', 'python')
        self.add_comment('loud_mouth', 'hello', 'python')
        self.add_comment('loud_mouth', 'hello', 'python')
        self.add_comment('loud_mouth', 'hello', 'python')
        self.add_comment('loud_mouth', 'hello', 'python')
        self.add_comment('admin', 'hi', 'python')
        self.add_comment('Dr Prof', 'hi there', 'python')
        self.commit()



    #-----------------------------------------------------------------------------
    # User handling
    #-----------------------------------------------------------------------------

    # Add a user to the database
    def add_user(self, username, password, email,  admin=0, banned=0, muted=0, staff=0, student=1):
        sql_cmd = f"""
                INSERT INTO Users(username, password, email, admin, banned, muted, staff, student)
                VALUES('{username}', '{password}','{email}', {admin}, {banned}, {muted}, {staff}, {student});
            """


        self.execute(sql_cmd)
        self.commit()
        
        return True

    # Add comment to the database
    def add_comment(self, username, text, page):
        find_id = f"""SELECT id FROM Users WHERE username = '{username}' LIMIT 1"""
        user_id = self.execute(find_id)[0][0]
        sql_cmd = f"""
                INSERT INTO Comments(user_id, text, page)
                VALUES({user_id}, '{text}', '{page}');
            """
        self.execute(sql_cmd)
        self.commit()

    #-----------------------------------------------------------------------------

    # Check login credentials
    def check_credentials(self, username, password):
        login_valid = f"""
                SELECT 1 
                FROM Users
                WHERE username = '{username}' AND password = '{password}'
            """
        user_exists = f"""
                SELECT 1 
                FROM Users
                WHERE username = '{username}'
            """
        admin_check = f"""
                SELECT 1
                FROM Users
                WHERE username = '{username}' AND admin = 1
            """
        is_banned = f"""
                SELECT 1
                FROM Users
                WHERE username = '{username}' AND banned = 1
            """
        admin = self.execute(admin_check)
        if admin:
            admin = 1
        else:
            admin = 0
        
        res = self.execute(user_exists)
        if not res:
            return "Username not found", False, admin

        res = self.execute(is_banned)
        if res:
            return "Account is banned", False, admin
        
        res = self.execute(login_valid)
        if res:
            return "", True, admin
        else:
            return "Incorrect password",  False, admin