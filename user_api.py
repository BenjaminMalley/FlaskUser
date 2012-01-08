from flask import Blueprint, render_template, current_app, request, session
from flask.views import View, MethodView
#import app from one directory up
from models import User, Login

def login_required(view_function, failure_template='login_failure.html', *args, **kwargs):
	'''implements a login_required decorator that takes a login failure template as an argument
	(and provides a default template) which is returned if the user is not in flask.session'''
	if 'username' in session:
		return view_function(*args, **kwargs)
	else:
		return render_template(failure_template)

class UserAPI(MethodView):
	
	def get(self, user_id=None):
		if user_id==None:
			pass
		else:
			pass

	def post(self):
		if username_is_unique(request.form['username']):
			with User(username=request.form['username']) as user:
				user.set_password(request.form['password'])
			return 'OK'
		return 'error'
	
	#@login_required
	def delete(self, user_id=None):
		if user_id==None:
			pass
		else:
			pass
			
	def login(self):
		error_message = None
		try:
			user = Users.objects(username=request.form['username'])
		except:
			error_message = 'an error'
		if user.authenticate(request.form['password']): 
			#user is authenticated
			return 'authenticated'
		else:
			#user is NOT authenticated
			with User(id=user_id) as user:
				user.active = False
			return 'not authenticated'
			
	def put(self):
		pass

class LoginView(View):
	'''A generic login view'''

	def __init__(self, template=None):
		'''specify a template when constructing the view'''
		self.template = template

	def dispatch_request(self):
		with User.objects(username=request.form['username'])[0] as user:
			if user.authenticated(str(request.form['password'])) and user.active:
				#user is authenticated
				user.logins.append(Login())
				session['username'] = request.form['username']
				return 'authenticated'
			else:
				#user is NOT authenticated
				return 'authentication error'

class LogoutView(View):
	def __init__(self, template=None):
		self.template = template

	def dispatch_request(self):
		session.pop('username', None)
		return 'user logged out'

def username_is_unique(username):
	if User.objects(username=username) == None:
		return True
	else:
		return False


