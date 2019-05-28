import unittest
import datetime

from app.main import db
from app.main.service.user import create, findAll, findByUserName
from app.test.base import BaseTestCase


class TestUser(BaseTestCase):

    def __createTestUser(self, name):
        data = dict()
        data['password'] = 'test12345'
        data['user_name'] = name
        data['first_name'] = 'bob'
        data['last_name'] = 'bill'
        data['email_address'] = name + '@test.local'
        return create(data)

    def testCreateUser(self):
        res = self.__createTestUser('bob')
        self.assertTrue(res[1] == 201)

    def testCreateUserExist(self):
        self.__createTestUser('bob')
        res = self.__createTestUser('bob')
        self.assertTrue(res[1] == 409)
    
    def testFindUserByName(self):
        self.__createTestUser('bob')
        self.assertTrue(findByUserName('bob') is not None)

    def testFindNoUserByName(self):
        res = findByUserName('alice')
        self.assertTrue(res is None)

    def testFindAllUsers(self):
        self.__createTestUser('bob')
        self.__createTestUser('alice')
        self.__createTestUser('carl')
        res = findAll()
        self.assertTrue(res is not None)

if __name__ == '__main__':
    unittest.main()
