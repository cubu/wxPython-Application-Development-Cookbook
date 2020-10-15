# Chapter 4: Containers and Advanced Controls
# Recipe 4: Taking control with the FlatNotebook
#
import wx
import wx.lib.agw.flatnotebook as fnb

class EditorBook(fnb.FlatNotebook):
    def __init__(self, parent):
        mystyle = fnb.FNB_DROPDOWN_TABS_LIST|\
                  fnb.FNB_FF2|\
                  fnb.FNB_SMART_TABS|\
                  fnb.FNB_X_ON_TAB
        super(EditorBook, self).__init__(parent, agwStyle=mystyle)     

        self.Bind(fnb.EVT_FLATNOTEBOOK_PAGE_CLOSING, self.OnClosing)

    def OnClosing(self, event):
        pgNum = event.GetSelection()
        page = self.GetPage(pgNum)
        if page.IsModified():
            msg = "Document is modified continue closing?"
            resp = wx.MessageBox(msg, "Close Page?", 
                                 wx.YES_NO|wx.CENTER|\
                                 wx.ICON_QUESTION)
            if resp == wx.NO:
                event.Veto()
                return
        event.Skip()

class MyFrame(wx.Frame):
    def __init__(self, parent, title=""):
        super(MyFrame, self).__init__(parent, title=title)
        
        # Set the panel
        sizer = wx.BoxSizer()
        self.nb = EditorBook(self)
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.SetSizer(sizer)

        # Add some pages
        page1 = wx.TextCtrl(self.nb, style=wx.TE_MULTILINE)
        self.nb.AddPage(page1, "Page 1")
        page2 = wx.TextCtrl(self.nb, style=wx.TE_MULTILINE)
        self.nb.AddPage(page2, "Page 2")

        self.SetInitialSize((400, 300))

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Notebook Control")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
