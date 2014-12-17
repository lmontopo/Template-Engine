import chapeau
import engine

arguments = {}

def first(request, client):
	print "I made it here"
	print request
	chapeau.render(client, 'to_do.html', arguments)


routing_dict = {'/home': 'home.html',
				'/home_post': first}


chapeau.go(routing_dict)

