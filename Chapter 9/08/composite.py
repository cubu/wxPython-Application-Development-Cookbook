# Chapter 9: Creating and Customizing Components
# Recipe 8: Creating a composite control
#
import wx
import wx.lib.colourselect as CSEL

class ColourEntry(wx.PyPanel):
    def __init__(self, parent, colour=wx.NullColour):
        super(ColourEntry, self).__init__(parent)

        self._cs = CSEL.ColourSelect(self, colour=colour)
        self._txt = wx.TextCtrl(self, style=wx.TE_READONLY)
        self._Synch()

        self.__DoLayout()
        
        self.Bind(CSEL.EVT_COLOURSELECT, self.OnCSel)

    def __DoLayout(self):
        self.Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.Sizer.Add(self._txt, 0, wx.EXPAND|wx.ALL, 3)
        tsize = self._txt.Size
        self._cs.SetMinSize((tsize[1], tsize[1]))
        self.Sizer.Add(self._cs, 0, wx.EXPAND|wx.ALL, 3)

    def _Synch(self):
        c = self.Colour
        self._txt.Value = c.GetAsString(wx.C2S_HTML_SYNTAX)

    def OnCSel(self, event):
        self._Synch()
        # Reassign object to the ColourEntry instance
        event.SetEventObject(self)
        event.Skip() # allow propagation

    @property
    def Colour(self):
        return self._cs.GetColour()

    @Colour.setter
    def Colour(self, colour):
        self._cs.SetColour(colour)

    @property
    def ColourCode(self):
        return self._txt.Value

#--------------------------------------------------------------#

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        
        for c in [wx.RED, wx.GREEN, wx.WHITE, wx.BLUE, wx.BLACK]:
            self.AddColourEntry(c)

    def AddColourEntry(self, colour):
        ce = ColourEntry(self, colour)
        self.Sizer.Add(ce, 0, wx.EXPAND|wx.ALL, 5)

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title)

        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        panel = MyPanel(self)
        self.Sizer.Add(panel, 1, wx.EXPAND)

        self.SetInitialSize((350, 300))
        
        self.Bind(CSEL.EVT_COLOURSELECT, self.OnColour)

    def OnColour(self, event):
        print event.EventObject
        print event.EventObject.ColourCode

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Composite Control")
        self.frame.Show()
        return True

if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
