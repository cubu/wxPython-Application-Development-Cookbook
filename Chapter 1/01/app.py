# -*- coding: utf-8 -*-
# Chapter 1: wxPython starting points
# Recipe 1: Creating the application object
#
import wx

class MyApp(wx.App):
    def OnInit(self):
        wx.MessageBox("Hello wxPython", "wxApp")
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()