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


# variables used in report script
teamY = [ 130, 165, 200, 235 ]
enemyY = [ 310, 345, 380, 415, 450 ]
cwd = os.path.dirname(sys.argv[0]) if os.path.dirname(sys.argv[0]) != "" else "."
debuglog = open('debuglog', 'w')

class PreloadImage:
	def loadFolderImage(path):
		reportIcons = listdir(path)
		images = []
		for i in reportIcons:
			im = Image.open(path + '/' + i)
			images.append(im)

		return images

	def windowEnumerationHandler(hwnd, top_windows):
		top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

	def getWindowHndlr(f):
		top_windows = []
		win32gui.EnumWindows(f, top_windows)
		for i in top_windows:
			if "league of legend" in i[1].lower():
				#win32gui.ShowWindow(i[0], 9)
				#win32gui.SetForegroundWindow(i[0])
				break
		return i[0]

	def getWindowSize(hwnd):
		rect = win32gui.GetWindowRect(hwnd)
		return (rect[0], rect[1], rect[2]-rect[0], rect[3]-rect[1])
	
	def bringFront(hwnd):
		win32gui.ShowWindow(hwnd, 9)
		win32gui.SetForegroundWindow(hwnd)

	checkboxIm = Image.open(cwd + '/image/' + 'checkbox.PNG')
	commentTextIm = Image.open(cwd + '/image/' + 'comment.PNG')
	cancelIm = Image.open(cwd + '/image/' + 'cancel.PNG')
	reportComfirmIm = Image.open(cwd + '/image/' + 'reportConfirm.PNG')
	with open(cwd + '/' + 'reportText.txt', encoding='utf8') as file:
		reportText = file.read()
	reportButtonIms = loadFolderImage(cwd + '/image/reportIcon')
	leaugeIcons = loadFolderImage(cwd + '/image/AramIcon')
	windowHndlr = getWindowHndlr(windowEnumerationHandler)
	windowSize = getWindowSize(windowHndlr)

	
def findLeagueIcon(windowSize):
	for im in PreloadImage.leaugeIcons:
		icon = pyautogui.locateCenterOnScreen(im, region=windowSize, confidence=0.9)
		if icon:
			debuglog.write('find aram\n')
			break
	return icon

# tkinter initialize  
window = tkinter.Tk()
window.title('水水牌檢舉器')
window.configure(background='white')

top_frame = ttk.Frame(window)
top_frame.pack()
bottom_frame = ttk.Frame(window)
bottom_frame.pack(side=tkinter.BOTTOM)
# end of tkinter initialize

# Button functions
def reportTeam():
	PreloadImage.bringFront(PreloadImage.windowHndlr)
	AramIcon = findLeagueIcon(PreloadImage.windowSize)
	ys = teamY

	if AramIcon:
		for y in ys:
			reportAPlayer(AramIcon.x, AramIcon.y + y)
	else:
		debuglog.write('aram not found\n')

def reportEnemy():
	PreloadImage.bringFront(PreloadImage.windowHndlr)
	AramIcon = findLeagueIcon(PreloadImage.windowSize)
	ys = enemyY

	if AramIcon:
		for y in ys:
			reportAPlayer(AramIcon.x, AramIcon.y + y)
	else:
		debuglog.write('aram not found\n')

def reportAll():
	PreloadImage.bringFront(PreloadImage.windowHndlr)
	AramIcon = findLeagueIcon(PreloadImage.windowSize)
	ys = teamY + enemyY

	if AramIcon:
		for y in ys:
			reportAPlayer(AramIcon.x, AramIcon.y + y)
	else:
		debuglog.write('aram not found\n')

def closeWindow():
	window.destroy()

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
		
	for im in PreloadImage.reportButtonIms:
		reportButton = pyautogui.locateCenterOnScreen(im, region=(posX, posY - 20, 300, 100), confidence=0.8, grayscale=True)
		if reportButton:
			break
	
	if reportButton:
		#pyautogui.moveTo(reportButton)
		pyautogui.mouseDown(reportButton,button='left',duration=1.0)
		pyautogui.mouseUp(reportButton,button='left')

		#locate report check boxes
		checkboxes = list(pyautogui.locateAllOnScreen(PreloadImage.checkboxIm, region=PreloadImage.windowSize, confidence=0.7))
		
		#TODO optimize here 
		if checkboxes:
			pass
		else:
			return
		# get random numbers
		rn = myRandom()

		# click check boxes
		for i in rn:
			pyautogui.click(checkboxes[i])

		commentTextField = pyautogui.locateCenterOnScreen(PreloadImage.commentTextIm, region=PreloadImage.windowSize)
		if commentTextField:
			pyautogui.click(commentTextField)
			pyperclip.copy(PreloadImage.reportText)
			pyautogui.hotkey('ctrl','v')

		# cancel report for testing
		#cancel = pyautogui.locateCenterOnScreen(PreloadImage.cancelIm, region=PreloadImage.windowSize)
		#if cancel:
		#	pyautogui.click(cancel)

		reportConfirm = pyautogui.locateCenterOnScreen(PreloadImage.reportComfirmIm, region=PreloadImage.windowSize)
		if reportConfirm:
			pyautogui.moveTo(reportConfirm)
			pyautogui.click(reportConfirm)
	else:
		debuglog.write('report fail\n')
		
		
#################################################
# main script: 

window.mainloop()
debuglog.close()

#################################################
