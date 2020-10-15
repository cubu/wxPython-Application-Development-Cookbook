# Chapter 10: Getting your Application Ready for Release
# Recipe 4: Optimizing for OSX
#
import wx

class OSXApp(wx.App):
    def OnInit(self):
        if wx.Platform == '__WXMAC__':
            spellcheck = "mac.textcontrol-use-spell-checker"
            wx.SystemOptions.SetOptionInt(spellcheck, 1)
            self.SetMacHelpMenuTitleName("&Help")
        self.frame = OSXFrame(None, "Optimize for OSX")
        self.frame.Show()
        return True

    def MacReopenApp(self):
        self.GetTopWindow().Raise()

class OSXFrame(wx.Frame):
    def __init__(self, parent, title):
        super(OSXFrame, self).__init__(parent, title=title)

        self._SetupMenus()

        self.text = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        sizer = wx.BoxSizer()
        sizer.Add(self.text, 1, wx.EXPAND)
        self.Sizer = sizer
        self.SetInitialSize((350, 200))

    def _SetupMenus(self):
        mb = wx.MenuBar()
        fmenu = wx.Menu()
        fmenu.Append(wx.ID_OPEN)
        fmenu.Append(wx.ID_EXIT)
        mb.Append(fmenu, "&File")
        emenu = wx.Menu()
        emenu.Append(wx.ID_COPY)
        emenu.Append(wx.ID_PREFERENCES)
        mb.Append(emenu, "&Edit")
        hmenu = wx.Menu()
        hmenu.Append(wx.NewId(), "&Online help...")
        hmenu.Append(wx.ID_ABOUT, "&About...")
        mb.Append(hmenu, "&Help")
        self.MenuBar = mb

if __name__ == '__main__':
    app = OSXApp(False)
    app.MainLoop()
