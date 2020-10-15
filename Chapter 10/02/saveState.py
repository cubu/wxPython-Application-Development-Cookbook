# Chapter 10: Getting your Application Ready for Release
# Recipe 2: Saving application state
#
import wx
import wx.lib.agw.persist as PERSIST

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, 
                                      name="MyAppsFrame")
        sizer = wx.BoxSizer()
        sizer.Add(MyPanel(self), 1, wx.EXPAND)
        self.Sizer = sizer
        
        self.Register(self)

        self.Bind(wx.EVT_CLOSE, self.OnExit)

    def Register(self, win):
        mgr = PERSIST.PersistenceManager.Get()
        if win and win.Name not in PERSIST.BAD_DEFAULT_NAMES:
            mgr.RegisterAndRestore(win)

        for child in win.Children:
            self.Register(child)

    def OnExit(self, event):
        mgr = PERSIST.PersistenceManager.Get()
        mgr.SaveAndUnregister()
        event.Skip()

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        cb1 = wx.CheckBox(self, label="Option 1", name="opt1")
        cb2 = wx.CheckBox(self, label="Option 2", name="opt2")
        sizer.AddMany([(cb1, 0, wx.ALL, 10), 
                       (cb2, 0, wx.ALL, 10)])
        self.Sizer = sizer

class MyApp(wx.App):
    def OnInit(self):
        self.SetAppName("PersistControls")
        self.frame = MyFrame(None, title="Save State")
        self.frame.Show()
        return True

if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
