# Chapter 6: Retrieving Information from Users, Common Dialogs
# Recipe 7: Guiding selections with a Wizard
#
import wx
import wx.wizard as WIZ

class PageBase(WIZ.WizardPageSimple):
    def __init__(self, parent, title):
        super(PageBase, self).__init__(parent)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, label=title)
        font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD)
        label.SetFont(font)
        sizer.Add(label, 0, wx.ALIGN_CENTER)
        line = wx.StaticLine(self)
        sizer.Add(line, 0, wx.EXPAND|wx.ALL, 5)
        self.Sizer = sizer

    def IsValid(self):
        return True

class QuestionPage(PageBase):
    def __init__(self, parent, title):
        super(QuestionPage, self).__init__(parent, title)

        self.field = wx.TextCtrl(self)
        self.Sizer.Add(self.field, 0, wx.ALL|wx.EXPAND, 5)

    def IsValid(self):
        val = self.field.Value.lower()
        if not val or " dont " in val:
            return False
        return super(QuestionPage, self).IsValid()

class MyWizard(WIZ.Wizard):
    def __init__(self, parent, title):
        bmp = wx.Bitmap("Monty_python_foot.gif")
        super(MyWizard, self).__init__(parent, 
                                       title=title, bitmap=bmp)
        self._pages = list()
        self._SetupPages()
        
        self.Bind(WIZ.EVT_WIZARD_PAGE_CHANGING,
                  self.OnChanging)
    
    def _SetupPages(self):
        page1 = QuestionPage(self, "What is your Name?")
        self._pages.append(page1)
        page2 = QuestionPage(self, "What is your Quest?")
        self._pages.append(page2)
        WIZ.WizardPageSimple.Chain(page1, page2)
        q3 = "What is your Favorite Color?"
        page3 = QuestionPage(self, q3)
        self._pages.append(page3)
        WIZ.WizardPageSimple.Chain(page2, page3)

    def OnChanging(self, event):
        if not event.Page.IsValid():
            event.Veto()
            wx.MessageBox("Into the Volcano!", "Fail!")
            self.Close()

        if event.Page.GetNext() is None:
            wx.MessageBox("Go on. Off you go.", "Success!")

    def Run(self):
        firstPage = self._pages[0]
        self.FitToPage(firstPage)
        return self.RunWizard(firstPage)

#-------------------------------------------------------#
class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title)

        sizer = wx.BoxSizer(wx.VERTICAL)

        panel = wx.Panel(self)
        button = wx.Button(panel, label="Start Wizard")
        psizer = wx.BoxSizer(wx.HORIZONTAL)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(button, 0, wx.ALIGN_CENTER|wx.ALL, 20)
        psizer.AddStretchSpacer()
        psizer.Add(vsizer, 0, wx.ALIGN_CENTER)
        psizer.AddStretchSpacer()
        panel.Sizer = psizer

        sizer.Add(panel, 1, wx.EXPAND)
        self.Sizer = sizer
        
        button.Bind(wx.EVT_BUTTON, self.OnWizard)

    def OnWizard(self, event):
        wizard = MyWizard(self, "Bridgekeeper Quiz")
        if wizard.Run():
            pass
        else:
            pass

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Wizard")
        self.frame.Show()
        return True
    
if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
