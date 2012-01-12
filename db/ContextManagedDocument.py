from mongoengine import Document

class ContextManagedDocument(Document):
	'''Uses a context manager to automatically save Document updates to the database'''
	def __enter__(self):
		return self

	def __exit__(self, *args):
		self.save()

