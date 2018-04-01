# Thanks to https://github.com/bmccormack/trello-python-demo/blob/master/demo.py for the inspiration

import requests
from john_settings import trello_key, trello_token, trello_boardlink
from pprint import pprint
import numpy as np

# you can specify your trello key and token in the setting file
key = trello_key
token = trello_token

board_link = trello_boardlink

# else you can input them here
if key is None:
	key = input('Please enter your trello key')

if token is None:
	token = input('Please enter your trello token')

if board_link is None:
	board_link = input("Please enter your board shortlink")

params_key_and_token = {'key': key,'token': token}

base_url = "https://api.trello.com/1/"

# Get all the cards for a particular board
card_response = requests.get(base_url + 'boards/' + board_link + '/cards', params = params_key_and_token)
card_response_array_of_dict = card_response.json()

# Get all the lists for a particular board
list_response = requests.get(base_url + 'boards/' + board_link + '/lists', params = params_key_and_token)
list_response_array_of_dict = list_response.json()

# Get all the actions for a particular board
arguments = {'action_fields' : "data, type"}
action_response = requests.get(base_url + 'boards/' + board_link + '/actions', params = params_key_and_token, data = arguments)
action_response_array_of_dict = action_response.json()

#print("%d lists, %d cards, %d actions" % (len()))
print("%d lists, %d cards, %d actions\n" % (len(list_response_array_of_dict), len(card_response_array_of_dict), len(action_response_array_of_dict)))


# Extract the names of each list into a separate list
lists = list()
for l in list_response_array_of_dict:
	lists.append(l["name"])


'''
# Print out each list and associated card
for c in card_response_array_of_dict:
	lname = ""
	for l in list_response_array_of_dict:
		if c["idList"] == l["id"]:
			lname = l["name"]
	print("%s : %s" % (lname, c["name"]))
'''

num_lists = len(lists)

# We'll create a 2D array to represent all the movements of cards between lists
board_array = np.zeros((num_lists, num_lists), dtype = int)

for c in card_response_array_of_dict: 

	movements = []

	for a in action_response_array_of_dict:
		if a['type'] == 'updateCard':
			if a['data']['card']['shortLink'] == c['shortLink']:
				try: 
					movements.append((a['data']['listBefore']['name'], a['data']['listAfter']['name']))
				except: 
					continue
					#pprint(a)

	#print(movements)

	for bef, aft in movements:
		bef_ind = lists.index(bef)
		aft_ind = lists.index(aft)

		#Update the board array with the list of movements
		board_array[bef_ind][aft_ind] += 1

# Create data in the format that Sankeymatic likes: SOURCE [AMOUNT] DESTINATION
print("Sankeymatic input data:")
for i in range(num_lists):
	for j in range(num_lists):

	# 	Use the line below if you only want to consider forward movements of cards through the lists
	# for j in range(i, num_lists)	
		if board_array[i][j] != 0:
			print(lists[i] + ' [' + str(int(board_array[i][j])) + '] ' + lists[j])


