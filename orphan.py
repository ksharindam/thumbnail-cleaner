#!/usr/bin/python3
"""
Name : Orphan Cleaner
Version : 0.1
Usage : Cleaning of unnecessary orphan thumbnails from ~/.local/share/icons folder

Modules Used : 
subprocess(to execute unix command),
shlex(to process the command),
hashlib(to calculate md5hash),
environ(to get home dir name)

Functions used : run(cmd), md5hash(string)
Descriptions: Only thumbnails of jpg,gif and nonhidden png files will be kept.
Thumbnails in the ~/.thumbnails/normal folder will be cleaned.
"""

# Import Modules
import subprocess
import shlex
import hashlib
from os import environ

# Functions
def run(cmd):
	'''
	This function takes a string as input and after exexuting it, returns the output text of the command.
	'''
	cmd = shlex.split(cmd)
	return subprocess.check_output(cmd).decode('ascii')

def md5hash(string):
	# Converts input string to md5hash
	m = hashlib.md5()
	m.update(string.encode('utf-8'))
	return m.hexdigest()

# Get the path of user home
home = environ['HOME']

# Create a list of thumbnails
cmd = 'ls '+home+'/.thumbnails/normal'
thumbnails = run(cmd)

thumbs = thumbnails.split('\n')
thumbs.pop()
total = len(thumbs)

# Find all images files under home directory.
images = run('find '+home+' -name *.jpg')
images = images.split('\n')
images.pop()

gif = run('find '+home+' -name *.gif')
gifs = gif.split('\n')
gifs.pop()
for each in gifs:
	images.append(each)

png = run('find '+home+' -name *.png')
pngs = png.split('\n')
pngs.pop()
for each in pngs:
	if each.startswith('/home/pi/.') is False:# This excludes hidden directories
		images.append(each)

# This removes nonorphan thumbnail names from thumbs list.
for each in images:
	path = 'file://'+each
	pathmd5 = md5hash(path)
	thumbname = pathmd5+'.png'
	if thumbname in thumbs:
		thumbs.remove(thumbname)

print('Total images =', len(images))
print('Total Thumbnails =', total)
print('Orphan Thumbnails = ', len(thumbs))
print('........................................')
# Delete orphan thumbnails
print(len(thumbs), ' thumbnails will be deleted')
print('Do you want to continue?')
confirm = input('Press Enter to continue or any_letter+enter to cancel: ')
if confirm == '':
	for each in thumbs:
		run('rm -f '+home+'/.thumbnails/normal/'+each)
#		print(each)
