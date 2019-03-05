#!/usr/bin/env python3
"""
Name : Orphan Cleaner
Version : 2.0
Usage :
    ./orphan.py

Descriptions:
    Cleans Orphan Thumbnails in the ~/.thumbnails/normal folder.
    This is used to clean unnecessary thumbnails and free up space
"""

import os, time
import shlex, subprocess
import hashlib

# Functions
def run(cmd):
    '''
    This function takes a string as input and after exexuting it, returns the output text
    of the command.
    '''
    cmd = shlex.split(cmd)
    return subprocess.check_output(cmd).decode('utf-8')

def md5hash(string):
    # Converts input string to md5hash
    string = string.replace('%', '%25')
    string = string.replace(' ', '%20')
    m = hashlib.md5(string.encode('utf-8'))
    return m.hexdigest()

# Get the path of user home
home = os.path.expanduser('~')

# Create a list of thumbnails
print('Listing Thumbnails...')
cmd = 'ls %s/.thumbnails/normal'%home
thumbnails = run(cmd)

thumbs = thumbnails.split('\n')
thumbs.pop()        # remove last blank entry
thumbs = set(thumbs)# set allows faster look up

print('Total Thumbnails =', len(thumbs))

# Find all images files under home directory.
print('Listing PNG images...')
png = run('find %s -not ( -path *thumbnails -prune ) -iname *.png'%home)
images = png.split('\n')
images.pop()

print('Listing other images...')

pic = run("find %s -regex '.*\(jpg\|jpeg\|gif\|mp4\|mkv\|JPG\|GIF\)'"%home)
pics = pic.split('\n')
pics.pop()
images+=pics

print('Total images =', len(images))


# This removes non-orphan thumbnail names from thumbs list.
print('Listing unnecessary thumbnails...')

for each in images:
    path = 'file://'+each
    pathmd5 = md5hash(path)
    thumbname = pathmd5+'.png'
    if thumbname in thumbs:
        thumbs.remove(thumbname)

print('Orphan Thumbnails = ', len(thumbs))
print('........................................')
# Delete orphan thumbnails
confirm = input('Delete all orphan thumbnails ? (y/N): ')
if confirm == 'y':
    for each in thumbs:
        run('rm -f '+home+'/.thumbnails/normal/'+each)
        print(each)
