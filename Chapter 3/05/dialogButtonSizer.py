# Chapter 3: UI Layout and Organization
# Recipe 5: Using standard dialog button layout
#
import wx

class CustomMessageDialog(wx.Dialog):
    def __init__(self, parent, title, msg, buttonFlags):
        super(CustomMessageDialog, self).__init__(parent, title=title)

        sizer = wx.BoxSizer(wx.VERTICAL)
        
        msgSizer = self.CreateTextSizer(msg)
        sizer.Add(msgSizer, 0, wx.EXPAND|wx.ALL, 5)
        
        sizer.AddStretchSpacer()

        btnSizer = self.CreateStdDialogButtonSizer(buttonFlags)
        sizer.Add(btnSizer, 0, wx.EXPAND|wx.BOTTOM, 5)

        self.SetSizer(sizer)
        self.SetInitialSize()

#------------------------------------------------------------------#

class MyFrame(wx.Frame):
    def __init__(self, parent, title=""):
        super(MyFrame, self).__init__(parent, title=title)
        
        # Set the panel
        panel = wx.Panel(self)

        sizer = wx.BoxSizer()
        button = wx.Button(panel, label="Show Dialog")
        sizer.Add(button)
        panel.SetSizer(sizer)
        
        self.Bind(wx.EVT_BUTTON, self.OnShowDialog, button)

    def OnShowDialog(self, event):
        CustomMessageDialog(self, "StdDialogButtonSizer", 
                 "See how the buttons are spaced\nAlso notice how they are aligned to follow platform guidelines.", 
                 wx.OK|wx.CANCEL).ShowModal()

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Standard Button Layout")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
