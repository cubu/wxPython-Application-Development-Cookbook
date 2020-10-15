# Chapter 9: Creating and Customizing Components
# Recipe 2: Validating user input
#
import wx

class InputValidator(wx.PyValidator):
    def __init__(self, checker = lambda s: s):
        super(InputValidator, self).__init__()
        assert callable(checker), "Checker must be callable"
        self._checker = checker

    def Clone(self):
        return InputValidator(self._checker)

    def Validate(self, win):
        ok = False
        txt = self.GetWindow();
        if self._checker(txt.Value):
            txt.BackgroundColour = wx.NullColour
            txt.ForegroundColour = wx.NullColour
            ok = True
        else:
            # Indicate the invalid field
            txt.BackgroundColour = wx.RED
            txt.ForegroundColour = wx.WHITE
        txt.Refresh()
        return ok

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True

#---------------------------------------------------------------#

class LoginDialog(wx.Dialog):
    def __init__(self, parent, title="Login"):
        super(LoginDialog, self).__init__(parent, title=title)

        self._user = wx.TextCtrl(self, 
                                 validator=InputValidator(),
                                 name="Username")
        self._pass = wx.TextCtrl(self, 
                                 validator=InputValidator(),
                                 style=wx.TE_PASSWORD,
                                 name="Password")
        
        self.__DoLayout()
        self.SetInitialSize((350, -1))

    def __DoLayout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        fieldSz = wx.FlexGridSizer(2, 2, 5, 8)
        fieldSz.AddGrowableCol(1, 1)
        userLbl = wx.StaticText(self, label="Username:")
        fieldSz.Add(userLbl, 0, wx.ALIGN_CENTER_VERTICAL)
        fieldSz.Add(self._user, 1, wx.EXPAND)
        passLbl = wx.StaticText(self, label="Password:")
        fieldSz.Add(passLbl, 0, wx.ALIGN_CENTER_VERTICAL)
        fieldSz.Add(self._pass, 1, wx.EXPAND)
        
        sizer.Add((10, 10))
        sizer.Add(fieldSz, 1, wx.ALL|wx.EXPAND, 5)
        btnSz = self.CreateButtonSizer(wx.OK|wx.CANCEL)
        sizer.Add(btnSz, 0, wx.EXPAND|wx.BOTTOM|wx.TOP, 5)
        
        self.Sizer = sizer

    @property
    def Username(self):
        return self._user.Value

    @property
    def Password(self):
        return self._pass.Value

#--------------------------------------------------------------#

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title)

        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self)
        panel.Sizer = wx.BoxSizer()
        msg = wx.StaticText(panel, label="Congratulations you logged in!")
        panel.Sizer.Add(msg, 0, wx.ALIGN_CENTER)
        self.Sizer.Add(panel, 1, wx.EXPAND)

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Custom Dialog")

        validName = "wxPython"
        validPass = "123"

        result = False
        
        while not result:
            dlg = LoginDialog(self.frame)
            if dlg.ShowModal() == wx.ID_OK:
                result = dlg.Username == validName and dlg.Password == validPass
                if result:
                    self.frame.Show()
            else: # cancelled login attempt
                self.frame.Destroy()
                break

        return True

if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
