# Example Application

This project demonstrates how to write a very simple HTTP-based
application.

Example installation:

```sh
pipenv shell
```

Get dependencies:

```sh
pipenv install --deploy
```

Run:
```sh
FLASK_APP=app.py flask run
```

Test
```python 
# The json microservice version
@app.route('/api/hello/')
@app.route('/api/hello/<username>')
def api(username='World!'):
return jsonify({'Hello': username})
```
