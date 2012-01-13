from flask import Blueprint, render_template, current_app, request, session, url_for, redirect
from flask.views import View, MethodView
#import app from one directory up
from ..db.models import User, Login
from redirect import redirect_back

def login_required(view_function, failure_template='login_failure.html', *args, **kwargs):
	'''implements a login_required decorator that takes a login failure template as an argument
	(and provides a default template) which is returned if the user is not in flask.session'''
	if 'username' in session:
		return view_function(*args, **kwargs)
	else:
		return render_template(failure_template)

class UserAPI(MethodView):
	
	def get(self, user_id=None):
		return 'OK'
		#if user_id==None:
		#	return 'OK'
		#else:
		#	pass

	def post(self):
		if username_is_unique(request.form['username']):
			with User(username=request.form['username']) as user:
				user.set_password(request.form['password'])
			return 'OK'
		return 'error'
	
	#@login_required
	def delete(self, user_id=None):
		if user_id==None:
			return 'bad request'
		else:
			with User.objects(id=user_id)[0] as user:
				try:
					assert session['username'] == user.username
				except KeyError, AssertionError:
					return 'bad request'
				user.active = False
				return url_for('logout')
			
			
	def put(self):
		pass

class LoginAPI(MethodView):
	'''LoginAPI accepts GET and POST methods.  On GET, this method returns the login form.
	On POST, it authenticates the user and redirects to last visited page.

	LoginAPI also supplies a logout method as a classmethod.  This will probably change.
	
	A generic template supplied for the login form but is meant to be overridden on initialization.'''

	def __init__(self, template=None):
		'''specify a template when constructing the view'''
		self.template = template

	def post(self):
		with User.objects(username=request.form['username'])[0] as user:
			if user.authenticated(str(request.form['password'])) and user.active:
				#user is authenticated
				user.logins.append(Login())
				session['username'] = request.form['username']
				#redirect user back to referring page, falling back to index
				
				return redirect_back('index')
			else:
				#flash an error message
				return 'error' 
	
	def get(self):
		return render_template(template)

	@classmethod
	def logout(self):
		session.pop('username', None)
		return redirect(url_for('index'))

def username_is_unique(username):
	if User.objects(username=username) == None:
		return True
	else:
		return False


