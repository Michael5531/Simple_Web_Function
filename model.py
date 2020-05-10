'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
import view
import random
import sql

# Initialise our views, all arguments are defaults for the template
page_view = view.View()

# Initialise sql database connextion
sql_db = sql.SQLDatabase()

# Login state
logged_in = False

# User details
current_id = -1

# Titles
title_map = {
    "index":"Main Page",
    "register":"Register",
    "login":"Login",
    "about":"About",
    "resource_page":"{} Resources",
    "profile":"{}'s Profile",
    "manage_users":"Manage Users"
}


def user_detail(detail):
    if logged_in:
        query = f"SELECT {detail} FROM Users WHERE id = {current_id}"
        return sql_db.execute(query)[0][0]
    else:
        return None
    
def get_id(username):
    get_id = f"SELECT id  FROM Users WHERE username = '{username}'"
    return sql_db.execute(get_id)[0][0]

# Wrapper function for page_view
def request_page(pagename, **kwargs):
    global logged_in

    page_title = title_map[f"{pagename}"]

    if pagename == "resource_page":
        page_title = page_title.format(kwargs["title"].capitalize())
    elif pagename == "profile":
        page_title = page_title.format(kwargs["profile_name"])
    
    if logged_in:
        return page_view(pagename, header="header_user", page_title=page_title, username=user_detail('username'), admin=user_detail('admin'), muted=user_detail('muted'),  **kwargs)
    else:
        return page_view(pagename, header="header_guest", page_title=page_title, **kwargs)

#-----------------------------------------------------------------------------
# Index
#-----------------------------------------------------------------------------

def index():
    '''
        index
        Returns the view for the index
    '''
    return request_page("index")

#-----------------------------------------------------------------------------
# Register
#-----------------------------------------------------------------------------

def register_form():
    '''
        register_form
        Returns the view for the register_form
    '''
    return request_page("register", err_msg="")

#-----------------------------------------------------------------------------
# Register User
def register_user(username, password, email):
    global logged_in
    global current_id

    registered = f"SELECT * FROM Users WHERE username = '{username}'"
    email_linked = f"SELECT * FROM Users WHERE email = '{email}'"

    if email[-7:] != ".edu.au":
        return request_page("register", err_msg="Not an educational email")
    elif sql_db.execute(registered):
        return request_page("register", err_msg="Already registered")
    elif sql_db.execute(email_linked):
        return request_page("register", err_msg="Account with that email already exists")
    else:
        sql_db.add_user(username, password, email)
        logged_in = True
        current_id = get_id(username)
        return request_page("index")


#-----------------------------------------------------------------------------
# Login
#-----------------------------------------------------------------------------

def login_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    return request_page("login", err_msg="")

#-----------------------------------------------------------------------------

# Check the login credentials
def login_check(username, password):
    '''
        login_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''
    global logged_in
    global current_id
    err_msg = ""
    err_msg, login, is_admin = sql_db.check_credentials(username, password)
    if login:
        logged_in = True
        current_id = get_id(username)
        return request_page("index")
    else:
        return request_page("login", err_msg=err_msg)
    
#-----------------------------------------------------------------------------
# About
#-----------------------------------------------------------------------------

def about():
    '''
        about
        Returns the view for the about page
    '''
    return request_page("about")

#-----------------------------------------------------------------------------

def logout():
    global logged_in
    global current_id
    logged_in = False
    current_id = -1
    return request_page("index")

def resource(title, documentation, reading, questions):
    page = title.lower()

    get_comments = f"""
        SELECT username, text, admin, staff
        FROM Comments c JOIN Users u ON (c.user_id = u.id)
        WHERE page = '{page}' ORDER BY c.id DESC
    """

    comments = sql_db.execute(get_comments)
    if current_id == -1:
        return request_page("resource_page", title=title, documentation=documentation, reading=reading, questions=questions, logged_in=logged_in, comments=comments, muted=1)
    else:
        return request_page("resource_page", title=title, documentation=documentation, reading=reading, questions=questions, logged_in=logged_in, comments=comments)



def get_resource(pagename):
    if pagename == 'python':
        return resource(
            "Python",
            "<a href=\"https://www.python.org/doc/\">Python docs</a>",
            "<a href=\"https://www.w3schools.com/python/python_intro.asp\">Introduction to Python</a>",
            "<a href=\"https://www.guru99.com/python-interview-questions-answers.html\">Interview Questions</a>"
            )

def resource_comment(pagename, comment):
    sql_db.add_comment(username=user_detail('username'), text=comment, page=pagename)
    return get_resource('python')

def manage_users():
    users_query = """SELECT username, muted, banned, staff, student, admin FROM Users"""
    res = sql_db.execute(users_query)
    return request_page("manage_users", user_details=res)

def profile(username):
    detail_query = f"""
        SELECT email, admin, staff, muted, banned, student
        FROM Users
        WHERE username = '{username}'
    """
    email, admin, staff, muted, banned, student = sql_db.execute(detail_query)[0]
    return request_page(
        "profile",
        profile_name=username,
        profile_email=email,
        profile_admin=admin,
        profile_staff=staff,
        profile_muted=muted,
        profile_banned=banned,
        profile_student=student
    )
