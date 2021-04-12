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
import tkinter
from tkinter import ttk

###########################################################
# Class definitions:

# new class for storing images like report icons, checkboxes...
class Images:
	# static variables
	checkboxIm = None
	commentTextIm = None
	cancelIm = None
	reportConfirmIm = None
	reportButtonIm = None
	leagueIm = None
	reportText = None

	# load all the static variables
	@staticmethod
	def initialize(cwd):
		Images.checkboxIm = Image.open(cwd + '/image/' + 'checkbox.PNG')
		Images.commentTextIm = Image.open(cwd + '/image/' + 'comment.PNG')
		Images.cancelIm = Image.open(cwd + '/image/' + 'cancel.PNG')
		Images.reportConfirmIm = Image.open(cwd + '/image/' + 'reportConfirm.PNG')
		Images.reportButtonIm = Images.loadImageFromFolder(cwd + '/image/reportIcon')
		Images.leagueIm = Images.loadImageFromFolder(cwd + '/image/AramIcon')
		with open(cwd + '/' + 'reportText.txt', encoding='utf8') as file:
			Images.reportText = file.read()

	# static method that load images from folder.
	@staticmethod 
	def loadImageFromFolder(path):
		files = listdir(path)
		images = []
		for i in files:
			im = Image.open(path + '/' + i)
			images.append(im)
		return images
# end of class Image

# class for storing window rect and handler
class WindowProperty:
	#static variables
	hwnd = None
	rect = None

	# method passed to win32gui
	@staticmethod
	def windowEnumHandler(hwnd, top_windows):
		top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

	# bring league window to the front
	@staticmethod
	def bringFront(hwnd):
		win32gui.ShowWindow(hwnd, 9)
		win32gui.SetForegroundWindow(hwnd)

	# initialize the static variables 
	@staticmethod
	def initialize():
		top_windows = []
		win32gui.EnumWindows(WindowProperty.windowEnumHandler, top_windows)
		for i in top_windows:
			if "league of legend" in i[1].lower():
				DLOG('find window: {}'.format(i[1].lower()))
				WindowProperty.hwnd = i[0]
				r = win32gui.GetWindowRect(i[0])
				WindowProperty.rect = (r[0], r[1], r[2] - r[0], r[3] - r[1])
				break
# end of class WindowProperty

# a class to store y-axis value
class Coordinate:
	teamY = [ 130, 165, 200, 235 ]
	enemyY = [ 310, 345, 380, 415, 450 ]
# end of class Coordinate

# end of Class definitions.
###########################################################

# write log to log file
def DLOG(msg):
	file = open('debuglog.log', 'a')
	file.write(time.strftime('%Y-%m-%d %H:%M:%S -\t', time.localtime()))
	file.write(msg + '\n')
	file.close()
# end of log()

# find league icon within a region, and return the position.
def findLeagueIcon(leaguRegion):
	for im in Images.leagueIm:
		icon = pyautogui.locateCenterOnScreen(im, region=leaguRegion, confidence=0.9)
		if icon:
			#DLOG('[findLeagueIcon] find league icon on window')
			break
	return icon
# end of findLeagueIcon()

# get a list of random numbers 
def myRandom():
	seed(time.time())
	randomNumbers = []
	for i in range(0,3):
		rn = randint(0,6)
		while rn in randomNumbers:
			rn = randint(0,6)
		randomNumbers.append(rn)
	return randomNumbers
# end of myRandom()

###########################################################
# Button functions
def reportTeam():
	WindowProperty.bringFront(WindowProperty.hwnd)
	leagueIcon = findLeagueIcon(WindowProperty.rect)

	DLOG('reportTeam() >>>')
	if leagueIcon:
		for y in Coordinate.teamY:
			reportAPlayer(leagueIcon.x, leagueIcon.y + y)
	else:
		DLOG('[reportTeam] League icon is not found')
	DLOG('reportTeam() <<<')

def reportEnemy():
	WindowProperty.bringFront(WindowProperty.hwnd)
	leaguIcon = findLeagueIcon(WindowProperty.rect)

	DLOG('reportEnemy() >>>')
	if leaguIcon:
		for y in Coordinate.enemyY:
			reportAPlayer(leaguIcon.x, leaguIcon.y + y)
	else:
		DLOG('[reportEnemy] League icon is not found')
	DLOG('reportEnemy() <<<')

def reportAll():
	WindowProperty.bringFront(WindowProperty.hwnd)
	leaguIcon = findLeagueIcon(WindowProperty.rect)

	DLOG('reportAll() >>>')
	ys = Coordinate.teamY + Coordinate.enemyY

	if leaguIcon:
		for y in ys:
			reportAPlayer(leaguIcon.x, leaguIcon.y + y)
	else:
		DLOG('[reportAll] League icon is not found')
	DLOG('reportAll() <<<')

def closeWindow():
	window.destroy()
# end of button functions
###########################################################

def reportAPlayer(posX, posY):
	pyautogui.moveTo(posX, posY)
		
	for im in Images.reportButtonIm:
		reportButton = pyautogui.locateCenterOnScreen(im, region=(posX, posY - 20, 300, 100), confidence=0.8, grayscale=True)
		if reportButton:
			break
	
	if reportButton:
		#pyautogui.moveTo(reportButton)
		pyautogui.mouseDown(reportButton,button='left',duration=1.0)
		pyautogui.mouseUp(reportButton,button='left')

		#locate report check boxes
		checkboxes = list(pyautogui.locateAllOnScreen(Images.checkboxIm, region=WindowProperty.rect, confidence=0.7))
		
		if checkboxes:
			# get random numbers
			rn = myRandom()

			# click check boxes
			for i in rn:
				pyautogui.click(checkboxes[i])
		
			# paste report text to comment text field
			commentTextField = pyautogui.locateCenterOnScreen(Images.commentTextIm, region=WindowProperty.rect)
			if commentTextField:
				pyautogui.click(commentTextField)
				pyperclip.copy(Images.reportText)
				pyautogui.hotkey('ctrl','v')

			# cancel report for testing
			#cancel = pyautogui.locateCenterOnScreen(Images.cancelIm, region=WindowProperty.rect)
			#if cancel:
			#	pyautogui.click(cancel)
			#	return

			# press report confirm button
			reportConfirm = pyautogui.locateCenterOnScreen(Images.reportConfirmIm, region=WindowProperty.rect)
			if reportConfirm:
				pyautogui.moveTo(reportConfirm)
				pyautogui.click(reportConfirm)
		else:
			DLOG('[reportAPlater] checkbox is not detected')
			# cancel report and go on.
			cancel = pyautogui.locateCenterOnScreen(Images.cancelIm, region=WindowProperty.rect)
			if cancel:
				pyautogui.click(cancel)
				return
	else:
		DLOG('[reportAPlayer]report fail')


###########################################################
# main script starts:

# get the current working directory
cwd = os.path.dirname(sys.argv[0]) if os.path.dirname(sys.argv[0]) != "" else "."

# tkinter initialize  
window = tkinter.Tk()
window.title('水水牌檢舉器')
window.configure(background='white')
window.iconbitmap(cwd + "/image/rsc/window_icon.ico")
window.geometry("+1600+700")

top_frame = ttk.Frame(window)
top_frame.pack()
bottom_frame = ttk.Frame(window)
bottom_frame.pack(side=tkinter.BOTTOM)
# end of tkinter initialize

# top frame
left_style = ttk.Style()
left_style.configure('B1.TButton', foreground='green', background='green')
left_button = ttk.Button(top_frame,text='TEAM', style='B1.TButton', command = reportTeam)
left_button.pack(side=tkinter.LEFT)

middle_style = ttk.Style()
middle_style.configure('B2.TButton', foreground='red', background='red')
middle_button = ttk.Button(top_frame,text='ENEMY', style='B2.TButton', command = reportEnemy)
middle_button.pack(side=tkinter.LEFT)

right_style = ttk.Style()
right_style.configure('B3.TButton', foreground='blue', background='blue')
right_button = ttk.Button(top_frame,text='ALL', style='B3.TButton', command = reportAll)
right_button.pack(side=tkinter.LEFT)

# bottom frame
bottom_style = ttk.Style()
bottom_style.configure('B4.TButton', foreground='black')
bottom_button = ttk.Button(text='Exit', style='B4.TButton', command = closeWindow)
bottom_button.pack(side=tkinter.BOTTOM)

# class initialization
Images().initialize(cwd)
WindowProperty().initialize()

window.mainloop()

# main script ends.
###########################################################