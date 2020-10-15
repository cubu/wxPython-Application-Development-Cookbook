# Chapter 6: Retrieving Information from Users, Common Dialogs
# Recipe 4: 
#
import wx

class BitmapPanel(wx.Panel):
    def __init__(self, parent):
        super(BitmapPanel, self).__init__(parent)

        sizer = wx.WrapSizer(wx.HORIZONTAL)
        self.Sizer = sizer

    def AddBitmap(self, artID):
        bmp = wx.ArtProvider.GetBitmap(artID)
        sbmp = wx.StaticBitmap(self, bitmap=bmp)
        self.Sizer.Add(sbmp, 0, wx.ALL, 8)
        self.Layout()

class MainPanel(wx.Panel):
    def __init__(self, parent):
        super(MainPanel, self).__init__(parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = BitmapPanel(self)
        sizer.Add(self.panel, 1, wx.EXPAND)
        button = wx.Button(self, label="Pick Images")
        sizer.Add(button, 0, wx.ALIGN_CENTER_HORIZONTAL)
        button.Bind(wx.EVT_BUTTON, self.OnGetChoices)

        self.Sizer = sizer

    def OnGetChoices(self, event):
        msg = "Pick the are resources to view."
        ids = [ x for x in dir(wx) 
               if x.startswith("ART_") ]
        dlg = wx.MultiChoiceDialog(self, msg, 
                                   "Pick Images", ids)
        if (dlg.ShowModal() == wx.ID_OK):
            for selection in dlg.GetSelections():
                theId = getattr(wx, ids[selection])
                self.panel.AddBitmap(theId)

class BitmapViewer(wx.Frame):
    def __init__(self, parent, title):
        super(BitmapViewer, self).__init__(parent, title=title)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = MainPanel(self)
        sizer.Add(self.panel, 1, wx.EXPAND)

        self.Sizer = sizer

#-----------------------------------------------------------#

class MyApp(wx.App):
    def OnInit(self):
        self.frame = BitmapViewer(None, title="MulitChoice")
        self.frame.Show()
        return True
    
if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
