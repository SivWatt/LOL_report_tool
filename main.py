import images
import league

import logging
import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

# GUI implement via tkinter
class Application(tk.Frame):
	def __init__(self):
		self.cwd = os.path.dirname(sys.argv[0]) if os.path.dirname(sys.argv[0]) != "" else "."

		# images
		self.images = images.MatchingImages(self.cwd)

		# logger
		logging.basicConfig(
			filename='debuglog.log', 
			level=logging.INFO,
			format='%(asctime)s - [%(process)s] [%(levelname)s] %(message)s [%(pathname)s:%(lineno)d]',
			datefmt='%Y-%m-%d %H:%M:%S'
		)
		self.logger = logging.getLogger()

		# reporter 
		self.reporter = league.Reporter(self.logger, self.images, self.cwd)

		# UI
		window = tk.Tk()
		super().__init__(window)
		self.master = window
		window.title('水水牌檢舉器')
		window.iconbitmap(os.path.join(self.cwd, 'image', 'rsc', 'window_icon.ico'))
		window.configure(background='white')
		window.geometry("+1600+700")

		topFrame = ttk.Frame(window)
		topFrame.pack()
		botFrame = ttk.Frame(window)
		botFrame.pack(side=tk.BOTTOM)

		# top frame
		teamStyle = ttk.Style()
		teamStyle.configure('Team.TButton', foreground='green', background='green')
		teamButton = ttk.Button(topFrame, text='TEAM', style='Team.TButton', command=self.team)
		teamButton.pack(side=tk.LEFT)

		enemyStyle = ttk.Style()
		enemyStyle.configure('Enemy.TButton', foreground='red', background='red')
		enemyButton = ttk.Button(topFrame, text='ENEMY', style='Enemy.TButton', command=self.enemy)
		enemyButton.pack(side=tk.LEFT)

		allStyle = ttk.Style()
		allStyle.configure('All.TButton', foreground='blue', background='blue')
		allButton = ttk.Button(topFrame, text='ALL', style='All.TButton', command=self.all)
		allButton.pack(side=tk.LEFT)

		# bottom frame
		exitStyle = ttk.Style()
		exitStyle.configure('Exit.TButton', foreground='black')
		exitButton = ttk.Button(botFrame, text='Exit', style='Exit.TButton', command=self.master.destroy)
		exitButton.pack(side=tk.LEFT)

		self.pack()

	def testT(self):
		self.logger.info("test button click")

	def team(self):
		self.reporter.reportTeam()

	def enemy(self):
		self.reporter.reportEnemy()

	def all(self):
		self.reporter.reportAll()

# main script
if __name__ == '__main__':
	app = Application()
	app.mainloop()
