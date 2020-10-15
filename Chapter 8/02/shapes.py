# Chapter 8: User Interface Primitives
# Recipe 2: Drawing basic shapes
#
import wx

class Canvas(wx.Panel):
    def __init__(self, parent):
        super(Canvas, self).__init__(parent)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnBackground)

    def OnBackground(self, event):
        sky = wx.TheColourDatabase.FindColour("SKY BLUE")
        event.DC.SetBrush(wx.Brush(sky))
        event.DC.DrawRectangleRect(self.Rect)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        w, h = self.Size

        self.DrawSun(dc, h, w)
        self.DrawGrass(dc, h, w)
        self.DrawStopSign(dc, h, w)

    def DrawSun(self, dc, h, w):
        dc.SetBrush(wx.YELLOW_BRUSH)
        dc.SetPen(wx.RED_PEN)
        dc.DrawCircle(w - 55, 55, 50)

    def DrawGrass(self, dc, h, w):
        dc.SetBrush(wx.GREEN_BRUSH)
        dc.SetPen(wx.GREEN_PEN)
        dc.DrawRectangle(0, h - 75, w, 75)

    def DrawStopSign(self, dc, h, w):
        dc.SetBrush(wx.RED_BRUSH)
        dc.SetPen(wx.BLACK_PEN)
        dc.DrawPolygon([(70, 190), (70, 215), (85, 230), 
                        (110, 230), (125, 215), (125, 190),
                        (110, 175), (85, 175)])
        dc.SetTextForeground(wx.WHITE)
        dc.DrawText("STOP", 80, 193)
        dc.DrawLine(97, 230, 97, h - 75) 

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title)

        sizer = wx.BoxSizer()
        self.panel = Canvas(self)
        sizer.Add(self.panel, 1, wx.EXPAND)

        self.Sizer = sizer
        self.SetInitialSize((400, 400))
        self.SetMaxSize((400, 400))

#-----------------------------------------------------------#

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Painting in your UI")
        self.frame.Show()
        return True
    
if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
