from flask import Blueprint, render_template, current_app, request, session
from flask.views import MethodView
#import app from one directory up
import sys
import os
sys.path.append(os.path.abspath('..'))
from app import db
from models import User

class UserAPI(MethodView):
	
	def get(self, user_id=None):
		if user_id==None:
			pass
		else:
			pass

	def post(self, user_id=None):
		if user_id==None:
			pass
		else:
			pass
	
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
			pass
		else:
			#user is NOT authenticated
			pass


user_api.add_url_rule('/<unicode:user_id>/', methods=['GET', 'POST', 'DELETE'])

def login_required(view_function, failure_template='login_failure.html', *args, **kwargs):
	'''implements a login_required decorator that takes a login failure template as an argument
	(and provides a default template) which is returned if the user is not in flask.session'''
	if 'username' in session:
		return view_function(*args, **kwargs)
	else:
		return render_template(failure_template)


