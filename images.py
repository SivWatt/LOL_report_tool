from PIL import Image
import os
from os import listdir

# class for storing images
class MatchingImages:
	def __init__(self, cwd):
		path = os.path.join(cwd, 'image')
		self.checkbox			= Image.open(os.path.join(path, 'checkbox.PNG'))
		self.commentText		= Image.open(os.path.join(path, 'comment.PNG'))
		self.cancelButton		= Image.open(os.path.join(path, 'cancel.PNG'))
		self.reportConfirm		= Image.open(os.path.join(path, 'reportConfirm.PNG'))
		self.reportButtons		= MatchingImages.loadImageFromFolder(os.path.join(path, 'reportIcon'))
		self.gameModeIcons		= MatchingImages.loadImageFromFolder(os.path.join(path, 'GameModeIcon'))

	@staticmethod
	def loadImageFromFolder(path):
		files = listdir(path)
		images = []
		for i in files:
			im = Image.open(os.path.join(path, i))
			images.append(im)
		return images
