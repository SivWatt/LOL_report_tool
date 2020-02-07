import pyautogui
import time
import win32gui
from random import seed
from random import randint
import pyperclip
import os
from os import listdir
from os.path import isfile, isdir, join

teamY = [ 130, 165, 200, 235 ]
enemyY = [ 310, 345, 380, 415, 450 ]


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

def reportAPlayer(posX, posY):
	pyautogui.moveTo(posX, posY)
	#reportButton = pyautogui.locateCenterOnScreen('./reportIcon/report4.PNG')
	
	cwd = os.path.abspath(os.getcwd())
	#print(cwd)
	reportIcons = listdir(cwd + "/reportIcon")
		
	for i in reportIcons:
		reportButton = pyautogui.locateCenterOnScreen(cwd + '/reportIcon/' + i)
		if reportButton:
			break
	
	if reportButton:
		print(reportButton)
		pyautogui.moveTo(reportButton)
		# bring league to the front 
		if __name__ == "__main__":
			results = []
			top_windows = []
			win32gui.EnumWindows(windowEnumerationHandler, top_windows)
			for i in top_windows:
				if "league of legend" in i[1].lower():
					print(i) 
					win32gui.ShowWindow(i[0], 5)
					win32gui.SetForegroundWindow(i[0])
					break
		time.sleep(1)
		#pyautogui.click(reportButton,clicks=10,interval=0.5,)
		pyautogui.mouseDown(reportButton,button='left',duration=2.0)
		pyautogui.mouseUp(reportButton,button='left')

		#locate report check boxes
		checkboxes = list(pyautogui.locateAllOnScreen('checkbox.PNG'))
		nl = len(checkboxes)
		print(nl)

		# get random numbers
		rn = myRandom()

		print(rn)

		# click check boxes
		for i in rn:
			pyautogui.click(checkboxes[i])

		commentText = pyautogui.locateCenterOnScreen('comment.PNG')
		if commentText:
			pyautogui.click(commentText)
			#pyautogui.typewrite("asjadlasdk")
			pyperclip.copy('外掛')
			pyautogui.hotkey('ctrl','v')

		reportConfirm = pyautogui.locateCenterOnScreen('reportConfirm.PNG')
		if reportConfirm:
			pyautogui.moveTo(reportConfirm)
			pyautogui.click(reportConfirm)

		#cancel = pyautogui.locateCenterOnScreen('cancel.PNG')
		#if cancel:
		#	pyautogui.click(cancel)

	else:
		print("not found")

#################################################
# main script: 

# locate aram icon
cwd = os.path.abspath(os.getcwd())
AramIconFiles = listdir(cwd + "/AramIcon")

for i in AramIconFiles:
	AramIcon = pyautogui.locateCenterOnScreen(cwd + '/AramIcon/' + i)
	if AramIcon:
		break

if AramIcon:
	#print(AramIcon)
	#y = 130
	ys = enemyY

	for y in ys:
		reportAPlayer(AramIcon.x, AramIcon.y + y)

	#reportAPlayer(AramIcon.x, AramIcon.y + 130)
	#reportAPlayer(AramIcon.x, AramIcon.y + 165)
	#reportAPlayer(AramIcon.x, AramIcon.y + 200)
	#reportAPlayer(AramIcon.x, AramIcon.y + 235)
	#reportAPlayer(AramIcon.x, AramIcon.y + 310)
	#reportAPlayer(AramIcon.x, AramIcon.y + 345)
	#reportAPlayer(AramIcon.x, AramIcon.y + 380)
	#reportAPlayer(AramIcon.x, AramIcon.y + 415)
	#reportAPlayer(AramIcon.x, AramIcon.y + 450)
else:
	print("Aram Icon not found")





#################################################