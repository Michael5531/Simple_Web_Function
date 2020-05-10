'''
    This file will handle our typical Bottle requests and responses 
    You should not have anything beyond basic page loads, handling forms and 
    maybe some simple program logic
'''

from bottle import route, get, post, request, static_file

import model

#-----------------------------------------------------------------------------
# Static file paths
#-----------------------------------------------------------------------------

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

#-----------------------------------------------------------------------------

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

#-----------------------------------------------------------------------------

# Allow CSS
@route('/webfonts/<webfonts:path>')
def serve_webfonts(webfonts):
    '''
        serve_css

        Serves css from static/webfonts/

        :: webfonts :: A path to the requested webfonts

        Returns a static file object containing the requested webfonts
    '''
    return static_file(webfonts, root='static/webfonts/')

#-----------------------------------------------------------------------------

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

# Allow svgs
@route('/sprites/<sprites:path>')
def serve_js(js):
    return static_file(js, root='static/sprites/')

#-----------------------------------------------------------------------------
# Pages
#-----------------------------------------------------------------------------

# Display the register page
@get('/register')
def get_register_controller():
    '''
        get_register
        
        Serves the login page
    '''
    return model.register_form()

#-----------------------------------------------------------------------------

# Register the user
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
    email = request.forms.get('email')
    # Call the appropriate method
    return model.register_user(username, password, email)

#-----------------------------------------------------------------------------

# Redirect to main page
@get('/')
@get('/home')
def get_index():
    '''
        get_index
        
        Serves the index page
    '''
    return model.index()


#-----------------------------------------------------------------------------

# Display the login page
@get('/login')
def get_login_controller():
    '''
        get_login
        
        Serves the login page
    '''
    return model.login_form()

#-----------------------------------------------------------------------------

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


#-----------------------------------------------------------------------------

@get('/about')
def get_about():
    '''
        get_about
        
        Serves the about page
    '''
    return model.about()
   

#-----------------------------------------------------------------------------

@get('/logout')
def get_logout():
    '''
        Logs the user out
    '''
    return model.logout()

@get('/python')
def python_res():
    return model.get_resource('python');

@post('/python')
def python_comment():
    comment = request.forms.get('comment')
    return model.resource_comment('python', comment)

@get('/manage_users')
def manage_users():
    return model.manage_users()

@get('/profile/<username>')
def get_profile(username):
    return model.profile(username)