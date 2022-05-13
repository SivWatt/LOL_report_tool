import pyautogui
import pyperclip

import window

import os
from random import seed
from random import randint
import time

# client window size 
# 1024 x 576
# 1280 x 720 -- currently used
# 1600 x 900

class Reporter:
	def __init__(self, logger, images, cwd):
		self.logger = logger
		self.images = images
		with open(os.path.join(cwd, 'reportText.txt'), encoding='utf8') as file:
			self.reportText = file.read()

		self.cancel_1280_720 = pyautogui.Point(820, 88)
		self.team_1280_720 = [	
								pyautogui.Point(280, 150), 
								pyautogui.Point(280, 190), 
								pyautogui.Point(280, 230), 
								pyautogui.Point(280, 270), 
								pyautogui.Point(280, 310), 
							 ]
		self.enemy_1280_720 = [	
								pyautogui.Point(280, 395), 
								pyautogui.Point(280, 435), 
								pyautogui.Point(280, 475), 
								pyautogui.Point(280, 515), 
								pyautogui.Point(280, 555), 
							 ]

	def reportTeam(self):
		self.logger.info("report teammates")
		client = window.LeagueClient()
		clientSize = client.getSize()
		client.bringFront()

		if clientSize == (1280, 720):
			self.report(client, self.team_1280_720)
		else:
			self.logger.warning("not supported window size: %s", clientSize)

	def reportEnemy(self):
		self.logger.info("report enemies")
		client = window.LeagueClient()
		clientSize = client.getSize()
		client.bringFront()

		if clientSize == (1280, 720):
			self.report(client, self.enemy_1280_720)
		else:
			self.logger.warning("not supported window size: %s", clientSize)

	def reportAll(self):
		self.logger.info("report all other players")
		self.reportTeam()
		self.reportEnemy()

	def report(self, client, targets):
		self.logger.info('report() >>>')
		self.logger.info("client: %s", client.rect)
		for point in targets:
			self.reportAPlayer(client.rect, point)
		self.logger.info('report() <<<')

	def reportAPlayer(self, leagueRegion, point):
		# move directly to the report button
		reportPoint = pyautogui.Point(leagueRegion[0] + point.x, leagueRegion[1] + point.y + 20)
		self.logger.info("move mouse to report button: %s", reportPoint)

		pyautogui.moveTo(reportPoint)
		pyautogui.mouseDown(reportPoint, button='left', duration=1.0)
		pyautogui.mouseUp(reportPoint, button='left')
		
		self.logger.info("locate check boxes")
		# locate report check boxes
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
			# cancel = pyautogui.Point(self.cancel_1280_720.x + leagueRegion[0], self.cancel_1280_720.y + leagueRegion[1])
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
			cancel = pyautogui.Point(self.cancel_1280_720.x + leagueRegion[0], self.cancel_1280_720.y + leagueRegion[1])
			pyautogui.click(cancel)

def myRandom():
	seed(time.time())
	randomNumbers = []
	for i in range(0,3):
		rn = randint(0,6)
		while rn in randomNumbers:
			rn = randint(0,6)
		randomNumbers.append(rn)
	return randomNumbers
