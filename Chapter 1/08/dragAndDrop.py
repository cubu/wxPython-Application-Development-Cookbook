# -*- coding: utf-8 -*-
# Chapter 1: wxPython starting points
# Recipe 8: Supporting drag and drop
#
import wx

class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, target):
        super(MyFileDropTarget, self).__init__()
        self.target = target

    def OnDropFiles(self, x, y, filenames):
        for fname in filenames:
            self.target.AppendText(fname)

class MyFrame(wx.Frame):
    def __init__(self, parent, title=""):
        super(MyFrame, self).__init__(parent, title=title)
        
        # Set the panel
        self.text = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.text.AppendText("Drag and drop some files here!")
        dropTarget = MyFileDropTarget(self.text)
        self.text.SetDropTarget(dropTarget)

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Drag and Drop")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()