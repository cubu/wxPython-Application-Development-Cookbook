# Chapter 2: Common User Controls
# Recipe 1: Starting with the easy button
#
import wx

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        # Sizer to control button layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Normal stock button
        button = wx.Button(self, wx.ID_OK)
        sizer.Add(button)

        # Button with a bitmap
        button = wx.Button(self, label="Play")
        bitmap = wx.Bitmap('monkeyTime.png')
        button.SetBitmap(bitmap)
        sizer.Add(button)
        
        # Button to show authorization is needed
        button = wx.Button(self, wx.ID_APPLY)
        button.SetAuthNeeded()
        sizer.Add(button)

        self.SetSizer(sizer)
        self.Bind(wx.EVT_BUTTON, self.OnButton)

    def OnButton(self, event):
        button = event.EventObject
        print("%s was pushed!" % button.Label)
        if button.GetAuthNeeded():
            print("Action requires authorization to proceed!")
        event.Skip()

class MyFrame(wx.Frame):
    def __init__(self, parent, title=""):
        super(MyFrame, self).__init__(parent, title=title)
        
        # Set the panel
        self.panel = MyPanel(self)

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Easy Button")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()