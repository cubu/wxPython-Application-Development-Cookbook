# -*- coding: utf-8 -*-
# Chapter 1: wxPython starting points
# Recipe 9: Handling AppleEvents
#
import wx

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame("Apple Events")
        self.frame.Show()
        return True

    def MacNewFile(self):
        """Called in response to an open-application event"""
        self.frame.AddNewFile()

    def MacOpenFiles(self, fileNames):
        """Called in response to an openFiles message in Cocoa
        or an open-document event in Carbon
        """
        self.frame.AddFiles(fileNames)

    def MacOpenURL(self, url):
        """Called in response to get-url event"""
        self.frame.AddURL(url)

    def MacPrintFile(self, fileName):
        """Called in response to a print-document event"""
        self.frame.PrintFile(fileName)

    def MacReopenApp(self):
        """Called in response to a reopen-application event"""
        if self.frame.IsIconized():
            self.frame.Iconize(False)
        self.frame.Raise()

class MyFrame(wx.Frame):
    def __init__(self, title):
        super(MyFrame, self).__init__(None, title=title)

        self._list = wx.ListBox(self)

    def AddFiles(self, files):
        self._list.AppendItems(files)

    def AddNewFile(self):
        newFileName = "NewFile-%d" % self._list.Count
        self._list.Append(newFileName)

    def AddURL(self, url):
        self._list.Append(url)

    def PrintFile(self, fileName):
        printMsg = "Print - %s" % fileName
        self._list.Append(printMsg)

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()