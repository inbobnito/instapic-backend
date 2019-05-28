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
        """ Test Create User """
        res = self.__createTestUser('bob')
        self.assertTrue(res[1] == 201)

    def testCreateUserExist(self):
        """ Test Create User on existing user """ 
        self.__createTestUser('bob')
        res = self.__createTestUser('bob')
        self.assertTrue(res[1] == 409)
    
    def testFindUserByName(self):
        """ Test Find User by name """ 
        self.__createTestUser('bob')
        self.assertTrue(findByUserName('bob') is not None)

    def testFindNoUserByName(self):
        """ Test Cannot find user by name """ 
        res = findByUserName('alice')
        self.assertTrue(res is None)

    def testFindAllUsers(self):
        """ Test Find all users """ 
        self.__createTestUser('bob')
        self.__createTestUser('alice')
        self.__createTestUser('carl')
        res = findAll()
        self.assertTrue(res is not None)

if __name__ == '__main__':
    unittest.main()
