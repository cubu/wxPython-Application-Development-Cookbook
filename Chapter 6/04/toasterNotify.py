# Chapter 6: Ways to Notify and Alert
# Recipe 4: Displaying transient notifications
#
import wx
import wx.lib.agw.toasterbox as tb

ID_GET_DUR = wx.NewId()
ID_START = wx.NewId()

class AlarmIcon(wx.TaskBarIcon):
    def __init__(self):
        super(AlarmIcon, self).__init__()

        self._timer = wx.Timer(self)
        self._duration = 10

        bmp = wx.Bitmap("clock.png")
        icon = wx.IconFromBitmap(bmp)
        self.SetIcon(icon, "Alarm Clock")
        self.ResetAlarm()
        
        self.Bind(wx.EVT_MENU, self.OnMenu)
        self.Bind(wx.EVT_TIMER, self.OnAlarm)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(ID_GET_DUR, "Set Duration")
        menu.AppendSeparator()
        item = menu.Append(ID_START, "Start")
        item.Enable(not self._timer.IsRunning())
        item = menu.Append(wx.ID_STOP)
        item.Enable(self._timer.IsRunning())
        menu.AppendSeparator()
        menu.Append(wx.ID_EXIT)
        return menu

    def OnMenu(self, event):
        if event.Id == ID_GET_DUR:
            msg = "Enter the alarm timer duration."
            num = wx.GetNumberFromUser(msg, "Duration (sec):", 
                                       "Timer Setting", 
                                       self._duration, 0, 360)
            self._duration = num
            self.ResetAlarm()
        elif event.Id == ID_START:
            self.ResetAlarm()
        elif event.Id == wx.ID_STOP:
            self._timer.Stop()
        elif event.Id == wx.ID_EXIT:
            self.Destroy()
        else:
            event.Skip()

    def OnAlarm(self, event):
        notify = tb.ToasterBox(None, closingstyle=tb.TB_ONCLICK)
        notify.SetPopupPauseTime(self._duration * 1000)
        msg = "Its time! Its time!\nClick to dismiss!"
        notify.SetPopupText(msg)
        notify.SetPopupPositionByInt(3) # bottom right
        notify.Play()

    def ResetAlarm(self):
        if self._timer.IsRunning():
            self._timer.Stop()
        self._timer.Start(self._duration * 1000)

class AlarmClock(wx.App):
    def OnInit(self):
        self.icon = AlarmIcon()
        return True

#------------------------------------------------------#

if __name__ == "__main__":
    app = AlarmClock(False)
    app.MainLoop()
