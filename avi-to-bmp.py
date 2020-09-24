import cv2
import os
import progressbar as pbar
from argparse import ArgumentParser

version="1.0.0"

def yn(question):
	while True: 
		query = input(question + '[y/N]') 
		Fl = query[0].lower() 
		
		if Fl in ['y','n']:
			return Fl == 'y' 
		print('Please answer with yes or no.') 

def ask(question):
	while True:
		answer = input(question)
		return answer


parser = ArgumentParser(
	description="A simple script for decode .avi file to .bmp files.",
	epilog="version 1.0.0. Created by crescendoCat."
)
parser.add_argument("file", help="a .avi file to parse")
parser.add_argument("folder", nargs='?', default='',help="the folder where bmp will put. If not exist, it will create one for you")
parser.add_argument("-v", "--version", action="version", version='%s' % version)
args = parser.parse_args()

if not os.path.exists(args.file):
	print("[ERROR] File %s not exitsts." % args.file)
	exit()

useDefaultFolder = args.folder == ''
defaultFolder = os.path.splitext(args.file)[0]

if useDefaultFolder:
	answer = ask('Where do you want to put your bmp file into? (default is %s)' % defaultFolder)
	if answer == '':
		os.mkdir(defaultFolder)
		args.folder = defaultFolder 
	else:
		args.folder = answer


while not os.path.exists(args.folder) :
	print("[ERROR] Folder %s not exitsts." % args.folder)
	if yn('Do you want to create folder %s?' % args.folder) is True:
		os.mkdir(args.folder)
	else:
		answer = ask('Where do you want to put your bmp file into? (default is %s)' % defaultFolder)
		if answer == '':
			os.mkdir(defaultFolder)
			args.folder = defaultFolder 
		else:
			args.folder = answer

print( "[INFO] Dumping file into %s." % args.folder)
vidcap = cv2.VideoCapture(args.file)
length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
print( "[INFO] frame count %d" % length )
success,image = vidcap.read()
count = 0

widgets = ['Transform: ', pbar.Percentage(), ' ', pbar.Bar('#'), ' ', pbar.Timer(), ' ', pbar.ETA(), ' ']
progress = pbar.ProgressBar(widgets=widgets)
for i in progress(range(length)):
    cv2.imwrite(args.folder +"/frame%d.bmp" % count, image)     # save frame as JPEG file      
    success,image = vidcap.read()
    #print( 'Frame %d read %s ' % (count, "successed" if success else "failed"))
    count += 1
    