import unittest
from mongoengine import connect
from flask import Flask, session
import config #include mongolab configuration details; not included in repo for security reasons
from ..user_api.user_api import *

class DatabaseTestCase(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		connect(config.DATABASE,
			host=config.HOST,
			port=config.PORT,
			username=config.USERNAME,
			password=config.PASSWORD)
		User.drop_collection()
		super(DatabaseTestCase, self).__init__(*args, **kwargs)

	@classmethod
	def add_user(cls):
		'''adds user to collection and returns user instance'''
		with User() as user:
			user.username = 'test_user'
			user.set_password('test_password')
		return user

	@classmethod
	def delete_user(self):
		'''removes test user from collection'''
		User.objects(username='test_user')[0].delete()
		return None

	def test_add_user(self):
		'''tests adding a user through the db api'''
		DatabaseTestCase.add_user()
		assert User.objects(username='test_user')[0].username == 'test_user'
		DatabaseTestCase.delete_user()

	def test_password_authentication(self):
		'''test that a password can be set and authenticated against'''
		user = DatabaseTestCase.add_user()
		# a good password works
		assert user.authenticated('test_password') == True
		# and a bad one doesn't
		assert user.authenticated('bad_password') == False
		DatabaseTestCase.delete_user()


class UserAPITestCase(unittest.TestCase):

	def __init__(self, *args, **kwargs):
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
		self.user = None
		super(UserAPITestCase, self).__init__(*args, **kwargs)

	def setUp(self):
		#nothing to do for set up
		self.user = DatabaseTestCase.add_user()
			
	def tearDown(self):
		#nothing to do for tear down
		self.user = DatabaseTestCase.delete_user()
		

	def login(self, password):
		return self.test_client.post('/login/', data=dict(
			username='test_user',
			password=password),
			follow_redirects=True)

	def test_delete_user(self):
		'''test setting a user to inactive through UserAPI.
		ensures that deletion only works when user is logged in.'''
		with self.app.test_client() as c:
			#first check when user isn't logged in
			rv = c.delete('/delete/{0}/'.format(self.user.id))
			assert User.objects(username='test_user')[0].active == True
			with c.session_transaction() as sess:
				sess['username'] = 'test_user'
			rv = c.delete('/delete/{0}/'.format(self.user.id))
			assert User.objects(username='test_user')[0].active == False

	def test_login(self):
		#good password works
		assert 'OK' in self.login('test_password').data
		#bad password doesn't
		assert 'error' in self.login('bad_password').data
		self.user.active = False
		self.user.save()
		#inactive users can't log in
		assert 'error' in self.login('test_password').data

	def test_user_logout(self):
		rv = self.test_client.get('/logout/', follow_redirects=True)
		assert 'OK' in rv.data

