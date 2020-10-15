# Chapter 6: Ways to Notify and Alert
# Recipe 2: Using the InfoBar
#
import wx

class AutoDismissInfo(wx.InfoBar):
    def __init__(self, parent, hideAfter=-1):
        super(AutoDismissInfo, self).__init__(parent)

        self._timer = wx.Timer(self)
        self._limit = hideAfter
        
        self.Bind(wx.EVT_TIMER, lambda event: self.Dismiss(), 
                  self._timer)

    def ShowMessage(self, msg, flags):
        if self._timer.IsRunning():
            self._timer.Stop()

        super(AutoDismissInfo, self).ShowMessage(msg, flags)

        if self._limit > 0:
            self._timer.Start(self._limit, True)

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title)

        # Hide messages after 3 seconds
        self.info = AutoDismissInfo(self, 3000)
        self.CreateStatusBar()
        self.SetStatusText("Move the mouse over the window!")
        panel = wx.Panel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.info, 0, wx.EXPAND)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        panel.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        panel.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.info.Bind(wx.EVT_BUTTON, self.OnButton)

    def OnEnter(self, event):
        self.info.ShowMessage("Mouse has entered the window!",
                              wx.ICON_INFORMATION)

    def OnLeave(self, event):
        self.info.ShowMessage("Mouse has left the window!",
                              wx.ICON_WARNING)

#-------------------------------------------------------------#

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Using the InfoBar")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
