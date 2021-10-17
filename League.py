import pyautogui
import pyperclip

import window

import os
from random import seed
from random import randint
import time

class Reporter:
	def __init__(self, logger, images, cwd):
		self.logger = logger
		self.images = images
		with open(os.path.join(cwd, 'reportText.txt'), encoding='utf8') as file:
			self.reportText = file.read()
		self.teamY = [ 130, 165, 200, 235 ]
		self.enemyY = [ 310, 345, 380, 415, 450 ]

	def findGameModeIcon(self, leagueRegion):
		#self.logger.info(leagueRegion)
		for im in self.images.gameModeIcons:
			#self.logger.info(im)
			icon = pyautogui.locateCenterOnScreen(im, region=leagueRegion, confidence=0.9)
			if icon:
				#self.logger.info(icon)
				self.logger.info("find game mode icon")
				return icon

	def reportTeam(self):
		self.logger.info("report teammates")
		self.report(self.teamY)

	def reportEnemy(self):
		self.logger.info("report enemies")
		self.report(self.enemyY)

	def reportAll(self):
		self.logger.info("report all other players")
		self.reportTeam()
		self.reportEnemy()

	def report(self, targets):
		client = window.LeagueClient()
		client.bringFront()
		leagueIcon = self.findGameModeIcon(client.rect)

		self.logger.info('report() >>>')
		if leagueIcon:
			for y in targets:
				self.reportAPlayer(client.rect, leagueIcon.x, leagueIcon.y + y)
		else:
			self.logger.info('[report] League icon is not found')
		self.logger.info('report() <<<')

	def reportAPlayer(self, leagueRegion, posX, posY):
		pyautogui.moveTo(posX, posY)
			
		for im in self.images.reportButtons:
			reportButton = pyautogui.locateCenterOnScreen(im, region=(posX, posY - 20, 300, 100), confidence=0.8, grayscale=True)
			if reportButton:
				break
		
		if reportButton:
			#pyautogui.moveTo(reportButton)
			pyautogui.mouseDown(reportButton, button='left', duration=1.0)
			pyautogui.mouseUp(reportButton, button='left')
			time.sleep(0.1)

			#locate report check boxes
			checkboxes = list(pyautogui.locateAllOnScreen(self.images.checkbox, region=leagueRegion, confidence=0.7))
			
			if checkboxes:
				# get random numbers
				rn = myRandom()

				# click check boxes
				for i in rn:
					pyautogui.click(checkboxes[i])
			
				# paste report text to comment text field
				commentTextField = pyautogui.locateCenterOnScreen(self.images.commentText, region=leagueRegion)
				if commentTextField:
					pyautogui.click(commentTextField)
					pyperclip.copy(self.reportText)
					pyautogui.hotkey('ctrl','v')

				# cancel report for testing
				# cancel = pyautogui.locateCenterOnScreen(self.images.cancelButton, region=leagueRegion, confidence=0.9)
				# self.logger.info(self.images.cancelButton)
				# self.logger.info(cancel)
				# if cancel:
				# 	pyautogui.click(cancel)
				# 	return

				#press report confirm button
				reportConfirmRetry = 3
				while reportConfirmRetry > 0:
					reportConfirm = pyautogui.locateCenterOnScreen(self.images.reportConfirm, region=leagueRegion)
					if reportConfirm:
						pyautogui.moveTo(reportConfirm)
						pyautogui.click(reportConfirm)
						break
					else:
						self.logger.debug("report confirm button not found, wait for 1 second to retry. %d left" % reportConfirmRetry)
						reportConfirmRetry = reportConfirmRetry - 1
						time.sleep(1)
					pass
			else:
				self.logger.info('checkbox is not detected')
				# cancel report and go on.
				cancel = pyautogui.locateCenterOnScreen(self.images.cancelButton, region=leagueRegion, confidence=0.9)
				if cancel:
					pyautogui.click(cancel)
					return
		else:
			self.logger.debug('[reportAPlayer] report fail')


def myRandom():
	seed(time.time())
	randomNumbers = []
	for i in range(0,3):
		rn = randint(0,6)
		while rn in randomNumbers:
			rn = randint(0,6)
		randomNumbers.append(rn)
	return randomNumbers
