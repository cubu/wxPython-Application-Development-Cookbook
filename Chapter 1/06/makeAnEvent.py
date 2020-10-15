# -*- coding: utf-8 -*-
# Chapter 1: wxPython starting points
# Recipe 6: Controlling the propagation of events (theres more)
#
import wx
import wx.lib.newevent

# Create a special event
MyEvent, EVT_MYEVENT = wx.lib.newevent.NewCommandEvent();

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, "Event Propagation")
        self.frame.Show();
        
        self.Bind(EVT_MYEVENT, self.OnMyEvent)
        return True

    def OnMyEvent(self, event):
        print("MyEvent occured!")

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title)
        
        self.panel = wx.Panel(self)
        button = wx.Button(self.panel, label="Push Me")
        self.Bind(wx.EVT_BUTTON, self.OnButton)

    def OnButton(self, event):
        # send our custom event
        wx.PostEvent(self, MyEvent(self.Id))

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
