# -*- coding: utf-8 -*-
# Chapter 1: wxPython starting points
# Recipe 6: Controlling the propagation of events
#
import wx

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)
        
        sizer = wx.BoxSizer()
        self.button1 = wx.Button(self, label="Button 1")
        sizer.Add(self.button1)
        self.button2 = wx.Button(self, label="Button 2")
        sizer.Add(self.button2)
        self.SetSizer(sizer)
        
        self.Bind(wx.EVT_BUTTON, self.OnButton)

    def OnButton(self, event):
        button = event.EventObject
        print("Button (%s) event at Panel!" % button.Label)
        if button is self.button1:
            event.Skip()

class MyFrame(wx.Frame):
    def __init__(self, parent, title=""):
        super(MyFrame, self).__init__(parent, title=title)
        
        self.panel = MyPanel(self)
        
        self.Bind(wx.EVT_BUTTON, self.OnButton)

    def OnButton(self, event):
        button = event.EventObject
        print("Button (%s) event at Frame!" % button.Label)
        event.Skip()

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Event Propagation")
        self.frame.Show();
        
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        return True

    def OnButton(self, event):
        button = event.EventObject
        print("Button (%s) event at App!" % button.Label)
        event.Skip()

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
