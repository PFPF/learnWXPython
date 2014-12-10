#! /usr/bin/evn python

import wx
import time
import os
from random import randint, choice

btnNum = 0
btnRemaining = 0
events = {wx.EVT_BUTTON:"left", wx.EVT_RIGHT_UP:"right"} # after realized that some people don't have middle button
def mkdir(path): # if the directory do not exist, create it
	dir = os.path.dirname(path)
	if not os.path.exists(dir):	os.makedirs(dir)

class TenButtonFrame(wx.Frame):
	def __init__(self, parent = None):
		wx.Frame.__init__(self, parent, wx.ID_ANY, "Ten Button Race!!!", size=(600,600)) # initialize the frame
		
		self.panel = wx.Panel(self) # create a panel
		self.question = wx.StaticText(self.panel, label="How many buttons do you want? Default is 10.\n\nN<=0 is the endless mode.", pos=(40, 10))
		self.inputBox = wx.TextCtrl(self.panel, pos=(200, 80)) # an input-box
		
		self.start = wx.Button(self.panel, label="START!", pos=(250,250)) # the start button
		self.btn = wx.Button(self.panel, pos=(randint(1,450), randint(1,450)), size=(randint(10,50),randint(10,50))) # create the button
		self.prompt = wx.StaticText(self.panel, label="Your next click should be: left button") # Show the next click
		self.clear = wx.Button(self.panel, label="   Clear the record   ", pos=(225,300))
		self.restart = wx.Button(self.panel, label="Restart", pos=(250,250))
		self.end = wx.StaticText(self.panel, label = "Default Label")
		
		self.start.Bind(wx.EVT_BUTTON, self.OnStart) # bind the start button's event
		self.btn.Bind(wx.EVT_BUTTON, self.OnBTN) # bind the racing button's event
		self.btn.Bind(wx.EVT_KEY_DOWN, self.OnCheat) # see if the user cheats by pressing keys
		self.clear.Bind(wx.EVT_BUTTON, self.OnClear) # bind the clear-record button
		self.restart.Bind(wx.EVT_BUTTON, self.OnRestart) # bind the restart button
		
		self.btn.Show(False) # hide the racing button 
		self.restart.Show(False) # hide the restart button -- you haven't began yet!
		self.prompt.Show(False) # hide the prompt
		self.end.Show(False)
		if not os.path.exists(os.path.dirname("/TenButtonRace/")): self.clear.Disable(); self.clear.SetLabel("No Record to Clear") # ensure the user
		
	# Event handler for the start button
	def OnClear(self, e): # clear the record
		import shutil
		shutil.rmtree("/TenButtonRace/", True) # whole dir
		self.clear.Disable()
		self.clear.SetLabel("No Record to Clear!")
	
	def OnStart(self, e):
		global btnRemaining, btnNum
		try:
			N = int(self.inputBox.GetValue()) # get the information from the user
			if(N > 0):
				btnRemaining = N; btnNum = N # set the buttons number
			else:
				btnRemaining = 0 # endless
		except:
			if(len(self.inputBox.GetValue()) == 0): btnRemaining = btnNum = 10 # default
			else: raise ValueError("I can't understand!!\n")
		
		self.inputBox.Show(False)
		self.question.Show(False)
		self.clear.Show(False)
		self.start.Show(False) # hide the widgets before
		self.btn.Show(True) # show the button1
		self.prompt.Show(True) # show the prompt
		
		self.startTime = time.time() # record the start time
	
	def OnCheat(self, e): # keyboard-cheat
		key = e.GetKeyCode()
		if(key == 67 and e.AltDown()):
			self.OnBTN(e)
		else:
			self.btn.Show(False) # so the user can't play
			self.end.SetLabel("You've cheated by pressing the keyboard. Game Over.")
			self.end.Show(True) # show it
			self.restart.Show(True) # enable restart
	
	def OnWrong(self, e): # wrong button
		self.btn.Show(False) # so the user can't play
		self.end = wx.StaticText(self.panel, label = "You've clicked on the wrong mouse button :(")
		self.end.Show(True) # show it
		self.restart.Show(True) # enable restart
		
		if(btnRemaining <= 0): # endless mode!
			btnNum = 1 - btnRemaining # calculate the buttons clicked by 0 - btnRemaining + 1
			spent = round(time.time() - self.startTime, 3) # delta t
			self.prompt.Show(False) # hide the prompt
			self.btn.Show(False) # Hide the button
			
			mkdir("/TenButtonRace/") # create the dir if not exist
			try:
				readF = open("/TenButtonRace/Endless.dat", 'r')
				recordNum = int(readF.readline())
				recordAvgTime = float(readF.readline()) # read the current record
				readF.close()
			except:
				recordNum = 0; recordAvgTime = 1000000 # no record yet lol
			recordNum = str(max(recordNum, btnNum)) # compare the record to the buttons clicked
			recordAvgTime = str(min(recordAvgTime, spent / btnNum)) # compare the record to the avg time
			
			writeF = open("/TenButtonRace/Endless.dat", 'w')
			writeF.write(recordNum + '\n' + recordAvgTime) # write the new record to the file.
			writeF.close()
			self.end.SetLabel("You've clicked {} buttons.\nYour time spent: {}s.\nYour record is {} buttons and {}s per button.".format(btnNum, spent, recordNum, recordAvgTime))
			self.end.Show(True) # show it
			
				
	def OnBTN(self, e):
		global btnRemaining, events
		self.btn.SetPosition((randint(1,500), randint(1,500))) # randomly change the position,
		self.btn.SetSize((randint(10,50),randint(10,50))) # and size of the button
		
		curEvent = choice(events.keys()) # get the next button
		self.prompt.SetLabel("Your next click should be: {} button".format(events[curEvent]))
		for event in events:
			if(event == curEvent):
				self.btn.Bind(event, self.OnBTN)
			else:
				self.btn.Bind(event, self.OnWrong) # wrong
		
		btnRemaining -= 1 # minus 1 from it
		if(btnRemaining == 0): # game over
			spent = round(time.time() - self.startTime, 3) # delta t
			self.prompt.Show(False) # hide the prompt
			self.btn.Show(False) # Hide the button
			self.restart.Show(True) # enable restart
			
			mkdir("/TenButtonRace/") # create the dir if not exist
			try:
				readF = open("/TenButtonRace/{}.dat".format(btnNum), 'r')
				record = float(readF.read()) # read the current record
				readF.close()
			except:
				record = 1000000 # no record yet lol
			record = str(min(record, spent)) # compare the record to the spent time
			
			writeF = open("/TenButtonRace/{}.dat".format(btnNum), 'w')
			writeF.write(record) # write the new record to the file.
			writeF.close()
			self.end.SetLabel("You've clicked {} buttons.\nYour time spent: {}s.\nYour record is {}s.".format(btnNum, spent, record))
			self.end.Show(True) # show it
			
	def OnRestart(self, e):
		
		self.restart.Show(False) # hide the restart button
		self.end.Show(False) # hide it
		
		self.btn = wx.Button(self.panel, pos=(randint(1,450), randint(1,450)), size=(randint(10,50),randint(10,50))) # create again	
		self.btn.Bind(wx.EVT_BUTTON, self.OnBTN) # bind the racing button's event
		self.btn.Bind(wx.EVT_KEY_DOWN, self.OnCheat) # see if the user cheats by pressing keys
		
		self.prompt = wx.StaticText(self.panel, label="Your next click should be: left button")
		self.OnStart(e) # start! 
	
# -------- Main Program Below ------------

app = wx.App(False)
frame = TenButtonFrame(None)
frame.Show()
app.MainLoop()