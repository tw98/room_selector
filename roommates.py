#!/usr/bin/env python
# Author Tom Wallenstein

import csv
import random
import time
from PIL import Image, ImageFont, ImageDraw
from subprocess import Popen
import os
import glob
from pathlib import Path
import webbrowser
import pandas
import math

def get_player_info(info_file, pic_folder_path):
	players = {}
	with open(info_file, mode='r') as csv_file:
		reader = csv.DictReader(csv_file)

		for row in reader:
			key = f'{row["lastName"]}_{row["firstName"]}'
			
			if row['status'] == 'squad':
				players[key] = row
				players[key]['picture'] = pic_folder_path + players[key]['picture']

	return players


def print_rooms(assignments):
	print('---- ROOM ASSIGNMENTS ----')
	for room in assignments:
		names = [f"{p['firstName']} {p['lastName']}" for p in room]
		print(', '.join(names))
		print('-----')
	return


def get_random_roommates(players, room_cap):
	room_mates = []
	for i in range(room_cap):
		random_player = random.choice(players)
		room_mates.append(random_player)
		players.remove(random_player)

		if len(players) == 0:
			break
	return players, room_mates


def get_room_assignments(rooms, player_dict):
	room_assignments = []

	r_caps = sorted(rooms.keys(), reverse=True)
	players = list(player_dict.values())

	for cap in r_caps:
		while(rooms[cap] != 0):
			players, room = get_random_roommates(players, int(cap))
			rooms[cap] -= 1
			room_assignments.append(room)

			if len(players) == 0:
				break

	return room_assignments

def create_image(img_paths, names):
	canvas_width, canvas_height = 2560, 1600
	new_im = Image.new('RGB', (canvas_width, canvas_height), 'black')
	
	max_imgs_in_row = 4
	n_imgs = len(img_paths)

	if n_imgs <= max_imgs_in_row:
		box_width = canvas_width // n_imgs
		box_height = canvas_height
	else: 
		box_width = canvas_width // max_imgs_in_row
		
		n_rows = math.ceil(n_imgs // max_imgs_in_row)
		box_height = canvas_height // n_rows

	padding_sides = 10
	padding_top = 30
	dist_text = 30

	img_size = min([box_width-(padding_sides*2), box_height])

	draw = ImageDraw.Draw(new_im)
	font = ImageFont.truetype("~/Library/Fonts/Arial.ttf", 72)
	text = "Test"
	text_width, text_height = draw.textsize(text, font)

	h_img_txt = img_size + dist_text + text_height
	padding_top = (box_height - h_img_txt) // 2
	
	images = [Image.open(path) for path in img_paths]

	for i, im in enumerate(images):
		im = im.resize((img_size, img_size))

		row = i // max_imgs_in_row
		col = i % max_imgs_in_row

		x = col * box_width + padding_sides
		y = row * box_height + padding_top

		new_im.paste(im, (x, y))

		draw = ImageDraw.Draw(new_im)
		text = names[i]
		text_width, text_height = draw.textsize(text, font)
		color = (255, 255, 255)
		x_pos = col * box_width + ((box_width - text_width) // 2)
		y_pos = row * box_height + padding_top + img_size + dist_text
		draw.text((x_pos, y_pos), text, color, font=font)

	return new_im


def show_rooms(room_assignments, main_folder, start_wait, transition_time):
	home = Path('.')
	wait = Image.new('RGBA', (2560, 1600), 'black')
	wait.save("./temp/wait.png")

	webbrowser.open("file://" + str(home.resolve()) + "/temp/wait.png")
	time.sleep(start_wait)

	for room in room_assignments:
		imgs = [player['picture'] for player in room]
		names = [player['nickname'] for player in room]
		outfile = '_'.join([player['lastName'] for player in room])
		
		img = create_image(imgs, names)

		saveName = "./temp/"+outfile+".png"
		img.save(saveName)
		
		webbrowser.open_new_tab("file://" + str(home.resolve()) + saveName[1:])
		time.sleep(transition_time)


def clean_up():
	# Get a list of all the file paths that ends with .txt from in specified directory
	fileList = glob.glob('./temp/*.png')
	# Iterate over the list of filepaths & remove each file.
	for filePath in fileList:
	    try:
	        os.remove(filePath)
	    except:
	        print("Error while deleting file : ", filePath)


def get_room_configurations():
	quit_signal = False
	rooms = {}

	while(not quit_signal):
		print('-- NEW ROOM CONFIGURATION --')
		print('Room Size (# of people): ')
		cap = input()
		print('Number of Rooms: ')
		num = input()

		rooms[cap] = int(num)

		while(True):
			print('*******')
			print('Press [n] to enter another room configuration')
			print('Press [d] to continue with room assignments')
			print('Press [q] to quit programm')
		
			key = input()
			if key == 'd':
				quit_signal = True
				break
			elif key == 'n':
				break
			elif key == 'q':
				exit()
			else:
				print('Invalid Input! Try again!')

	return rooms

# main function
def main():
	main_folder = './'
	# get number and sizes of rooms
	rooms = get_room_configurations()
	# get roster of players
	squad = get_player_info(info_file='squad.csv', pic_folder_path=main_folder + 'pics/')

	room_assignments = get_room_assignments(rooms, squad)

	show_rooms(room_assignments, main_folder=main_folder, start_wait=3, transition_time=5)

	print_rooms(room_assignments)
	clean_up()
		

if __name__ == '__main__':
	main()






