# Chapter 3: UI Layout and Organization
# Recipe 3: Grouping controls with a StaticBox control
#
import wx

class GroupBox(wx.StaticBox):
    def __init__(self, parent, orient, label=""):
        super(GroupBox, self).__init__(parent, label=label)
        self._sizer = wx.StaticBoxSizer(self, orient)

    def AddItem(self, item, proportion=0, flag=wx.ALL, border=5):
        self._sizer.Add(item, proportion, flag, border)

    @property
    def Sizer(self):
        return self._sizer

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        # Layout sizers
        sizer = wx.BoxSizer(wx.VERTICAL)
        sbox = GroupBox(self, wx.HORIZONTAL, "Button Group")
        for x in range(1, 4):
            button = wx.Button(self, label="Button %d" % x)
            sbox.AddItem(button)

        sizer.Add(sbox.Sizer, 0, wx.ALL, 20)
        self.SetSizer(sizer)

class MyFrame(wx.Frame):
    def __init__(self, parent, title=""):
        super(MyFrame, self).__init__(parent, title=title)
        
        # Set the panel
        self.panel = MyPanel(self)

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="StaticBox")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
