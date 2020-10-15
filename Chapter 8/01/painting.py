# Chapter 8: User Interface Primitives
# Recipe 1: Painting your UI
#
import wx

class ImageBackground(wx.Panel):
    def __init__(self, parent, bitmap):
        super(ImageBackground, self).__init__(parent)

        self.bitmap = bitmap
        self.width = bitmap.Size.width
        self.height = bitmap.Size.height

        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)

        w, h = self.Size
        cols = (w / self.width) + 1
        rows = (h / self.height) + 1
        x = y = 0

        # Tile the image on the background
        for r in range(rows):
            for c in range(cols):
                dc.DrawBitmap(self.bitmap, x, y, True) 
                x += self.width
            y += self.height
            x = 0

class BinaryInput(ImageBackground):
    def __init__(self, parent, bmp):
        super(BinaryInput, self).__init__(parent, bmp)

        self._DoLayout()

        self.Bind(wx.EVT_BUTTON, self.OnButton)

    def _DoLayout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.txt = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        sizer.Add(self.txt, 0, wx.EXPAND|wx.ALL, 5)
        hsizer = wx.BoxSizer()
        hsizer.AddStretchSpacer()
        btn0 = wx.Button(self, label="0")
        btn1 = wx.Button(self, label="1")
        hsizer.AddMany([(btn0,), ((20, 20),), (btn1,)])
        hsizer.AddStretchSpacer()
        sizer.Add(hsizer, 0, wx.EXPAND)
        self.Sizer = sizer

    def OnButton(self, event):
        obj = event.EventObject
        lbl = obj.Label
        self.txt.AppendText(lbl)

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title)

        sizer = wx.BoxSizer()
        bmp = wx.Bitmap("binary.png")
        self.panel = BinaryInput(self, bmp)
        sizer.Add(self.panel, 1, wx.EXPAND)

        self.Sizer = sizer
        self.SetInitialSize((400, 200))

#-----------------------------------------------------------#

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Painting in your UI")
        self.frame.Show()
        return True
    
if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
