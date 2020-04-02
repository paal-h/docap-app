#things that we need to use
import unittest
import json
#load our application
from app import APP as tested_app
class TestApp(unittest.TestCase):

    def test_hello(self):
        # creating a FlaskClient instance to interact with the app
        app = tested_app.test_client()
        # calling /api/ endpoint
        hello = app.get('/api/hello/')
        # asserting the body
        body = json.loads(str(hello.data, 'utf8'))
        # the value of the Hello key should be default
        self.assertEqual(body['Hello'], 'World!')

    def test_hello_Jim(self):
        # creating a FlaskClient instance to interact with the app
        app = tested_app.test_client()
        # calling /api/ endpoint
        hello = app.get('/api/hello/Jim')
        # asserting the body
        body = json.loads(str(hello.data, 'utf8'))
        # the value of the Hello key should be default
        self.assertEqual(body['Hello'], 'Jim')

if __name__ == '__main__':
    unittest.main()