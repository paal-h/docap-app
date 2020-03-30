from flask import Flask, render_template, jsonify
from flask_bootstrap import Bootstrap
app = Flask(__name__)
Bootstrap(app)

# The website version
@app.route('/')
@app.route('/<username>')
def home_page(username='World!'):
    return render_template('home.html', username=username)

# The json microservice version
@app.route('/api/hello/')
@app.route('/api/hello/<username>')
def api(username='World!'):
    return jsonify({'Hello': username})

@app.route('/api/version')
def version():
    '''This function returns a dictionary containing only
        the key version with a value set to the application
        version number which is read from a file called VERSION.txt
        The VERSION.txt file is
        extracted by taking the
        any whitespace (like \n
        converted to an integer
        or dots in them.
        read and the variable version is
        first line ([0]) and then removing
        from it) with strip(). It's not
        because sometimes versions have letters,
        :rtype: A Json object containing version: number'''

    with open("VERSION.txt", "r") as myfile:
        version_number = myfile.readlines()[0].strip()
    return jsonify({'version': version_number})