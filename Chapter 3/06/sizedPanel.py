# Chapter 3: UI Layout and Organization
# Recipe 6: Simplfying panel layout
#
import wx
import wx.lib.sized_controls as sized

class MyPanel(sized.SizedScrolledPanel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        self.SetSizerType("form")

        # Add some controlls
        label = wx.StaticText(self, label="Field 1:")
        text = wx.TextCtrl(self)
        text.SetSizerProp("expand", True)

        label2 = wx.StaticText(self, label="Field 2:")
        choice = wx.Choice(self, choices=['1', '2', '3'])
        choice.SetSizerProp("expand", True)

#------------------------------------------------------------------#

class MyFrame(wx.Frame):
    def __init__(self, parent, title=""):
        super(MyFrame, self).__init__(parent, title=title)
        
        # Set the panel
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(MyPanel(self), 1, wx.EXPAND)
        self.SetSizer(sizer)

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Sized Panel")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
