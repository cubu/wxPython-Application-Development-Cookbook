# Chapter 2: Common User Controls
# Recipe 4: Using the TextCtrl
#
import wx

class MemoryTextCtrl(wx.TextCtrl):
    """TextCtrl that remembers previous entries"""
    def __init__(self, parent):
        super(MemoryTextCtrl, self).__init__(parent)

        self._memories = set()

        self.Bind(wx.EVT_KILL_FOCUS, lambda event: self.Memorize())
        self.Bind(wx.EVT_SET_FOCUS, self.OnUpdateCompleteList)

    def OnUpdateCompleteList(self, event):
        # Set the autocomplete list with the
        # latest set of memories.
        self.AutoComplete(list(self._memories))
        event.Skip()

    def Memorize(self):
        """remember the current value"""
        if self.Value:
            self._memories.add(self.Value)

    def Forget(self):
        """forget all remembered words"""
        self._memories.clear()

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        # Layout sizers
        vsizer = wx.BoxSizer(wx.VERTICAL)
        
        field1 = wx.BoxSizer(wx.HORIZONTAL)
        field1.Add(wx.StaticText(self, label="Field 1:"))
        textCtrl = MemoryTextCtrl(self)
        field1.Add(textCtrl)
        vsizer.Add(field1)
        
        field2 = wx.BoxSizer(wx.HORIZONTAL)
        field2.Add(wx.StaticText(self, label="Field 2:"))
        textCtrl = MemoryTextCtrl(self)
        field2.Add(textCtrl)
        vsizer.Add(field2)
        
        self.SetSizer(vsizer)

class MyFrame(wx.Frame):
    def __init__(self, parent, title=""):
        super(MyFrame, self).__init__(parent, title=title)
        
        # Set the panel
        self.panel = MyPanel(self)

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="The TextCtrl")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
