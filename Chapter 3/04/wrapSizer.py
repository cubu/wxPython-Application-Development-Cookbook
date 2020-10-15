# Chapter 3: UI Layout and Organization
# Recipe 4: Creating an automatic wrapping layout
#
import wx

class WrappingPanel(wx.Panel):
    def __init__(self, parent):
        super(WrappingPanel, self).__init__(parent)

        sizer = wx.WrapSizer(wx.HORIZONTAL)
        
        # Add many buttons
        for x in range(15):
            button = wx.Button(self, label="Button %d" % x)
            sizer.Add(button, 0, wx.ALL, 5)

        self.SetSizer(sizer)
        self.SetInitialSize()

class MyFrame(wx.Frame):
    def __init__(self, parent, title=""):
        super(MyFrame, self).__init__(parent, title=title)
        
        # Set the panel
        sizer = wx.BoxSizer()
        self.panel = WrappingPanel(self)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        self.SetInitialSize()

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Wrapping layout")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
