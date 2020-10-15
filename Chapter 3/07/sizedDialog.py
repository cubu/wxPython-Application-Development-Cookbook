# Chapter 3: UI Layout and Organization
# Recipe 7: Making dialog layout easy 
#
import wx
import wx.lib.sized_controls as sized

class ProxyConfigDlg(sized.SizedDialog):
    def __init__(self, parent, title):
        super(ProxyConfigDlg, self).__init__(parent, title=title)

        pane = self.GetContentsPane()
        pane.SetSizerType("grid", {"rows":3, "cols":2})
        
        # Build the layout
        proxyLbl = wx.StaticText(pane, label="Proxy URL:")
        url = wx.TextCtrl(pane)
        url.SetSizerProps(expand=True)
        
        nameLbl = wx.StaticText(pane, label="Username:")
        name = wx.TextCtrl(pane)
        name.SetSizerProps(expand=True)
        
        passLbl = wx.StaticText(pane, label="Password:")
        name = wx.TextCtrl(pane, style=wx.TE_PASSWORD)
        name.SetSizerProps(expand=True)

        self.SetButtonSizer(self.CreateButtonSizer(wx.CANCEL|wx.OK))
        self.SetInitialSize((300, 175))
        self.Fit()

#------------------------------------------------------------------#

class MyFrame(sized.SizedFrame):
    def __init__(self, parent, title=""):
        super(MyFrame, self).__init__(parent, title=title)
        
        panel = self.GetContentsPane()
        button = wx.Button(panel, label="Show Dialog")
        
        self.Bind(wx.EVT_BUTTON, self.OnButton, button)

    def OnButton(self, event):
        dialog = ProxyConfigDlg(self, "Sized Dialog")
        dialog.ShowModal()
        dialog.Destroy()

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Sized Panel")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
