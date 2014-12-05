#! /usr/bin/evn python

import wx
import time
from random import randint
times = 0
class TenButtonFrame(wx.Frame):
	def __init__(self, parent = None):
		wx.Frame.__init__(self, parent, wx.ID_ANY, "Ten Button Race!!!", size=(600,600))
		
		self.panel = wx.Panel(self)
		
		self.start = wx.Button(self.panel, label="START!", pos=(250,250))
		self.btn = wx.Button(self.panel, pos=(randint(1,500), randint(1,500)), size=(randint(10,50),randint(10,50)))
		#Hide the other ten buttons
		self.btn.Bind(wx.EVT_CHAR_HOOK, self.OnCheat)
		self.start.Bind(wx.EVT_BUTTON, self.OnStart)
		self.btn.Bind(wx.EVT_BUTTON, self.OnBTN)
		self.btn.Show(False)
		#Bind all the buttons to their event handlers
		
	# Event handler for the start button
	def OnCheat(self, e):
		self.btn.Show(False)
		wx.StaticText(self.panel, label = "You've cheated by pressing the keyboard. Game Over.")
	def OnStart(self, e):
		self.start.Show(False)
		self.btn.Show(True)
		time.clock()
		#Make Button One appear
	def OnBTN(self, e):
		global times
		times += 1
		if(times == 10):
			wx.StaticText(self.panel, label = "Your time spent: {}s.".format(time.clock()))
			self.btn.Show(False)
		self.btn.SetPosition((randint(1,500), randint(1,500)))
		self.btn.SetSize((randint(10,50),randint(10,50)))
	#Other event handlers here
	
	#Remember the last event handler needs to print the final time.
	
	
# -------- Main Program Below ------------

app = wx.App(False)
frame = TenButtonFrame(None)
frame.Show()
app.MainLoop()