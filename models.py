from mongoengine import * 
from datetime import datetime
from contextlib import contextmanager
#we need to set some global flags for requiring/not requiring fields so we can allow for reuse
#certainly, there's a better way, but for now we'll keep config.py out of version control
#and let users recreate it for each use
FULL_NAME_REQUIRED = False
EMAIL_REQUIRED = False
LOGIN_LOCATION_REQUIRED = False

class ContextManagerMixin():
	def __enter__(self):
		return self
		
	def __exit__(self, *args):
		self.save()

	@contextmanager
	def transaction(self):
		yield self
		self.save()

class Post(EmbeddedDocument, ContextManagerMixin):
	content = StringField()

class Login(EmbeddedDocument, ContextManagerMixin):
	timestamp = DateTimeField(default=datetime.now())
	location = GeoPointField(required=LOGIN_LOCATION_REQUIRED)	
	
class Password(EmbeddedDocument, ContextManagerMixin):
	hash = StringField()
	salt = BinaryField()
	
class User(Document, ContextManagerMixin):
	username = StringField()
	#using a list of passwords allows us to check against old passwords at password change
	passwords = ListField(EmbeddedDocumentField(Password), required=False)
	first_name = StringField(required=FULL_NAME_REQUIRED)
	last_name = StringField(required=FULL_NAME_REQUIRED)
	logins = ListField(EmbeddedDocumentField(Login), required=False)
	creation_time = DateTimeField(default=datetime.now())
	active = BooleanField(default=True)
	email = EmailField(required=EMAIL_REQUIRED)
	
	def _get_hash(self, p, s, rounds_left=500):
		import hashlib
		p = hashlib.sha512(s + p).hexdigest()
		if rounds_left > 0:
			return self._get_hash(p, s, rounds_left-1)
		else:
			return p
	
	def authenticate(self, attempt):
		password = self.passwords[-1]
		if self._get_hash(attempt, password.salt) == password.hash:
			return True
		else:
			return False
			
	def set_password(self, password):
		import os
		salt = str(os.urandom(16))
		self.passwords.append(Password(hash=self._get_hash(password, salt), salt=salt))
	
	def __repr__(self):
		return self.username
	
if __name__=='__main__':
	pass
	
	
	
