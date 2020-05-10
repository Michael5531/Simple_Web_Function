'''
    This file will handle our typical Bottle requests and responses 
    You should not have anything beyond basic page loads, handling forms and 
    maybe some simple program logic
'''

from bottle import route, get, post, request, static_file

import model


# -----------------------------------------------------------------------------
# Static file paths
# -----------------------------------------------------------------------------

# Allow image loading
@route('/img/<picture:path>')
def serve_pictures(picture):
    '''
        serve_pictures

        Serves images from static/img/

        :: picture :: A path to the requested picture

        Returns a static file object containing the requested picture
    '''
    return static_file(picture, root='static/img/')


# -----------------------------------------------------------------------------

# Allow CSS
@route('/css/<css:path>')
def serve_css(css):
    '''
        serve_css

        Serves css from static/css/

        :: css :: A path to the requested css

        Returns a static file object containing the requested css
    '''
    return static_file(css, root='static/css/')


# -----------------------------------------------------------------------------

# Allow javascript
@route('/js/<js:path>')
def serve_js(js):
    '''
        serve_js

        Serves js from static/js/

        :: js :: A path to the requested javascript

        Returns a static file object containing the requested javascript
    '''
    return static_file(js, root='static/js/')


# -----------------------------------------------------------------------------
# Pages
# -----------------------------------------------------------------------------

# Redirect to logi
@get('/home')
def get_index():
    '''
        get_index
        
        Serves the index page
    '''
    return model.index()


# -----------------------------------------------------------------------------

# Display the login page

@get('/login')
def get_login_controller():
    '''
        get_login
        
        Serves the login page
    '''
    return model.login_form()


# -----------------------------------------------------------------------------

# Attempt the login
@post('/login')
def post_login():
    '''
        post_login
        
        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    '''

    # Handle the form processing
    username = request.forms.get('username')
    password = request.forms.get('password')

    # Call the appropriate method
    return model.login_check(username, password)


# -----------------------------------------------------------------------------

@get('/about')
def get_about():
    '''
        get_about
        
        Serves the about page
    '''
    return model.about()

@post('/register')
def post_register():
    '''
        post_register
        
        Handles register
        Expects a form containing 'username' and 'password' fields
    '''

    # Handle the form processing
    username = request.forms.get('username')
    password = request.forms.get('password')
    # Call the appropriate method
    return model.register_user(username, password)


# -----------------------------------------------------------------------------
@get('/')
@get('/register')
def get_register():
    return model.register()


@get('/course_guide')
def get_course_guide():
    return model.course_guide()


@get('/which_major_is_right_for_you')
def get_major():
    return model.major()


@get('/Summer_and_Winter_School')
def get_s_and_w():
    return model.summer_winter()


@get('/Help_Available')
def get_help():
    return model.help_available()


@get('/Exchange_Opportunities')
def get_exchange():
    return model.exchange()


@get('/Academic_Integrity')
def get_academic():
    return model.academic()


@get('/Study_Tips')
def get_tips():
    return model.tips()


@get('/Study_Resources')
def get_resources():
    return model.resources()


@get('/Tips_for_Internships_and_Jobs')
def get_internships():
    return model.internships()


@get('/Messages')
def get_messages():
    return model.messages()


@post('/Messages')
def post_messages():
    recepient = request.forms.get('recepient')
    content = request.forms.get('content')

    return model.post_meassages(recepient, content)


@get('/Public_Forum')
def get_forums():
    return model.forums()


@post('/Public_Forum')
def post_forum():
    content = request.forms.get('content')
    return model.post_forum(content)