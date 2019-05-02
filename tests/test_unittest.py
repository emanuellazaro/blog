from app import app
import unittest2


class FlaskAppTests(unittest2.TestCase):

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def test_posts_status_code(self):
        # sends HTTP GET request to the application
        result = self.app.get('/posts/', follow_redirects=True)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_api_status_code(self):
        # sends HTTP GET request to the application
        result = self.app.get('/info/')
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_addpost_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        test_content = '{"post_title":"Test Post", "post_picture": "https://path_to_a_image", "post_content" : "It is just a test using unittest2 adding a new post", "published": True, "author_id": 1, "post_ID": 999}'
        result = self.app.post('/posts/', data=test_content, content_type='application/json', follow_redirects=True)

        # assert the status code of the response
        self.assertEqual(result.status_code, 201)

    """def test_updpost_status_code(self):
        # sends HTTP PUT request to the application
        # on the specified path
        result = self.app.put('/posts/test-post', data='{"post_title":"Update Test Post", "post_picture": "https://path_to_a_image", "post_content" : "It is just a test using unittest2 updating the post created before!" , "author_id":"1" }', content_type='application/json', follow_redirects=True)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_delusers_status_code(self):
        # sends HTTP Delete request to the application
        # on the specified path
        result = self.app.delete('/posts', data='{"post_slug":"update-test-post"}', content_type='application/json', follow_redirects=True)
        print (result)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)"""


if __name__ == "__main__":
    unittest2.main()
