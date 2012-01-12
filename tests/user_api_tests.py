import unittest
from mongoengine import connect
from flask import Flask, session
import config #include mongolab configuration details; not included in repo for security reasons
from ..user_api.user_api import *

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
		self.app.add_url_rule('/', view_func=UserAPI.as_view('index'), methods=['GET', 'POST'])
		self.app.add_url_rule('/logout/', view_func=LoginAPI.logout)
		self.app.add_url_rule('/login/', view_func=LoginAPI.as_view('login'),
			methods=['GET', 'POST'])
		self.app.add_url_rule('/delete/<user_id>/', view_func=UserAPI.as_view('user_api'),
			methods=['DELETE'])
		self.test_client = self.app.test_client()
	
	def tearDown(self):
		#nothing to do for tear down
		pass
		
	def add_user(self):
		'''adds user to collection and returns user instance'''
		with User() as user:
			user.username = 'test_user'
			user.set_password('test_password')
		return user
	
	def delete_user(self):
		'''removes test user from collection'''
		User.objects(username='test_user')[0].delete()

	def login(self, password):
		return self.test_client.post('/login/', data=dict(
			username='test_user',
			password=password),
			follow_redirects=True)

	def test_add_user(self):
		'''tests adding a user through the db api'''
		self.add_user()
		assert User.objects(username='test_user')[0].username == 'test_user'
		
	def test_password_authentication(self):
		'''test that a password can be set and authenticated against'''
		user = self.add_user()
		# a good password works
		assert user.authenticated('test_password') == True
		# and a bad one doesn't
		assert user.authenticated('bad_password') == False
		self.delete_user()
	
	def test_UserAPI_delete(self):
		'''test setting a user to inactive through UserAPI.
		ensures that deletion only works when user is logged in.'''
		user = self.add_user()
		with self.app.test_client() as c:
			#first check when user isn't logged in
			rv = c.delete('/delete/{0}/'.format(user.id))
			assert User.objects(username='test_user')[0].active == True
			with c.session_transaction() as sess:
				sess['username'] = 'test_user'
			rv = c.delete('/delete/{0}/'.format(user.id))
			assert User.objects(username='test_user')[0].active == False
		self.delete_user()

	def test_LoginAPI_post(self):
		user = self.add_user()
		#good password works
		assert 'OK' in self.login('test_password').data
		#bad password doesn't
		assert 'error' in self.login('bad_password').data
		user.active = False
		user.save()
		#inactive users can't log in
		assert 'error' in self.login('test_password').data
		self.delete_user()

	def test_user_logout(self):
		rv = self.test_client.get('/logout/', follow_redirects=True)
		assert 'OK' in rv.data

