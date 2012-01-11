import unittest
import sys
import os
from mongoengine import connect
from flask import Flask, session
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
		#add an index rule because some views redirect to index
		self.app.add_url_rule('/', view_func=UserAPI.as_view('index'), methods=['GET',])
		self.app.add_url_rule('/logout/', view_func=LogoutView.as_view('logout'))
		self.app.add_url_rule('/login/', view_func=LoginView.as_view('login'), methods=['POST',])
		self.app.add_url_rule('/delete/<user_id>/', view_func=UserAPI.as_view('user_api'),
			methods=['DELETE'])
		self.test_client = self.app.test_client()
	
	def tearDown(self):
		#nothing to do for tear down
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

	def login(self, password):
		return self.test_client.post('/login/', data=dict(
			username='test_user',
			password=password))

	def test_user_login(self):
		assert 'authenticated' in self.login('test_password').data
		assert 'error' in self.login('bad_password').data

	def test_user_logout(self):
		rv = self.test_client.get('/logout/', follow_redirects=True)
		assert 'OK' in rv.data

	def test_user_login_delete(self):
		user = User.objects(username='test_user')[0]
		with self.app.test_client() as c:
			with c.session_transaction() as sess:
				sess['username'] = 'test_user'
			rv = c.delete('/delete/{0}/'.format(user.id))
			print rv.data

if __name__=='__main__':
	unittest.main()
