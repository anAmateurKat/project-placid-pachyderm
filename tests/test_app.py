#tests/test_app.py

import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
    
    def test_home(self):
        """
        Test the root directory.
        """
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert '<title>About Me</title>' in html
        assert 'Placid' in html
        assert '<link rel="stylesheet" href="static/styles/index.css">' in html
        assert '<img src="static/img/profile-pic.png" alt="Picture of Yourself" width="480" height="400">' in html

      def test_timeline(self):
        # checks timeline page elements
        response = self.client.get("/timeline.html")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Timeline</title>" in html
        assert '<label for="name">Name:</label> <br>' in html
        assert 'Timeline Posts' in html
        assert '<form id="form">' in html

    def test_timeline_get(self):
        # checks timeline "GET" portion of the api
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

    def test_timeline_post(self):
        # checks timeline "POST" portion of the api
        post_test = {"name":"Johnny Doe", "email":"johnny@doe.yay", "content":"Hello world!"}
        response = self.client.post("/api/timeline_post", data=post_test)
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert json['name'] == "Johnny Doe"
        assert json['email'] == "johnny@doe.yay"
        assert json['content'] == "Hello world!"

        # checks "GET" method to verify data added correctly
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json_gotit = response.get_json()
        assert "timeline_posts" in json_gotit
        assert len(json_gotit["timeline_posts"]) == 1

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post('/api/timeline_post', data={
            "email": "johndoe@email.com",
            "content": "Testing from test_app.py!"
        })
        html = response.get_data(as_text=True)
        assert response.status_code == 400, f"Response code: {response.status_code} html response is: {html}"
        assert "Error. Request missing the field 'name'" in html

        # POST request empty name
        response = self.client.post('/api/timeline_post', data={
            "name": "",
            "email": "johndoe@email.com",
            "content": "Testing from test_app.py!"
        })
        html = response.get_data(as_text=True)
        assert response.status_code == 400
        assert "Error. Name should not be empty" in html

        # POST request empty content
        response = self.client.post('/api/timeline_post', data={
            "name": "John Doe",
            "email": "johndoe@email.com",
            "content": ""
        })
        html = response.get_data(as_text=True)
        assert response.status_code == 400, f"Response code: {response.status_code} html response is: {html}"
        assert "Error. Content should not be empty" in html

        # POST request missing email
        response = self.client.post('/api/timeline_post', data={
            "name": "John Doe",
            "content": "Hello world, I'm John!"
        })
        html = response.get_data(as_text=True)
        assert response.status_code == 400, f"Response code: {response.status_code} html response is: {html}"
        assert "Error. Request missing the field 'email'" in html
        
        # POST request with malformed email
        response = self.client.post('/api/timeline_post', data={
            "name": "John Doe",
            "email": "johndoe-email.com",
            "content": "Hello world, I'm John!"
        })
        html = response.get_data(as_text=True)
        assert response.status_code == 400, f"Response code: {response.status_code} html response is: {html}"
        assert "Error. Invalid email" in html
