import pyautogui
import win32gui
from PIL import Image

import time
from random import seed
from random import randint
import pyperclip
import os
import sys
from os import listdir

teamY = [ 130, 165, 200, 235 ]
enemyY = [ 310, 345, 380, 415, 450 ]
cwd = os.path.dirname(sys.argv[0]) if os.path.dirname(sys.argv[0]) != "" else "."
debuglog = open('debuglog', 'w')

class PreloadImage:
	checkboxIm = Image.open(cwd + '/image/' + 'checkbox.PNG')
	commentText = Image.open(cwd + '/image/' + 'comment.PNG')
	cancelIm = Image.open(cwd + '/image/' + 'cancel.PNG')
	reportComfirmIm = Image.open(cwd + '/image/' + 'reportConfirm.PNG')
	with open(cwd + '/' + 'reportText.txt', encoding='utf8') as file:
		data = file.read()
	

def windowEnumerationHandler(hwnd, top_windows):
	top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

def myRandom():
	seed(time.time())
	randomNumbers = []
	for i in range(0,3):
		rn = randint(0,6)
		
		while rn in randomNumbers:
			rn = randint(0,6)

		randomNumbers.append(rn)

	return randomNumbers

def loadFolderImage(path):
	reportIcons = listdir(path)
	images = []
	for i in reportIcons:
		im = Image.open(path + '/' + i)
		images.append(im)

	return images

def reportAPlayer(posX, posY, leagueWindow, reportButtons):
	pyautogui.moveTo(posX, posY)
		
	for im in reportButtons:
		reportButton = pyautogui.locateCenterOnScreen(im, region=(posX, posY - 20, 300, 100))
		if reportButton:
			break
	
	if reportButton:
		#pyautogui.moveTo(reportButton)
		pyautogui.mouseDown(reportButton,button='left',duration=1.0)
		pyautogui.mouseUp(reportButton,button='left')

		#locate report check boxes
		checkboxes = list(pyautogui.locateAllOnScreen(PreloadImage.checkboxIm, region=leagueWindow, confidence=0.9))
		nl = len(checkboxes)

		# get random numbers
		rn = myRandom()

		# click check boxes
		for i in rn:
			pyautogui.click(checkboxes[i])

		commentText = pyautogui.locateCenterOnScreen(PreloadImage.commentText, region=leagueWindow)
		if commentText:
			pyautogui.click(commentText)
			pyperclip.copy(PreloadImage.data)
			pyautogui.hotkey('ctrl','v')

		# cancel report for testing
		#cancel = pyautogui.locateCenterOnScreen(PreloadImage.cancelIm, region=leagueWindow)
		#if cancel:
		#	pyautogui.click(cancel)

		reportConfirm = pyautogui.locateCenterOnScreen(PreloadImage.reportComfirmIm, region=leagueWindow)
		if reportConfirm:
			pyautogui.moveTo(reportConfirm)
			pyautogui.click(reportConfirm)
	else:
		debuglog.write('report fail\n')
		
		
#################################################
# main script: 

# bring league to the front 
if __name__ == "__main__":
	results = []
	top_windows = []
	win32gui.EnumWindows(windowEnumerationHandler, top_windows)
	for i in top_windows:
		if "league of legend" in i[1].lower():
			win32gui.ShowWindow(i[0], 9)
			win32gui.SetForegroundWindow(i[0])
			rect = win32gui.GetWindowRect(i[0])
			break

# get argument to know how to report
if len(sys.argv) > 1:
	reportee = sys.argv[1]
	if reportee == "ALL":
		ys = teamY + enemyY
	elif reportee == "TEAM":
		ys = teamY
	elif reportee == "ENEMY":
		ys = enemyY
else:
	ys = enemyY

# get league window position and size
leagueWindow = (rect[0], rect[1], rect[2]-rect[0], rect[3]-rect[1])

# preload images 
reportButtons = loadFolderImage(cwd + '/image/reportIcon')
LeaugeIcons = loadFolderImage(cwd + '/image/AramIcon')

# locate Aram or NG icon
for im in LeaugeIcons:
	AramIcon = pyautogui.locateCenterOnScreen(im, region=leagueWindow, confidence=0.9)
	if AramIcon:
		debuglog.write('find aram\n')
		break

if AramIcon:
	for y in ys:
		reportAPlayer(AramIcon.x, AramIcon.y + y, leagueWindow, reportButtons)
else:
	debuglog.write('aram not found\n')

debuglog.close()
#################################################
