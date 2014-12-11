import re

BLOCK_START = "BLOCK_START"
BLOCK_END   = "BLOCK_END"
BLOCK_ELSE  = "BLOCK_ELSE"
VARIABLE    = "VARIABLE"
TEXT		= "TEXT"

# ------- This class will keep my resulting HTML ----------#
class ResultingHTML(object):
	def __init__(self, value = ""):
		self.value = value
	def update_output(self, html_text):
		html_text = str(html_text)
		self.value = self.value + html_text
		self.value = self.value.replace('\n', '')
		self.value = self.value.replace('\t', '')

my_HTML = ResultingHTML()


# ------------ Scope Class ------------- # 

class Scope(object):
	def __init__(self, parent, dictionary):
		self.parent = parent
		self. dictionary = dictionary

	def add(self, input):
		dictionary.update(input)

	def fetch(self, input_key):
		try:
			value = self.dictionary[input_key]
		except:
			value = self.parent.fetch(input_key)
		return value


# --------- Determines Type of Node ------------ #
def determine_type(token):
	if re.match("{{.*?}}", token):
		return VARIABLE
	elif re.match("{%.*?%}", token):
		if re.match("{%\s*?end\s*%}", token):
			return BLOCK_END
		else:
			return BLOCK_START
	else:
		return TEXT


# ---------- Tokenizer and Parser ----------- #
def tokenize(template_text):
		TOKENIZED = re.compile(r"({{.*?}}|{%.*?%})")
		template_list = TOKENIZED.split(template_text)
		template_with_type = []
		for tok in template_list:
			token_type = determine_type(tok)
			if token_type == VARIABLE or token_type == BLOCK_END or token_type == BLOCK_START:
				token_value = tok[2:-2]
			else:
				token_value = tok
			token_data = (token_type, token_value)
			template_with_type.append(token_data)
		return template_with_type


def parse(input_t):
	output = []
	while True:
		item, input_t = input_t[0], input_t[1:]
		if (item[0] != BLOCK_START and item[0] != BLOCK_END):
			output.append(item)
			if len(input_t) == 0:
				break
		if item[0] == BLOCK_START:
			sub_output, input_t = parse(input_t)
			sub_output.insert(0, item)
			output.append(sub_output)
			if len(input_t) == 0:
				break
		if item[0] == BLOCK_END:
			return output, input_t
	return output


# ----------- Main Evaluation ------------- #
def eval_main(parsed_template, context):
	for item in parsed_template: 
		if type(item) is list:
			evaluate_list(item, context)
		elif type(item) is dict:
			evaluate_node(item, context)


def evaluate_node(node, context):
	if node['type'] == TEXT:
		return my_HTML.update_output(node['value'])
	if node['type'] == VARIABLE:
		var_value = context.fetch(node['value'])
		return my_HTML.update_output(var_value)

def evaluate_list(list_input, context):
	if bool((re.search("for\s.*?\sin", list_input[0]['value']))):
		do_for_loop(list_input, context)
	if bool((re.match(".?if", list_input[0]['value']))):
		do_conditional(list_input, context)

def do_for_loop(list_input, context):
	head, rest = list_input[0], list_input[1:]
	#Here I will parse the for loop and the rest of block
	item_var = re.search("for\s(.*?)\sin\s.*?\s.?", list_input[0]['value']).group(1)
	copy = item_var
	list_var = re.search("for\s.*?\sin\s(.*?)\s.?", list_input[0]['value']).group(1)
	for item_var in context.fetch(list_var):
		inner_context = Scope(context, {'%s' %copy: item_var})
		eval_main(rest, inner_context)

def do_conditional(list_input, context):
	#Here I will eval the conditional and then act accordingly
	pass


# ---------- Running Things ---------------- #

# template_1 = 'first_template.html'
# template_3 = 'else_template.html'


# parsed_template1 = parse(tokenize(template_1))[0]
# print "Parsed template #1: ", parsed_template1, '\n'
# vars_1 = {'name': 'Leta', 'to_do': [['shower', 'fun'],['errands', 'work']]}
# outter_context1 = Scope(None, vars_1)
# eval_main(parsed_template1, outter_context1)
# print "The resulting HTML for template 1 is :\n", my_HTML.value, '\n'

# parsed_template3 = parse(tokenize(template_3))[0]
# print "Parsed Template #3: ", parsed_template3, '\n'
# vars_3 = {'name': 'Leta', 'num': -2}
# outter_context3 = Scope(None, vars_3)
# eval_main(parsed_template3, outter_context3)
# print "The resulting HTML for template 3 is :\n", my_HTML.value, '\n'


# new_file = open('else.html', 'w')
# new_file.write(my_HTML.value)
# new_file.close
