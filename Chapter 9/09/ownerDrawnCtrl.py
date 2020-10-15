# Chapter 9: Creating and Customizing Components
# Recipe 9: Designing an owner drawn control
#
import wx

class CaptionBox(wx.PyPanel):
    def __init__(self, parent, caption, flag=wx.VERTICAL):
        super(CaptionBox, self).__init__(parent,
                                         style=wx.NO_BORDER)
        self.Label = caption
        self._csizer = wx.BoxSizer(flag)

        self.__DoLayout()

        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def __DoLayout(self):
        msizer = wx.BoxSizer(wx.VERTICAL)
        tsize = self.GetTextExtent(self.Label)
        msizer.AddSpacer(tsize[1] + 3) # extra space for caption
        msizer.Add(self._csizer, 0, wx.EXPAND|wx.ALL, 8)
        self.SetSizer(msizer)

    def DoGetBestSize(self):
        size = super(CaptionBox, self).DoGetBestSize()
        # Make sure there is room for the label
        tsize = self.GetTextExtent(self.Label)
        size.SetWidth(max(size.width, tsize[0]+20))
        return size

    def AddItem(self, item):
        self._csizer.Add(item, 0, wx.ALL, 5)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        rect = self.ClientRect

        # Get the sytem color to draw the caption
        ss = wx.SystemSettings
        color = ss.GetColour(wx.SYS_COLOUR_ACTIVECAPTION)
        txtcolor = ss.GetColour(wx.SYS_COLOUR_CAPTIONTEXT)
        dc.SetTextForeground(txtcolor)

        # Draw the border
        self.OnDrawBorder(dc, color, rect)

        # Add the Caption
        self.OnDrawCaption(dc, color, rect)

    def OnDrawBorder(self, dc, color, rect):
        rect.Inflate(-2, -2)
        dc.SetPen(wx.Pen(color))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangleRect(rect)

    def OnDrawCaption(self, dc, color, rect):
        tsize = dc.GetTextExtent(self.Label)
        rect = wx.Rect(rect.x, rect.y,
                       rect.width, tsize[1] + 3)
        dc.SetBrush(wx.Brush(color))
        dc.DrawRectangleRect(rect)
        rect.Inflate(-5, 0)
        dc.SetFont(self.GetFont())
        dc.DrawLabel(self.Label, rect, wx.ALIGN_LEFT)

#--------------------------------------------------------------#

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        self.Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self._AddBox("Caption Box 1", wx.VERTICAL)
        self._AddBox("Caption Box 2", wx.HORIZONTAL)

    def _AddBox(self, caption, flag):
        box = CaptionBox(self, caption, flag)

        for x in range(3):
            btn = wx.Button(box, label="Button %d" % x)
            box.AddItem(btn)

        self.Sizer.Add(box, 0, wx.ALL, 20)

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title)

        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        panel = MyPanel(self)
        self.Sizer.Add(panel, 1, wx.EXPAND)

        self.SetInitialSize()

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Owner Drawn Control")
        self.frame.Show()
        return True

if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
