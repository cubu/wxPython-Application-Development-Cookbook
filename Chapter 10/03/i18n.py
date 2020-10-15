# Chapter 10: Getting your Application Ready for Release
# Recipe 3: Supporting internationalization
#
import wx
import os

# Function alias
_ = wx.GetTranslation

class TranslatableApp(wx.App):
    def OnInit(self):
        self.SetAppName("I18NTestApp")
        
        # Get user configured language if set
        config = wx.Config()
        lang = config.Read('lang', 'LANGUAGE_DEFAULT')
        
        # Setup the Local
        self.locale = wx.Locale(getattr(wx, lang))
        path = os.path.abspath('./locale') + os.path.sep
        self.locale.AddCatalogLookupPathPrefix(path)
        self.locale.AddCatalog(self.AppName)
        
        self.frame = TestFrame(None, title=_("Sample App"))
        self.frame.Show()
        return True

class TestFrame(wx.Frame):
    def __init__(self, parent, title=""):
        super(TestFrame, self).__init__(parent, title=title)

        self.panel = TestPanel(self)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.Sizer = sizer
        self.SetInitialSize((350, 200))
        
        self.Bind(wx.EVT_BUTTON, self.OnButton)

    def OnButton(self, event):
        if event.Id == wx.ID_CLOSE:
            self.Close()

class TestPanel(wx.Panel):
    def __init__(self, parent):
        super(TestPanel, self).__init__(parent)

        self.closebtn = wx.Button(self, wx.ID_CLOSE)
        self.langch = wx.Choice(self, 
                                choices=[_("English"), 
                                         _("Japanese")])
        self.__DoLayout()
        self.Bind(wx.EVT_CHOICE, self.OnChoice)

    def __DoLayout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        greeting = wx.StaticText(self, label=_("Hello"))
        sizer.Add(greeting, 0, wx.ALIGN_CENTER_HORIZONTAL)
        
        langsz = wx.BoxSizer(wx.HORIZONTAL)
        langlbl = wx.StaticText(self, label=_("Language"))
        langsz.Add(langlbl, 0, 
                   wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        langsz.Add(self.langch, 1, 
                   wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        sizer.Add(langsz, 0, wx.ALL|wx.EXPAND, 5)
        
        sizer.Add(self.closebtn, 0, 
                  wx.ALIGN_RIGHT|wx.RIGHT, 5)
        self.Sizer = sizer

    def OnChoice(self, event):
        if self.langch.Selection == 0:
            val = 'LANGUAGE_ENGLISH'
        else:
            val = 'LANGUAGE_JAPANESE'
        config = wx.Config()
        config.Write('lang', val)
        
if __name__ == '__main__':
    app = TranslatableApp(False)
    app.MainLoop()
