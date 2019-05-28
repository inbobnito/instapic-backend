import unittest
import json

from app.main import db
from app.test.base import BaseTestCase

class TestAuthBlueprint(BaseTestCase):
    def __makeUser(self):
        return self.client.post('/user/',
            data=json.dumps(dict(
                user_name='bobby91',
                password='test123456'
            )),
            content_type='application/json'
        )

    def __login(self):
        return self.client.post('/auth/login',
            data=json.dumps(dict(
                user_name='bobby91',
                password='test123456'
            )),
            content_type='application/json'
        )

    def testRegister(self):
        """ Test user registration """
        with self.client:
            response = self.__makeUser()
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def testRegisterAlreadyRegistered(self):
        """ Test registration with already registered email"""
        self.__makeUser()
        with self.client:
            response = self.__makeUser()
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'User already exists. Please Log in.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 409)

    def testLogin(self):
        """ Test login of a created user """
        with self.client:
            # user registration
            resp_register = self.__makeUser()
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.'
            )
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            response = self.__login()
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def testLoginNonRegistered(self):
        """ Test login of an unknown user """
        with self.client:
            response = self.__login()
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'username or password does not match.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)

    def testLogout(self):
        """ Test logout """
        with self.client:
            # user registration
            resp_register = self.__makeUser()
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.')
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # user login
            resp_login = self.__login()
            data_login = json.loads(resp_login.data.decode())
            self.assertTrue(data_login['status'] == 'success')
            self.assertTrue(data_login['message'] == 'Successfully logged in.')
            self.assertTrue(data_login['Authorization'])
            self.assertTrue(resp_login.content_type == 'application/json')
            self.assertEqual(resp_login.status_code, 200)
            # valid token logout
            response = self.client.post('/auth/logout', headers=dict(
                    Authorization=json.loads(
                        resp_login.data.decode()
                    )['Authorization']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out.')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()