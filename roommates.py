#!/usr/bin/env python


# Author Tom Wallenstein

import csv
import random
import time
from PIL import Image, ImageFont, ImageDraw
from subprocess import Popen
import os
import glob

def getDataFromCSV(file):
	data = []
	with open(file, mode='r') as csv_file:
	    reader = csv.DictReader(csv_file)
	    for row in reader:
	    	data.append(row)
    	
	return data

def printRooms(data):
	print('---- ROOM ASSIGNMENTS ----')
	for element in data:
		print(element)
	return


def getImageRoom2(path1, path2, name1, name2):	
	image_width = 1100
	image_height = 1100 

	# print('Path1 :' + path1)
	# print('Path2 :' + path2)
	try:

   		img1  = Image.open(path1) 
   		width, height = img1.size 
		# print("image1 opening successful")
   		if (width != image_width and height != image_height):
   			img1 = img1.resize((image_width, image_height)) 

	except IOError: 
		pass

	try:  
   		img2  = Image.open(path2) 
   		width, height = img2.size 
   		# print("image2 opening successful")
   		if (width != image_width and height != image_height):
   			img2 = img2.resize((image_width, image_height)) 
	
	except IOError: 
		pass

	w = 2560
	h = 1600
	padding_side = (w/2 - image_width) / 2
	padding_top = (h - image_height) / 2

	endImg = Image.new('RGBA', (2560, 1600), 'black')
	endImg.paste(img1, (padding_side, padding_top))
	endImg.paste(img2, (w/2+padding_side, padding_top))

	draw = ImageDraw.Draw(endImg)
	font = ImageFont.truetype("~/Library/Fonts/Arial.ttf", 160)

	if (name1 == 'Hot Aldo'):
		draw.text((350, 110) , name1,(255,0,0), font=font)

	# draw = ImageDraw.Draw(endImg)
	# font = ImageFont.truetype("~/Library/Fonts/Arial.ttf", 36)
	if (name2 == 'Hot Aldo'):
		draw.text((1600, 1150),name2,(255,0,0), font=font)

	return endImg

def getImageRoom3(path1, path2, path3, name1, name2, name3):	
	image_width = 800
	image_height = 800 

	try:  
   		img1  = Image.open(path1) 
   		width, height = img1.size 

   		if (width != image_width and height != image_height):
   			img1 = img1.resize((image_width, image_height)) 

	except IOError: 
		pass

	try:  
   		img2  = Image.open(path2) 
   		width, height = img2.size 

   		if (width != image_width and height != image_height):
   			img2 = img2.resize((image_width, image_height)) 
	
	except IOError: 
		pass

	try:  
   		img3  = Image.open(path3) 
   		width, height = img3.size 

   		if (width != image_width and height != image_height):
   			img3 = img3.resize((image_width, image_height)) 
	
	except IOError: 
		pass

	w = 2560
	h = 1600
	padding_side = (w - 3 * image_width) / 6
	padding_top = (h - image_height) / 2

	endImg = Image.new('RGBA', (2560, 1600), 'black')
	endImg.paste(img1, (padding_side, padding_top))
	endImg.paste(img2, (image_width + 3 * padding_side, padding_top))
	endImg.paste(img3, (2 * image_width + 5 * padding_side, padding_top))

	draw = ImageDraw.Draw(endImg)
	font = ImageFont.truetype("~/Library/Fonts/Arial.ttf", 36)

	if (name1 == 'Hot Aldo'):
		draw.text((133, 480) , name1,(255,255,255), font=font)

	# draw = ImageDraw.Draw(endImg)
	# font = ImageFont.truetype("~/Library/Fonts/Arial.ttf", 36)
	if (name2 == 'Hot Aldo'):
		draw.text((420, 480),name2,(255,255,255), font=font)

	# draw = ImageDraw.Draw(endImg)
	# font = ImageFont.truetype("~/Library/Fonts/Arial.ttf", 36)
	
	if (name3 == 'Hot Aldo'):
		draw.text((760, 480),name3,(255,255,255), font=font)

	return endImg


squad = getDataFromCSV('squad.txt')
num_Players = len(squad)

nicknames = getDataFromCSV('nicknames.txt')

# print "Squad"
# for row in squad:
# 	   	print(row)

# print "Nicknames"
# for row in nicknames:
# 	   	print(row)

room_assignments = []

while (squad != []):
	if (len(squad) != 3):
		first = random.choice(squad)
		second = random.choice(squad)

		while (first == second):
			second = random.choice(squad)

		room_assignments.append([first["lastName"], second["lastName"]])
		squad.remove(first)
		squad.remove(second)
	else:
		first = random.choice(squad)
		second = random.choice(squad)
		third = random.choice(squad)

		while (first == second):
			second = random.choice(squad)
		while (first == third or second == third):
			third = random.choice(squad)

		room_assignments.append([first["lastName"], second["lastName"], third["lastName"]])
		squad.remove(first)
		squad.remove(second)
		squad.remove(third)

# print(room_assignments)

path_application = '/Applications/Preview.app'


wait = Image.new('RGBA', (2560, 1600), 'black')
wait.save("./temp/wait.png")
p = Popen(['open', path_application, "./temp/wait.png"])
time.sleep(6)
	
p.terminate()
p.kill()
# raw_input("Press Enter to continue...")

for room in room_assignments:
	if len(room) == 2:
		img1_path = "./pics/" + room[0] + ".jpg"
		img2_path = "./pics/" + room[1] + ".jpg"
		
		nickname1 = filter(lambda x: x["name"] == room[0], nicknames)[0]["nickname"]
		nickname2 = filter(lambda x: x["name"] == room[1], nicknames)[0]["nickname"]

		
		# print('path1 ' + img1_path)
		# print('path2 ' + img2_path)
		img = getImageRoom2(img1_path, img2_path, nickname1, nickname2)

		saveName = "./temp/"+room[0]+room[1]+".png"
		img.save(saveName)
	else:
		img1_path = "./pics/" + room[0] + ".jpg"
		img2_path = "./pics/" + room[1] + ".jpg"
		img3_path = "./pics/" + room[2] + ".jpg"

		# print('path1 ' + img1_path)
		# print('path2 ' + img2_path)
		# print('path3 ' + img3_path)

		nickname1 = filter(lambda x: x["name"] == room[0], nicknames)[0]["nickname"]
		nickname2 = filter(lambda x: x["name"] == room[1], nicknames)[0]["nickname"]
		nickname3 = filter(lambda x: x["name"] == room[2], nicknames)[0]["nickname"]

		img = getImageRoom3(img1_path, img2_path, img3_path, nickname1, nickname2, nickname3)

		saveName = "./temp/"+room[0]+room[1]+room[2]+".png"
		img.save(saveName)

	p = Popen(['open', path_application, saveName])
	time.sleep(12)
	# raw_input("Press Enter to continue...")
	
	# p.terminate()
	# p.kill()
	# time.sleep(1)

printRooms(room_assignments)

# Get a list of all the file paths that ends with .txt from in specified directory
fileList = glob.glob('./temp/*.png')
# Iterate over the list of filepaths & remove each file.
for filePath in fileList:
    try:
        os.remove(filePath)
    except:
        print("Error while deleting file : ", filePath)






