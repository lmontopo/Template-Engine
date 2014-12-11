from engine import *
import unittest 

def slurp(path):
	with open(path, "r") as f:
		return f.read()

class TestMain(unittest.TestCase):
	def test_determine_type(self):
		self.assertEqual(determine_type('{{name}}'), VARIABLE)
		self.assertEqual(determine_type('{% end %}'), BLOCK_END)
		self.assertEqual(determine_type('{% end%}'), BLOCK_END)
		self.assertEqual(determine_type('{% for blah in blah %}'), BLOCK_START)
		self.assertEqual(determine_type('<html>Hey<h1>'), TEXT)

	def test_empty(self):
		tokens = tokenize(slurp("empty.html"))
		self.assertEqual(tokens, [(TEXT, '')])
		ast = parse(tokens)
		self.assertEqual(ast, [(TEXT, '')])

	def test_variable(self):
		tokens = tokenize(slurp("variable.html"))
		expected = [(TEXT, '<html>'), (VARIABLE, 'variable'), (TEXT, '</html>\n')]
		self.assertEqual(tokens, expected)
		ast = parse(tokens)
		self.assertEqual(ast, expected)
	
	def test_nested(self):
		ast = parse(tokenize(slurp("nested.html")))
		expected = [
				('TEXT', ''),
				[
					('BLOCK_START', ' for item in to_do '),
					('TEXT', ' '),
					('VARIABLE', 'task'),
					('TEXT', ' ')
				],
				('TEXT', '\n')
			   ]
		self.assertEqual(ast, expected)

	def test_double_nested(self):
		ast = parse(tokenize(slurp("double_nested.html")))
		expected = [
				('TEXT', ''),
				[
					('BLOCK_START', ' for foo in foos '),
					('TEXT', '\n\t'),
					[
						('BLOCK_START', ' for bar in bars '),
						('TEXT', '\n\t\t'),
						('VARIABLE', 'foo'),
						('TEXT', ':'),
						('VARIABLE', 'bar'),
						('TEXT', '\n\t')
					],
					('TEXT', '\n')
				],
				('TEXT', '\n')
		           ]
		self.assertEqual(ast, expected)

	def test_conditional(self):
		ast = parse(tokenize(slurp("conditional.html")))
		print ast
		assertEqual(0, 1)

"""
	def test_parser(self):

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
"""

if __name__ == '__main__':
	unittest.main()
