import pyautogui
import win32gui

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

def reportAPlayer(posX, posY, leagueWindow):
	pyautogui.moveTo(posX, posY)
	reportIcons = listdir(cwd + "/reportIcon")
		
	for i in reportIcons:
		reportButton = pyautogui.locateCenterOnScreen(cwd + '/reportIcon/' + i, region=(posX, posY - 20, 300, 100))
		if reportButton:
			break
	
	if reportButton:
		pyautogui.moveTo(reportButton)
		#time.sleep(1)
		#pyautogui.click(reportButton,clicks=10,interval=0.5,)
		pyautogui.mouseDown(reportButton,button='left',duration=2.0)
		pyautogui.mouseUp(reportButton,button='left')

		#locate report check boxes
		checkboxes = list(pyautogui.locateAllOnScreen(cwd + '/' + 'checkbox.PNG', region=leagueWindow))
		nl = len(checkboxes)

		# get random numbers
		rn = myRandom()

		# click check boxes
		for i in rn:
			pyautogui.click(checkboxes[i])

		commentText = pyautogui.locateCenterOnScreen(cwd + '/' + 'comment.PNG', region=leagueWindow)
		if commentText:
			pyautogui.click(commentText)
			with open(cwd + '/' + 'reportText.txt', encoding='utf8') as file:
				data = file.read()
			pyperclip.copy(data)
			pyautogui.hotkey('ctrl','v')

		reportConfirm = pyautogui.locateCenterOnScreen(cwd + '/' + 'reportConfirm.PNG', region=leagueWindow)
		if reportConfirm:
			pyautogui.moveTo(reportConfirm)
			#pyautogui.click(reportConfirm)

		# cancel report for testing
		cancel = pyautogui.locateCenterOnScreen('cancel.PNG', region=leagueWindow)
		if cancel:
			pyautogui.click(cancel)


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

leagueWindow = (rect[0], rect[1], rect[2]-rect[0], rect[3]-rect[1])

# locate aram icon
AramIconFiles = listdir(cwd + "/AramIcon")

for i in AramIconFiles:
	AramIcon = pyautogui.locateCenterOnScreen(cwd + '/AramIcon/' + i, region=leagueWindow)
	if AramIcon:
		break

if AramIcon:
	for y in ys:
		reportAPlayer(AramIcon.x, AramIcon.y + y, leagueWindow)

#################################################
