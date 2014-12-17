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
		ast = parse(tokens)[0]
		self.assertEqual(ast, [(TEXT, '')])

	def test_variable(self):
		tokens = tokenize(slurp("variable.html"))
		expected = [(TEXT, '<html>'), (VARIABLE, 'variable'), (TEXT, '</html>')]
		self.assertEqual(tokens, expected)
		ast = parse(tokens)[0]
		self.assertEqual(ast, expected)

	def test_get_ast(self):
		ast = get_ast(tokenize(slurp("variable.html")))
		expected = [(TEXT, '<html>'), (VARIABLE, 'variable'), (TEXT, '</html>')]
		self.assertEqual(ast,expected)
	
	def test_nested(self):
		ast = parse(tokenize(slurp("nested.html")))[0]
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
		ast = parse(tokenize(slurp("double_nested.html")))[0]
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
		ast = parse(tokenize(slurp("conditional.html")))[0]
		expected = [
					('TEXT', ''), 
						[
						('BLOCK_START', ' if num > 0 '), 
							[
							('TEXT', ''), 
							('VARIABLE', 'num'), 
							('TEXT', '')
							], 
							
							[
							('TEXT', ' Nope ')
							]
						], 
					('TEXT', '\n')
					]
		self.assertEqual(ast, expected)


	def test_output_simple(self):
		context = Scope(None, {})
		ast = parse(tokenize(slurp("basic.html")))[0]
		output = process_template(ast, context)
		self.assertEqual(output, '<html>Hi</html>')

	def test_render(self):
		context = {}
		output = render("basic.html", context)
		self.assertEqual(output, '<html>Hi</html>')
		
	def test_output_hello_var(self):
		context = Scope(None, {'name': 'Leta'})
		ast = parse(tokenize(slurp("hello.html")))[0]
		output = process_template(ast, context)
		self.assertEqual(output, '<html>Hey, Leta</html>')
		

if __name__ == '__main__': 
	unittest.main()
