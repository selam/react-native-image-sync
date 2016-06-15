#!/usr/bin/env

import sys # retrieve sys.args
import getopt
import os
import fnmatch
import shutil

def usage(ld=False):
    if not ld:
        print 'sync-images -i imagename -p /home/user/workspace/projectName'
    else:
        print '''sync-image take image name and destination path from command line
and search this image from current working directory when found the image
it checks directory name contains drawable and ends with hdpi, if it does copy
image into react-native project directory accordingly file requirement

usage:
syny-image -i ic_add_white -p /home/{user}/workspace/your-project

'''.format(user=os.getlogin())
    sys.exit()



try:
     opts, args = getopt.getopt(sys.argv[1:],"hi:p:",["help", "image=","path="])
except getopt.GetoptError as e:
    print 'test.py -i <inputfile> -o <outputfile>', e
    sys.exit(2)


image_name = None
destination_path = None
for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage(ld=True)
    elif opt in ("-i", "--image"):
        image_name = arg
    elif opt in ("-p", "--path"):
        destination_path = arg


if None in (image_name, destination_path):
    usage(ld=False)

if not image_name.endswith('.png'):
   image_name = "{file_name}*.png".format(file_name=image_name,)

if not destination_path.startswith("/"):
    # user gives us a relative path,  into absolute path
    destination_path = "/home/{user}/workspace/{project}".format(user=os.getlogin(), project=destination_path)

for root, dirs, files in os.walk(os.getcwd()):
    file_dir = os.path.basename(root)
    files = fnmatch.filter(files, image_name)
    if "drawable" in file_dir and file_dir.endswith("hdpi"):
        # this file going to android directory
        # check first is directory there?
        destination_dir = os.path.join(destination_path, "android/app/src/main/res", file_dir)
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir, mode=755)
        for fn in files:
            shutil.copyfile(os.path.join(root, fn), os.path.join(destination_dir, fn))
    elif file_dir.endswith("x_ios"):
        # this file going to ios directory
        pass
