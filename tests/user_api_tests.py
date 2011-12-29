import unittest
import sys
import os
from mongoengine import connect
import CONFIG

class UserAPITestCase(unittest.TestCase):
	
	def setUp(self):
		print "hello"
	
	def tearDown(self):
		pass
	
if __name__=='__main__':
	connect(config.DATABASE,
		host=config.HOST,
		port=config.PORT,
		username=config.USERNAME,
		password=config.PASSWORD)
	unittest.main()
