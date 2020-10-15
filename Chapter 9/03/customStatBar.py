# Chapter 9: Creating and Customizing Components
# Recipe 3: Interacting with the StatusBar
#
import wx
CSB_MSG = 0
CSB_ICON = 1

class CustomStatusBar(wx.StatusBar):
    def __init__(self, parent):
        super(CustomStatusBar, self).__init__(parent)

        self.err, self.info = self._GetIcons()
        self.img = wx.StaticBitmap(self)
        self.menu = wx.Menu()
        self.menu.Append(wx.ID_COPY) 

        self.SetFieldsCount(2)
        self.SetStatusWidths([-1, 24])

        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MENU, self.OnMenu)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def _GetIcons(self):
        errBmp = wx.ArtProvider.GetBitmap(wx.ART_ERROR, 
                                          wx.ART_MENU,
                                          (16,16))
        infoBmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION,
                                           wx.ART_MENU,
                                           (16,16))
        return errBmp, infoBmp

    def OnLeftUp(self, event):
        pt = event.GetPosition()
        if self.GetFieldRect(CSB_MSG).Contains(pt):
            rect = self.GetFieldRect(CSB_MSG)
            self.PopupMenu(self.menu, (rect.x, rect.Bottom))

    def OnMenu(self, event):
        if event.Id == wx.ID_COPY:
            msg = self.GetStatusText()
            if wx.TheClipboard.Open():
                data = wx.TextDataObject(msg)
                wx.TheClipboard.SetData(data)

    def OnSize(self, event):
        rect = self.GetFieldRect(CSB_ICON)
        w, h = self.img.Size
        xpad = (rect.width - w) / 2
        ypad = (rect.height - h) / 2
        self.img.SetPosition((rect.x + xpad, rect.y + ypad))
        event.Skip()

    def PushInfoMsg(self, msg):
        self.img.SetBitmap(self.info)
        self.img.Show()
        self.PushStatusText(msg)

    def PushErrorMsg(self, msg):
        self.img.SetBitmap(self.err)
        self.img.Show()
        self.PushStatusText(msg)
        
#-----------------------------------------------------------#
ID_ERROR = wx.NewId()
ID_INFO = wx.NewId()

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        button = wx.Button(self, ID_ERROR, "Make Error")
        sizer.Add(button, 0, wx.ALL, 20)
        button = wx.Button(self, ID_INFO, "Make Info")
        sizer.Add(button, 0, wx.ALL, 20)
        self.Sizer = sizer
        
class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title)

        sizer = wx.BoxSizer()
        self.panel = MyPanel(self)
        sizer.Add(self.panel, 1, wx.EXPAND)

        self._bar = CustomStatusBar(self)
        self.SetStatusBar(self._bar)

        self.Sizer = sizer
        self.SetInitialSize()
        
        self.Bind(wx.EVT_BUTTON, self.OnButton)

    def OnButton(self, event):
        if event.Id == ID_ERROR:
            self._bar.PushErrorMsg("Operation failed!")
        elif event.Id == ID_INFO:
            self._bar.PushInfoMsg("Save succeeded")
        else:
            event.Skip()

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Interactive StatusBar")
        self.frame.Show()
        return True
    
if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
