"""This version will have each node represented by a class.  Each node type will have a make 
scope method which will either make a new scope or not.  If a new scope is made, then the 
nodes within it are children of the node that made the scope.  Each node type will also have an
associated method to 'process' that node."""


import re
import sys

VARIABLE    = "VARIABLE"
TEXT		= "TEXT"


class _Node(object):
	def __init__(self, token=None):
		self.children = []
		self.creates_scope = False
		self.process_token(token)

	def process_token(self, token):
		pass

	def enter_scope(self):
		pass

	def render(self, context):
		pass

	def exit_scope(self):
		pass

	def render_children(self, context):
		if len(self.children) > 0:
			return child.render(context)


class _Variable(_Node):
	def process_token(self, token):
		self.name = token

	def render(self, context):
		return self.context[self.name]


class _Text(_Node):
	def render(self, context):
		return self.token


