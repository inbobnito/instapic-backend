import unittest
import json

from app.main import db
from app.test.base import BaseTestCase

class TestPicBlueprint(BaseTestCase):

    def __makeUser(self):
        return self.client.post('/user/',
            data=json.dumps(dict(
                user_name='bobby91',
                password='test123456'
            )),
            content_type='application/json'
        )

    def __getPics(self, token):
       return self.client.get('/pic/bobby91',headers=dict(Authorization=json.loads(token)['Authorization']),
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

    def __upload(self, token, title="Test Image", description="Please Ignore"):
        return self.client.post('/pic/', data=json.dumps(dict(
                image="data:image/png;base64,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",
                image_ext="image/png",
                title=title,
                description=description,
            )), headers=dict(Authorization=json.loads(token)['Authorization']),
            content_type='application/json'
        )


    def testUploadPic(self):
        """ Test upload a picture """
        with self.client:
            self.__makeUser()
            response = self.__login()
            response = self.__upload(token=response.data.decode())
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)


    def testUploadPicFail(self):
        """ Test upload a picture/post with incorrect values """
        with self.client:
            self.__makeUser()
            response = self.__login()
            response = self.__upload(title=None, description=None, token=response.data.decode())
            data = json.loads(response.data.decode())
            self.assertTrue(data['errors'] != None)
            self.assertEqual(response.status_code, 400)

    def testGetPicByUser(self):
        """ Test getting a picture by a user """
        with self.client:
            self.__makeUser()
            response = self.__login()
            self.__upload(token=response.data.decode())
            self.__upload(token=response.data.decode())
            self.__upload(token=response.data.decode())
            response = self.__getPics(token=response.data.decode())
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(len(data['data']) == 3)