import unittest
from main import create_app
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["FLASK_ENV"]="testing"

class TestCourses(unittest.TestCase):
    def setUp(self):
        # need to create an app instance to test
        self.app = create_app()
        # the app instance has a handy test_client function
        # this generates an imaginary browser that can make requests
        self.client = self.app.test_client()
    
    def test_transaction_index(self):
        # we use the client to make a request
        response = self.client.get("/transactions/")
        data = response.get_json()
        
        # Now we can perform tests on the response
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_create_bad_transaction(self):
        response = self.client.post("/transactions/", json={"transaction_name": ""})
        self.assertEqual(response.status_code, 400)
