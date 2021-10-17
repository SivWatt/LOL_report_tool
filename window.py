import win32gui

def windowEnumHandler(hwnd, top_windows):
	top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

# class for storing window cordinate, size and handler
class WindowProperty:
	def __init__(self, name):
		topWindows = []
		self.windows = []
		win32gui.EnumWindows(windowEnumHandler, topWindows)
		for i in topWindows:
			if name == i[1].lower():
				r = win32gui.GetWindowRect(i[0])
				self.windows.append((i[0], (r[0], r[1], r[2] - r[0], r[3] - r[1])))
				self.hwnd = i[0]
				self.rect = (r[0], r[1], r[2] - r[0], r[3] - r[1])

	# bring window to front
	def bringFront(self):
		win32gui.ShowWindow(self.hwnd, 9)
		win32gui.SetForegroundWindow(self.hwnd)

# end of class WindowProperty

# class for locating league client window
class LeagueClient(WindowProperty):
	# for unknown reasons, always gets 2 windows
	# , and one of it is not visible
	def __init__(self):
		super().__init__('league of legends')	
		for i in self.windows:
			if i[1][2] >= 1024 and i[1][3] >= 576:
				self.hwnd = i[0]
				self.rect = i[1]
				break

	# NOTES: issue when client window is minimized
	# if client is minimized
	# elif w[1][0] == -32000 and w[1][1] == -32000:
	#	client.hwnd = w[0]
	#	client.rect = w[1]
	#	WindowProperty.bringFront(client.hwnd)
	#	break

# end of LeagueClientWindow

# class for locating league game window
class LeagueGame(WindowProperty):
	def __init__(self):
		super().__init__('league of legends (tm) client')

# end of LeagueGameWindow