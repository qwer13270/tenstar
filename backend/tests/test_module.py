""" Houses tests """

from .. import app
import unittest

class MyTestCase(unittest.TestCase):
    """ Wrapper for test cases """

    def setUp(self) -> None :
        """ Set up for testing """
        app.app.testing = True
        self.app = app.app.test_client()

    def test_index(self) -> None:
        """ Test index page """
        result = self.app.get('/')
        # Make your assertions
        self.assertEqual(1,1)

    def test_signup_page(self) -> None:
        """ Test signup page """
        response = self.app.get('/signup')
        self.assertEqual(response.status_code, 200)
      
    def test_login(self) -> None :
        """ Test Login page """
        result = self.app.get('/login')
        self.assertEqual(result.status_code, 200)
    
    # Test create-event-request
    # def test_create_event_request(self):
    #    event_creation = {
            
    #    }

    # Test logging in with valid credentials.
    #def test_login_valid_credentials(self):
    #    valid_credentials = {
    #       'email': 'test@gmail.com',  
    #        'password': 'test'     
    #   }
    #    response = self.app.post('/login-request', data=valid_credentials, follow_redirects=True)
    #   self.assertEqual(response.status_code, 200)
        # TODO: test router

    # Test logging in with invalid credentials
    #def test_login_invalid_credentials(self):
    #    invalid_credentials = {
    #        'email': 'test@gmail.com',  
    #        'password': 'wrongpassword'
    #    }
    #    response = self.app.post('/login-request', data=invalid_credentials)
    #    self.assertEqual(response.status_code, 401)

    # Test logging in with nonexistent account
    #def test_login_nonexistent_user(self):
    #    nonexistent_user = {
    #        'email': 'nonexistent@gmail.com', 
    #        'password': 'test'
    #    }
    #   response = self.app.post('/login-request', data=nonexistent_user)
    #    self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()

