# Chapter 8: User Interface Primitives
# Recipe 4: Drawing Gradients with a GraphicsContext
#
import wx

class PodLabel(wx.PyControl):
    def __init__(self, parent, label, color):
        super(PodLabel, self).__init__(parent,
                                       style=wx.NO_BORDER)
        self._label = label
        self._color = color

        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def DoGetBestSize(self):
        txtsz = self.GetTextExtent(self._label)
        size = wx.Size(txtsz[0] + 10, txtsz[1] + 6)
        return size

    def OnPaint(self, event):
        gcdc = wx.GCDC(wx.PaintDC(self))
        gc = gcdc.GetGraphicsContext()

        # Get the working rectangle we can draw in
        rect = self.GetClientRect()

        # Setup the GraphicsContext
        pen = gc.CreatePen(wx.TRANSPARENT_PEN)
        gc.SetPen(pen)
        rgb = self._color.Get(False)
        alpha = self._color.Alpha() *.2 # fade to transparent
        color2 = wx.Colour(*rgb, alpha=alpha)
        x1, y1 = rect.x, rect.y
        y2 = y1 + rect.height
        gradbrush = gc.CreateLinearGradientBrush(x1, y1,
                                                 x1, y2,
                                                 self._color,
                                                 color2)
        gc.SetBrush(gradbrush)

        # Draw the background
        gc.DrawRoundedRectangle(rect.x, rect.y,
                                rect.width, rect.height,
                                rect.height/2)

        # Use the GCDC to help draw the aa text
        gcdc.DrawLabel(self._label, rect, wx.ALIGN_CENTER)

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        vsizer = wx.BoxSizer(wx.VERTICAL)
        for color in (wx.RED, wx.GREEN, wx.BLUE):
            hsizer = wx.BoxSizer(wx.HORIZONTAL)
            label = PodLabel(self, "Label String", color)
            hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL)
            hsizer.Add(wx.TextCtrl(self), 1, 
                       wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
            vsizer.Add(hsizer, 0, wx.EXPAND|wx.ALL, 5)
        self.Sizer = vsizer

#-----------------------------------------------------------#

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title)

        sizer = wx.BoxSizer()
        self.panel = MyPanel(self)
        sizer.Add(self.panel, 1, wx.EXPAND)

        self.Sizer = sizer
        self.SetInitialSize()

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Drawing Gradients")
        self.frame.Show()
        return True
    
if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
