'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
import view
import random
from sql import SQLDatabase
# Initialise our views, all arguments are defaults for the template
page_view = view.View()

#-----------------------------------------------------------------------------
# Index
#-----------------------------------------------------------------------------

newdata = SQLDatabase()
newdata.database_setup()
newdata.message_data_setup()

logged_in = False

current_user = None

def request_page(pagename, **kwargs):
    global logged_in

    if logged_in:
        return page_view(pagename, header="header", **kwargs)
    else:
        return page_view(pagename, header="header_guest",**kwargs)


def index():
    '''
        index
        Returns the view for the index
    '''
    return request_page("index")

#-----------------------------------------------------------------------------
# Login
#-----------------------------------------------------------------------------

def login_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    return request_page("login")

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

    # By default assume good creds
    global logged_in
    global current_user
    logged_in = False
    if newdata.check_credentials(username,password)==True:
        login = True
    if login: 
        logged_in = True
        current_user = username
        return request_page ("index", name=username)
    else:
        return request_page("login", err_msg='incorrect ID and password')
    
#-----------------------------------------------------------------------------
# About
#-----------------------------------------------------------------------------


def register_user(username, password, admin=0):
    global logged_in
    global current_user
    newdata.add_user(username,password)
    logged_in = True
    current_user = username
    return request_page("index")

def register():
    return request_page("register")


def about():
    '''
        about
        Returns the view for the about page
    '''
    return request_page("about", garble=about_garble())
# Returns a random string each time
def about_garble():
    '''
        about_garble
        Returns one of several strings for the about page
    '''
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.", 
    "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
    "organically grow the holistic world view of disruptive innovation via workplace diversity and empowerment.",
    "bring to the table win-win survival strategies to ensure proactive domination.",
    "ensure the end of the day advancement, a new normal that has evolved from generation X and is on the runway heading towards a streamlined cloud solution.",
    "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return garble[random.randint(0, len(garble) - 1)]

#-----------------------------------------------------------------------------


def course_guide():
    return request_page("courseguide")


def major():
    return request_page("major")


def summer_winter():
    return request_page("summer_and_winter")


def help_available():
    return request_page("help_available")


def exchange():
    return request_page("exchange")


def academic():
    return request_page("academic")


def tips():
    return request_page("tips")


def resources():
    return request_page("resources")


def internships():
    return request_page("internships")


def messages():
    global current_user
    all_messages = ""
    message_list = newdata.find_chat(current_user)
    for m in message_list:
        mess = "Time: {}  Sender: {}  Recepient: {}\nContent:\n{}\n\n".format(m[0], m[1], m[3], m[2])
        all_messages += mess
    return request_page("messages", all_messages = all_messages)


def post_meassages(recepient, content):
    global current_user
    newdata.send_to_user(current_user, content, recepient)
    all_messages = ""
    message_list = newdata.find_chat(current_user)
    for m in message_list:
        mess = "Time: {}  Sender: {}  Recepient: {}\nContent:\n{}\n\n".format(m[0], m[1], m[3], m[2])
        all_messages += mess
    return request_page("messages", all_messages = all_messages)


def forums():
    all_messages = ""
    message_list = newdata.find_forum_message()
    for m in message_list:
        mess = "Time: {}  Sender: {}  Recepient: {}\nContent:\n{}\n\n".format(m[0], m[1], m[3], m[2])
        all_messages += mess
    return request_page("forums", all_messages = all_messages)


def post_forum(content):
    global current_user
    newdata.send_to_public(current_user, content)
    all_messages = ""
    message_list = newdata.find_forum_message()
    for m in message_list:
        mess = "Time: {}  Sender: {}  Recepient: {}\nContent:\n{}\n\n".format(m[0], m[1], m[3], m[2])
        all_messages += mess
    return request_page("forums", all_messages = all_messages)