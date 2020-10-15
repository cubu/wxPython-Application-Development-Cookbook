# Chapter 4: Containers and Advanced Controls
# Recipe 1: Adding tabs with the Notebook control
#
import wx

class MyNotebook(wx.Notebook):
    def __init__(self, parent):
        super(MyNotebook, self).__init__(parent)     

        # Setup an image list
        self.il = wx.ImageList(16, 16)
        print self.il.Add(wx.Bitmap("smile.png"))
        self.AssignImageList(self.il)

        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnChanging)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnChanged)

    def AddPage(self, page, label, imageId=-1):
        pg = super(MyNotebook, self).AddPage(page, label)
        if imageId >= 0:
            self.SetPageImage(pg, imageId)
        return pg

    def OnChanging(self, event):
        result = wx.MessageBox("Allow Page Change?",
                               "Allow?", wx.YES_NO)
        if result == wx.NO:
            event.Veto()

    def OnChanged(self, event):
        print "Page Changed", event.Selection

class MyFrame(wx.Frame):
    def __init__(self, parent, title=""):
        super(MyFrame, self).__init__(parent, title=title)
        
        # Set the panel
        sizer = wx.BoxSizer()
        self.nb = MyNotebook(self)
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.SetSizer(sizer)

        # Add some pages
        page1 = wx.TextCtrl(self.nb, style=wx.TE_MULTILINE)
        self.nb.AddPage(page1, "Page 1")
        page1 = wx.TextCtrl(self.nb, style=wx.TE_MULTILINE)
        self.nb.AddPage(page1, "Page 2", 0)

        self.SetInitialSize()

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Notebook Control")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
