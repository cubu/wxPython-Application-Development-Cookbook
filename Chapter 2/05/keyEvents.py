# Chapter 2: Common User Controls
# Recipe 5: Processing key events
#
from urllib import urlopen
import re

from abc import ABCMeta, abstractmethod
import wx

class CompleterDataSource:
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def getSuggestions(self, phrase):
        """return list of strings"""
        pass

class DataSourceTextCtrl(wx.TextCtrl):
    def __init__(self, parent, dataSource):
        super(DataSourceTextCtrl, self).__init__(parent)

        assert isinstance(dataSource, CompleterDataSource)
        self._dataSource = dataSource
        
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def OnKeyDown(self, event):
        self.AutoComplete([])
        event.Skip()

    def OnChar(self, event):
        char = unichr(event.KeyCode)
        if not char.isalnum():
            char = ""

        query = self.Value + char
        tips = self._dataSource.getSuggestions(query)
        if tips:
            self.AutoComplete(tips)
        event.Skip()

class GoogleSuggestSource(CompleterDataSource):
    def getSuggestions(self, phrase):
        """Query google for suggestion list"""
        if phrase:
            url = "http://google.com/complete/search?output=toolbar&q="
            page = urlopen(url + phrase).read()
            suggestions = re.findall(r'data="([\w*\s*]+)"', page)
            return suggestions

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        # Layout sizers
        vsizer = wx.BoxSizer(wx.VERTICAL)
        
        field1 = wx.BoxSizer(wx.HORIZONTAL)
        field1.Add(wx.StaticText(self, label="Field 1:"))
        textCtrl = DataSourceTextCtrl(self, GoogleSuggestSource())
        field1.Add(textCtrl)
        vsizer.Add(field1)
        
        self.SetSizer(vsizer)

class MyFrame(wx.Frame):
    def __init__(self, parent, title=""):
        super(MyFrame, self).__init__(parent, title=title)
        
        # Set the panel
        self.panel = MyPanel(self)

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Key Events")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
