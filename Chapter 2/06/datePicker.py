# Chapter 2: Common User Controls
# Recipe 6: Picking dates with the DatePickerCtrl
#
import wx
import wx.calendar as wxcal
import datetime

class DatePicker(wx.DatePickerCtrl):
    def __init__(self, parent, dt, style=wx.DP_DEFAULT):
        super(DatePicker, self).__init__(parent, dt=dt, style=style)

        self.SetInitialSize((120, -1))

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        # Layout sizers
        sizer = wx.BoxSizer(wx.VERTICAL)

        now = wx.DateTime.Now();
        self._dp = DatePicker(self, now, 
                              wx.DP_DROPDOWN|wx.DP_SHOWCENTURY)
        sizer.Add(self._dp, 0, wx.ALL, 20)
        
        self.SetSizer(sizer)

class MyFrame(wx.Frame):
    def __init__(self, parent, title=""):
        super(MyFrame, self).__init__(parent, title=title)
        
        # Set the panel
        self.panel = MyPanel(self)
        
        self.Bind(wx.EVT_DATE_CHANGED, self.OnDateChange)

    def OnDateChange(self, evt):
        date = evt.GetDate()
        self.Title = date.Format()

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Picking Dates")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
