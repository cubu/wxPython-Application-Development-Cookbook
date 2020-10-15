# Chapter 4: Containers and Advanced Controls
# Recipe 2: Enhancing a ComboBox with Bitmaps
#
import wx
import wx.lib.langlistctrl as langlist
import wx.combo

class LanguageComboBox(wx.combo.BitmapComboBox):
    def __init__(self, parent):
        super(LanguageComboBox, self).__init__(parent)

        for x in dir(wx):
            if x.startswith("LANGUAGE_"):
                langID = getattr(wx, x)
                flag = self.GetFlag(langID)
                name = wx.Locale.GetLanguageName(langID)
                
                self.Append(name, flag)

    def GetFlag(self, langID):
        flag = langlist.GetLanguageFlag(langID)
        if flag.IsOk():
            if flag.Size != (16, 11):
                img = wx.ImageFromBitmap(flag)
                img.Rescale(16, 11)
                flag = img.ConvertToBitmap()
        return flag

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        self._combo = LanguageComboBox(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self._combo, 1, wx.EXPAND|wx.CENTER)
        sizer.Add(hsizer, 0, wx.EXPAND|wx.CENTER)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_COMBOBOX, self.OnLanguageSelect)

    def OnLanguageSelect(self, event):
        print("Selected: %s" % self._combo.Value)
        
class MyFrame(wx.Frame):
    def __init__(self, parent, title=""):
        super(MyFrame, self).__init__(parent, title=title)
        
        # Set the panel
        sizer = wx.BoxSizer()
        sizer.Add(MyPanel(self), 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.SetInitialSize((300, 200))

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="BitmapComboBox")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
