from engine import *
import unittest 


class TestMain(unittest.TestCase):
	
	def setUp(self):
		my_HTML = ResultingHTML()
		print "Set up has terminated with html value: ", my_HTML.value


	def test_determine_type(self):
		self.assertEqual(determine_type('{{name}}'), 'VARIABLE')
		self.assertEqual(determine_type('{% end %}'), 'BLOCK_END')
		self.assertEqual(determine_type('{% end%}'), 'BLOCK_END')
		self.assertEqual(determine_type('{% for blah in blah %}'), 'BLOCK_START')
		self.assertEqual(determine_type('<html>Hey<h1>'), 'TEXT')

	def test_parser(self):
		template_for = 'first_template.html'
		parsed_for = [{'type': 'TEXT', 'value': '<html>\n'}, 
				[{'type': 'BLOCK_START', 'value': ' for item in to_do '}, 
				{'type': 'TEXT', 'value': '\n<li> Day \n\t'}, 
				[{'type': 'BLOCK_START', 'value': ' for task in item '}, 
				{'type': 'TEXT', 'value': '\n\t<li>'}, {'type': 'VARIABLE', 'value': 'task'}, 
				{'type': 'TEXT', 'value': '</li>\n\t'}], 
				{'type': 'TEXT', 'value': '\n</li>\n'}], 
				{'type': 'TEXT', 'value': '\n</html>\n\n'}]
		self.assertEqual(parse(tokenize(template_for))[0], parsed_for)

		template_conditional = 'else_template.html'
		parsed_conditional = [{'type': 'TEXT', 'value': '<html>\n<body>\n'},		
		 				[{'type': 'BLOCK_START', 'value': 'if num > 0 '}, 
		 				[{'type': 'TEXT', 'value': '\n'}, {'type': 'VARIABLE', 'value': 'num'},
		 				 {'type': 'TEXT', 'value': '\n'}], 
		 				 [{'type': 'TEXT', 'value': '\nOut of numbers!\n'}]], 
		 				 {'type': 'TEXT', 'value': '\n</body>\n</html>\n'}]
		self.assertEqual(parse(tokenize(template_conditional))[0], parsed_conditional)


	def test_output_loops(self):
		loops_html = "<html><li> Day <li>shower</li><li>fun</li></li><li> Day <li>errands</li><li>work</li></li></html>"
		template_for = 'first_template.html'
		vars_loop = {'name': 'Leta', 'to_do': [['shower', 'fun'],['errands', 'work']]}
		outter_context = Scope(None, vars_loop)
		eval_main(parse(tokenize(template_for))[0], outter_context)
		self.assertEqual(my_HTML.value, loops_html)


	# def test_output_conditional_else(self):
	# 	#my_HTML = ResultingHTML()
	# 	cond_html = "<html><body>Out of numbers!</body></html>"
	# 	template_cond = 'else_template.html'
	# 	vars_cond = {'num': -2}
	# 	outter_context = Scope(None, vars_cond)
	# 	eval_main(parse(tokenize(template_cond))[0], outter_context)
	# 	self.assertEqual(my_HTML.value, cond_html)
		


