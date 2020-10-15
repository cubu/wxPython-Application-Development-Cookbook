# -*- coding: utf-8 -*-
# Chapter 1: wxPython starting points
# Recipe 5: Understanding the window hierarchy
#
import wx

def SetClipboardText(text):
    data_o = wx.TextDataObject()
    data_o.SetText(text)
    if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():
        wx.TheClipboard.SetData(data_o)
        wx.TheClipboard.Close()

def GetClipboardText():
    text_obj = wx.TextDataObject()
    rtext = ""
    if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():
        if wx.TheClipboard.GetData(text_obj):
            rtext = text_obj.GetText()
            wx.TheClipboard.Close()
    return rtext


class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)
        
        sizer = wx.BoxSizer()
        self.text = wx.TextCtrl(self);
        sizer.Add(self.text)
        self.copy = wx.Button(self, label="Put to Clipboard")
        sizer.Add(self.copy)
        self.paste = wx.Button(self, label="Get from Clipboard")
        sizer.Add(self.paste)
        self.SetSizer(sizer)
        
        self.Bind(wx.EVT_BUTTON, self.OnCopyPaste)

    def OnCopyPaste(self, event):
        if event.EventObject is self.copy:
            SetClipboardText(self.text.Value)
        else:
            self.text.Value = GetClipboardText()

class MyFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="",
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE):
        super(MyFrame, self).__init__(parent, id, title,
                                      pos, size, style)
        
        self.panel = MyPanel(self)

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Clipboard")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
