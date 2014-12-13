import re
import sys

BLOCK_START = "BLOCK_START"
BLOCK_END   = "BLOCK_END"
BLOCK_ELSE  = "BLOCK_ELSE"
VARIABLE    = "VARIABLE"
TEXT		= "TEXT"

# ------- This class will keep my resulting HTML ----------#
class ResultingHTML(object):
	def __init__(self, value = ""):
		self.value = value
		with open ('value.txt', 'a') as erfile:
			erfile.write('We are re-instantiating and the value is: %s' %self.value)
	def update_output(self, html_text):
		html_text = str(html_text)
		self.value = self.value + html_text
		self.value = self.value.replace('\n', '')
		self.value = self.value.replace('\t', '')



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
		elif re.match("{%\s*?else\s*%}", token):
			return BLOCK_ELSE
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
		if (item[0] != BLOCK_START and item[0] != BLOCK_END and item[0] != BLOCK_ELSE):
			output.append(item)
			if len(input_t) == 0:
				break
		if item[0] == BLOCK_START:
			if re.match("\s*?if", item[1]):
				sub_output, input_t = parse(input_t)
				res = sub_output[:-1]
				alt = sub_output[-1]
				new_to_append = [res,alt]
				new_to_append.insert(0, item)
				output.append(new_to_append)
			else: 
				sub_output, input_t = parse(input_t)
				sub_output.insert(0, item)
				output.append(sub_output)
			if len(input_t) == 0:
				break
		if item[0] == BLOCK_ELSE:
			sub_output, input_t = parse(input_t)
			output.append(sub_output)
			return output, input_t
		if item[0] == BLOCK_END:
			return output, input_t
	return output, input_t


# ----------- Main Evaluation ------------- #
def template_compile(parsed_template, context):
	my_HTML = ResultingHTML()
	eval_main(parsed_template, context, my_HTML)
	return my_HTML.value

def eval_main(parsed_template, context, my_HTML):
	with open ('error.txt', 'a') as erfile:
		erfile.write('%s' %parsed_template)
	for item in parsed_template:

		if type(item) is list:
			evaluate_list(item, context, my_HTML)
		elif type(item) is tuple:
			evaluate_node(item, context, my_HTML)


def evaluate_node(node, context, my_HTML):
	with open ('error.txt', 'a') as erfile:
			erfile.write('im in evaluate_node')
	if node[0] == TEXT:
		return my_HTML.update_output(node[1])
	if node[0] == VARIABLE:
		var_value = context.fetch(node[1])
		my_HTML.update_output(var_value)
		return None

def evaluate_list(list_input, context):
	if bool((re.search("for\s.*?\sin", list_input[0][1]))):
		do_for_loop(list_input, context)
	if bool((re.match(".?if", list_input[0][1]))):
		do_conditional(list_input, context)

def do_for_loop(list_input, context):
	head, rest = list_input[0], list_input[1:]
	item_var = re.search("for\s(.*?)\sin\s.*?\s.?", head[1]).group(1)
	copy = item_var
	list_var = re.search("for\s.*?\sin\s(.*?)\s.?", head[1]).group(1)
	for item_var in context.fetch(list_var):
		inner_context = Scope(context, {'%s' %copy: item_var})
		eval_main(rest, inner_context)

def do_conditional(list_input, context):
	head, consequence, alternate = list_input[0], list_input[1], list_input[2]
	condition = head[1]
	condition_array = filter(lambda x: x != '', condition.split(' '))
	condition_array_chop = condition_array[1:]
	condition_string = ''
	for i in range(len(condition_array_chop)):
		if condition_array_chop[i] in context.dictionary:
			condition_array_chop[i] = context.dictionary[condition_array_chop[i]]
	for i in range(len(condition_array_chop)):
		condition_string = condition_string + str(condition_array_chop[i])
	condition_value = eval(condition_string)
	if condition_value:
		return eval_main(consequence, context)
	else:
		return eval_main(alternate, context)