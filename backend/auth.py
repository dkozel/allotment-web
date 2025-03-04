from flask_basicauth import BasicAuth

basic_auth = BasicAuth()

def init_basic_auth(app):
    app.config['BASIC_AUTH_USERNAME'] = 'tts'
    app.config['BASIC_AUTH_PASSWORD'] = 'password'
    basic_auth.init_app(app)