import FlaskUser.tests.user_api_tests as tests
import unittest
suite = unittest.makeSuite(tests.DatabaseTestCase, 'test')
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
suite = unittest.makeSuite(tests.UserAPITestCase, 'test')
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
