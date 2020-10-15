# Chapter 9: Creating and Customizing Components
# Recipe 5: 
#
import wx

class FunctionPanel(wx.PyPanel):
    def __init__(self, parent):
        super(FunctionPanel, self).__init__(parent)

        self._pane = None
        self._bar = FunctionBar(self)
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self._bar, 0, wx.EXPAND)

        self.Bind(wx.EVT_BUTTON, self.OnButton)

    def OnButton(self, event):
        if event.Id == wx.ID_CLOSE:
            self.ShowFunctionBar(False)
        else:
            event.Skip()

    @property
    def ContentPane(self):
        return self._pane

    def SetContentPane(self, pane):
        if self._pane == None:
            self.Sizer.Insert(0, pane, 1, wx.EXPAND)
        else:
            self.Sizer.Replace(self._pane, pane)
            self._pane.Destroy()
        self._pane = pane
        self.Layout()

    def AddFunctionButton(self, id, label=wx.EmptyString):
        self._bar.AddFunctionButton(id, label)

    def IsBarShown(self):
        return self._bar.IsShown()

    def ShowFunctionBar(self, show=True):
        self._bar.Show(show)
        self.Layout()

class FunctionBar(wx.PyPanel):
    def __init__(self, parent):
        super(FunctionBar, self).__init__(parent)

        cbmp = wx.ArtProvider.GetBitmap(wx.ART_CLOSE, 
                                        wx.ART_MENU)
        self._close = wx.BitmapButton(self, wx.ID_CLOSE, cbmp)
        self.Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.Sizer.Add(self._close, 0, wx.ALL, 5)

    def AddFunctionButton(self, id, label=wx.EmptyString):
        button = wx.Button(self, id, label)
        self.Sizer.Add(button, 0, wx.ALL, 5)

#--------------------------------------------------------------#
ID_SHOW_BAR = wx.NewId()

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title)

        self.MenuBar = wx.MenuBar()
        view = wx.Menu()
        item = view.Append(ID_SHOW_BAR, 
                           "Show Function Bar\tCtrl+B", 
                           kind=wx.ITEM_CHECK)
        item.Check(True)
        self.MenuBar.Append(view, "View")

        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        panel = FunctionPanel(self)
        panel.SetContentPane(wx.TextCtrl(panel, style=wx.TE_MULTILINE))
        panel.AddFunctionButton(wx.ID_CUT)
        panel.AddFunctionButton(wx.ID_COPY)
        panel.AddFunctionButton(wx.ID_PASTE)
        self.Sizer.Add(panel, 1, wx.EXPAND)
        self._panel = panel
        
        self.Bind(wx.EVT_BUTTON, self.OnFunctionButton)
        self.Bind(wx.EVT_MENU, self.OnMenu, id=ID_SHOW_BAR)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdate, id=ID_SHOW_BAR)

        self.SetInitialSize()

    def OnFunctionButton(self, event):
        txt = self._panel.ContentPane
        if event.Id == wx.ID_CUT:
            txt.Cut()
        elif event.Id == wx.ID_COPY:
            txt.Copy()
        elif event.Id == wx.ID_PASTE:
            txt.Paste()
        else:
            event.Skip()

    def OnMenu(self, event):
        show = event.EventObject.IsChecked(event.Id)
        self._panel.ShowFunctionBar(show)

    def OnUpdate(self, event):
        event.Check(self._panel.IsBarShown())

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Function Panel")
        self.frame.Show()
        return True

if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
