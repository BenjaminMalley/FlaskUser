import unittest
import sys
import os
from mongoengine import connect
from flask import Flask
import config #include mongolab configuration details; not included in repo for security reasons
sys.path.append(os.path.abspath('..'))
from user_api import *

class UserAPITestCase(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		connect(config.DATABASE,
			host=config.HOST,
			port=config.PORT,
			username=config.USERNAME,
			password=config.PASSWORD)
		User.drop_collection()
		super(UserAPITestCase, self).__init__(*args, **kwargs)
	
	def setUp(self):
		self.app = Flask(__name__)
		self.app.secret_key = 'test_key'
		self.test_client = self.app.test_client()

	def tearDown(self):
		pass
		
	def test_add_user(self):
		with User() as user:
			user.username = 'test_user'
		assert User.objects(username='test_user')[0].username == 'test_user'
		
	def test_password_authentication(self):
		'''test that a password can be set and authenticated against'''
		with User.objects(username='test_user')[0] as user:
			user.set_password('test_password')
		# a good password works
		assert user.authenticated('test_password') == True
		# and a bad one doesn't
		assert user.authenticated('bad_password') == False


	def test_user_login(self):
		self.app.add_url_rule('/login/', view_func=LoginView.as_view('login'), methods=['POST',])
		rv = self.test_client.post('/login/', data=dict(
			username='test_user',
			password='test_password'))
		assert 'authenticated' in rv.data
		rv = self.test_client.post('/login/', data=dict(
			username='test_user',
			password='bad_password'))
		assert 'error' in rv.data


			
if __name__=='__main__':
	unittest.main()
