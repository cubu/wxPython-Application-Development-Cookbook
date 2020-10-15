# Chapter 6: Ways to Notify and Alert
# Recipe 3: Providing extra tips on usage
#
import wx

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        self._timer = wx.Timer(self)
        self._countDown = 10
        
        self._msg = wx.StaticText(self, label="")
        self._go = wx.Button(self, label="Go")
        tip = "Start a countdown to exit the application."
        self._go.ToolTipString = tip
        self._stop = wx.Button(self, label="Stop")
        self._stop.Enable(False)
        tip = "Cancel the application exit."
        self._stop.ToolTipString = tip

        self._doLayout()

        self.Bind(wx.EVT_BUTTON, self.OnButton)
        self.Bind(wx.EVT_TIMER, self.OnTimer)

    def _doLayout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        sizer.Add(self._msg, 0, 
                  wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 10)
        bsizer = wx.BoxSizer(wx.HORIZONTAL)
        bsizer.Add(self._go, 0, wx.ALL, 5)
        bsizer.Add(self._stop, 0, wx.ALL, 5)
        sizer.Add(bsizer, 0, 
                  wx.ALIGN_CENTER_HORIZONTAL|wx.BOTTOM, 10)
        
        self.Sizer = sizer

    def OnButton(self, event):
        if event.EventObject is self._go:
            self._timer.Start(1000)
            self._go.Enable(False)
            self._stop.Enable(True)
        else:
            self._timer.Stop()
            self._go.Enable(True)
            self._stop.Enable(False)

    def OnTimer(self, event):
        if self._countDown > 0:
            self._countDown -= 1
            msg = "Exiting in %d seconds..." % self._countDown
            self._msg.Label = msg
            self.Layout()
        else:
            wx.GetApp().Exit()

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title)

        sizer = wx.BoxSizer(wx.VERTICAL)
        panel = MyPanel(self)
        sizer.Add(panel, 1, wx.EXPAND)
        self.Sizer = sizer

        self.SetInitialSize((450, -1))

#-------------------------------------------------------------#

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Providing ToolTips")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
