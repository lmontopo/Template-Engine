import re

# ------- This class will keep my resulting HTML ----------#
class ResultingHTML(object):
	def __init__(self, value = ""):
		self.value = value
	def update_output(self, html_text):
		try:
			self.value = self.value + html_text
		except TypeError:
			#this will help me catch errors in my html template
			str(html_text)
			self.value = self.value + html_text
		


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
		return 'VARIABLE'
	elif re.match("{%.*?%}", token):
		if re.match("{%\s*?end\s*%}", token):
			return 'BLOCK_END'
		else:
			return 'BLOCK_START'
	else:
		return 'TEXT'


# ---------- Tokenizer and Parser ----------- #
def tokenize(file):
	TOKENIZED = re.compile(r"({{.*?}}|{%.*?%})")
	with open(file, 'r') as template:
		text =  template.read()
		template_list = TOKENIZED.split(text)
		template_with_type = []
		for tok in template_list:
			token_type = determine_type(tok)
			if token_type == 'VARIABLE' or token_type == 'BLOCK_END' or token_type == 'BLOCK_START':
				token_value = tok[2:-2]
			else:
				token_value = tok
			token_data = { 'type': token_type, 'value': token_value}
			template_with_type.append(token_data)
		return template_with_type


def parse(input_t):
	output = []
	while True:
		item, input_t = input_t[0], input_t[1:]
		if (item['type'] != 'BLOCK_START' and item['type'] != 'BLOCK_END'):
			output.append(item)
			if len(input_t) == 0:
				break
		if item['type'] == 'BLOCK_START':
			sub_output, input_t = parse(input_t)
			sub_output.insert(0, item)
			output.append(sub_output)
			if len(input_t) == 0:
				break
		if item['type'] == 'BLOCK_END':
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
	if node['type'] == 'TEXT':
		return my_HTML.update_output(node['value'])
	if node['type'] == 'VARIABLE':
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

parsed_template = parse(tokenize('first_template.html'))
print parsed_template, 'parsed template'
outter_context = Scope(None, {'name': 'Leta', 'to_do': [['eat', 'sleep'], ['shower', 'homework']]})

eval_main(parsed_template, outter_context)
print "The resulting HTML is:\n", my_HTML.value

