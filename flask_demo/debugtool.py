from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

# the toolbar is only enabled in debug mode:
app.debug = True

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SECRET_KEY'] = 'asdf'

toolbar = DebugToolbarExtension(app)

@app.route('/it/')
def dict():


    return render_template('toolbar.html')




if __name__ == '__main__':

    app.run(host='0.0.0.0')
