from engine import *
import unittest 

class TestMain(unittest.TestCase):
	def test_determine_type(self):
		self.assertEqual(determine_type('{{name}}'), 'VARIABLE')
		self.assertEqual(determine_type('{% end %}'), 'BLOCK_END')
		self.assertEqual(determine_type('{% end%}'), 'BLOCK_END')
		self.assertEqual(determine_type('{% for blah in blah %}'), 'BLOCK_START')
		self.assertEqual(determine_type('<html>Hey<h1>'), 'TEXT')

	# def test_evaluate_node(self):
	# 	test_context = Scope(None, {'name': 'Leta', 'to_do': ['eat', 'homework']})
	# 	test_HTML = ResultingHTML()
	# 	evaluate_node({'type': 'TEXT','value': '<html><title>Hello, '}, test_context)
						
	# 	self.assertEqual(test_HTML.value,'<html><title>Hello, ' )