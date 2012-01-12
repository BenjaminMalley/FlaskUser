import Flask_User.tests.user_api_tests as tests
import unittest
suite = unittest.makeSuite(UserAPITestCase, 'test')
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)