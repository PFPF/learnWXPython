#! /usr/bin/evn python

import wx
import time
from random import randint, choice

btnNum = 0
btnRemaining = 0
events = {wx.EVT_BUTTON:"left", wx.EVT_RIGHT_UP:"right"} # after realized that some people don't have middle button

class TenButtonFrame(wx.Frame):
	def __init__(self, parent = None):
		wx.Frame.__init__(self, parent, wx.ID_ANY, "Ten Button Race!!!", size=(600,600)) # initialize the frame
		
		self.panel = wx.Panel(self) # create a panel
		self.question = wx.StaticText(self.panel, label="How many buttons do you want? Default is 10.\n\nN<=0 means as many as you can", pos=(40, 10))
		self.inputBox = wx.TextCtrl(self.panel, pos=(200, 80)) # an input-box
		
		self.start = wx.Button(self.panel, label="START!", pos=(250,250)) # the start button
		self.btn = wx.Button(self.panel, pos=(randint(1,450), randint(1,450)), size=(randint(10,50),randint(10,50))) # create the button
		self.prompt = wx.StaticText(self.panel, label="Your next click should be: left button") # Show the next click
		self.start.Bind(wx.EVT_BUTTON, self.OnStart) # bind the start button's event
		self.btn.Bind(wx.EVT_BUTTON, self.OnBTN) # bind the racing button's event
		self.btn.Bind(wx.EVT_CHAR_HOOK, self.OnCheat) # see if the user cheats by pressing keys
		
		self.btn.Show(False) # hide the racing button 
		self.prompt.Show(False) # hide the prompt
		
	# Event handler for the start button

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
		self.start.Show(False) # hide the widgets before
		self.btn.Show(True) # show the button1
		self.prompt.Show(True) # show the prompt
		time.clock() # the first call
	
	def OnCheat(self, e): # keyboard-cheat
		self.btn.Show(False) # so the user can't play
		wx.StaticText(self.panel, label = "You've cheated by pressing the keyboard. Game Over.")
	
	def OnWrong(self, e): # wrong button
		self.btn.Show(False) # so the user can't play
		wx.StaticText(self.panel, label = "You've clicked on the wrong mouse button :(")
		
		if(btnRemaining <= 0): # endless mode!
			btnNum = 1 - btnRemaining # calculate the buttons clicked by 0 - btnRemaining + 1
			spent = time.clock() # second call
			self.prompt.Show(False) # hide the prompt
			self.btn.Show(False) # Hide the button
			
			try:
				readF = open("endless.txt", 'r')
				recordNum = int(readF.readline())
				recordAvgTime = float(readF.readline()) # read the current record
				readF.close()
			except:
				recordNum = 0; recordAvgTime = 1000000 # no record yet lol
			recordNum = str(max(recordNum, btnNum)) # compare the record to the buttons clicked
			recordAvgTime = str(min(recordAvgTime, spent / btnNum)) # compare the record to the avg time
			
			writeF = open("endless.txt", 'w')
			writeF.write(recordNum + '\n' + recordAvgTime) # write the new record to the file.
			writeF.close()
			wx.StaticText(self.panel, label = "You've clicked {} buttons.\nYour time spent: {}s.\nYour record is {} buttons and {}s per button.".format(btnNum, spent, recordNum, recordAvgTime))
			
			
				
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
			spent = time.clock() # second call
			self.prompt.Show(False) # hide the prompt
			self.btn.Show(False) # Hide the button
			
			try:
				readF = open("{}.txt".format(btnNum), 'r')
				record = float(readF.read()) # read the current record
				readF.close()
			except:
				record = 1000000 # no record yet lol
			record = str(min(record, spent)) # compare the record to the spent time
			
			writeF = open("{}.txt".format(btnNum), 'w')
			writeF.write(record) # write the new record to the file.
			writeF.close()
			wx.StaticText(self.panel, label = "You've clicked {} buttons.\nYour time spent: {}s.\nYour record is {}s.".format(btnNum, spent, record))
	
# -------- Main Program Below ------------

app = wx.App(False)
frame = TenButtonFrame(None)
frame.Show()
app.MainLoop()