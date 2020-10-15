# Chapter 3: UI Layout and Organization
# Recipe 1: Understanding control layout
#
import wx

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        # Define controls
        self.label = wx.StaticText(self, label="Label:")
        choices = ['a', 'b', 'c']
        self.choice = wx.Choice(self, choices=choices)
        self.info = wx.StaticText(self)
        
        # Do Layout
        self._doLayout()

        self.Bind(wx.EVT_CHOICE, self.OnChoice, self.choice)

    def _doLayout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddStretchSpacer()

        row = wx.BoxSizer(wx.HORIZONTAL)
        row.Add(self.label)
        row.AddSpacer(10)
        row.Add(self.choice)
        
        sizer.Add(row, flag=wx.CENTER)
        
        sizer.Add(self.info, flag=wx.CENTER)
        sizer.AddStretchSpacer()
        self.SetSizer(sizer)

    def OnChoice(self, event):
        self.info.Label = "'%s' was selected!" % event.String
        self.Layout()

class MyFrame(wx.Frame):
    def __init__(self, parent, title=""):
        super(MyFrame, self).__init__(parent, title=title)
        
        # Set the panel
        self.panel = MyPanel(self)
        
        self.SetInitialSize((200, 100))

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Laying out controls with Sizers")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
