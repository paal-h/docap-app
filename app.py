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