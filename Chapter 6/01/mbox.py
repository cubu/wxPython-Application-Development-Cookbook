# Chapter 6: Ways to Notify and Alert
# Recipe 1: Showing a MessageBox
#
import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title)

        panel = wx.Panel(self)
        button = wx.Button(panel, label="Show MessageBox")
        hsizer = wx.BoxSizer()
        hsizer.AddStretchSpacer()
        hsizer.Add(button, 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer.AddStretchSpacer()
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(hsizer, 1, wx.ALIGN_CENTER_HORIZONTAL)
        panel.SetSizer(vsizer)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        self.Bind(wx.EVT_BUTTON, self.OnButton, button)

    def OnButton(self, event):
        result = wx.MessageBox("Heres the message text!",
                               "Here is the Title",
                               wx.YES_NO|wx.CENTER|wx.ICON_INFORMATION)
        if result == wx.NO:
            print("Answer was no!")
        else:
            print("Answer was yes!")

#-------------------------------------------------------------#

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Show a MessageBox")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
