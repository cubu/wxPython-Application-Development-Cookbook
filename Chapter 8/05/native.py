# Chapter 8: User Interface Primitives
# Recipe 5: Recreating native controls with RendererNative
#
import wx

class CustomCheckBox(wx.PyControl):
    def __init__(self, parent, label, style=0):
        style |= wx.NO_BORDER
        super(CustomCheckBox, self).__init__(parent,
                                             style=style)
        self.Label = label
        self._value = False
        self._style = style
        self._clickIn = False

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_ENTER_WINDOW, 
                  lambda event: self.Refresh())
        self.Bind(wx.EVT_LEAVE_WINDOW, 
                  lambda event: self.Refresh())

    def GetValue(self):
        return self._value

    def SetValue(self, value):
        self._value = value

    Value = property(GetValue, SetValue)

    def OnLeftDown(self, event):
        self._clickIn = True

    def OnLeftUp(self, event):
        if self._clickIn:
            self.Value = not self.Value
        self._clickIn = False

        # generate a checkbox event
        etype = wx.wxEVT_COMMAND_CHECKBOX_CLICKED
        event = wx.CommandEvent(etype)
        event.EventObject = self
        event.Checked = self.Value
        self.ProcessEvent(event)

        self.Refresh()

    def DoGetBestSize(self):
        txtsz = self.GetTextExtent(self.Label)
        cboxsz = (16, 16)
        size = None
        if self._style & wx.ALIGN_BOTTOM:
            size = wx.Size(txtsz[0] + 4, 
                           txtsz[1] + cboxsz[1] + 6)
        else:
            size = wx.Size(txtsz[0] + cboxsz[0] + 6,
                           max(txtsz[1], cboxsz[1]) + 4)
        return size

    def GetFlags(self):
        flag = 0
        pt = self.ScreenToClient(wx.GetMousePosition())
        hitResult = self.HitTest(pt)

        if not self.Enabled:
            flag |= wx.CONTROL_DISABLED
        elif hitResult == wx.HT_WINDOW_INSIDE:
            flag |= wx.CONTROL_CURRENT

        if self.Value:
            flag |= wx.CONTROL_CHECKED
        return flag

    def OnPaint(self, event):
        dc = wx.GCDC(wx.PaintDC(self))
        renderer = wx.RendererNative.Get()
        txtsz = dc.GetTextExtent(self.Label)
        cboxsz = (16, 16)
        
        cx, cy, lx, ly = 2, 2, 2, 2
        if self._style & wx.ALIGN_BOTTOM:
            cx += (self.Rect.Width / 2) - (cboxsz[0] / 2)
            ly += cboxsz[1]
        else:
            cy += (self.Rect.Height / 2) - (cboxsz[1] / 2)
            lx += (2 + cboxsz[0])
            ly += (self.Rect.Height / 2) - (txtsz[1] / 2)

        cboxRect = wx.Rect(cx, cy, cboxsz[0], cboxsz[1])
        flag = self.GetFlags()
        renderer.DrawCheckBox(self, dc, cboxRect, flag)

        dc.DrawText(self.Label, lx, ly)

#-----------------------------------------------------------#

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add((20,20))

        cbox = CustomCheckBox(self, "Custom CheckBox 1", wx.ALIGN_BOTTOM)
        vsizer.Add(cbox, 0, wx.ALL, 5)
        
        vsizer.Add((20,20))

        cbox2 = CustomCheckBox(self, "Custom CheckBox 2")
        vsizer.Add(cbox2, 0, wx.ALL, 5)
        
        vsizer.Add((20,20))
        
        cbox = wx.CheckBox(self, label="Normal Checkbox")
        vsizer.Add(cbox, 0, wx.ALL, 5)

        self.Sizer = vsizer
        self.Bind(wx.EVT_CHECKBOX, self.OnCheck)

    def OnCheck(self, event):
        print "'%s' was clicked" % event.EventObject.Label

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
        self.frame = MyFrame(None, title="RendererNative")
        self.frame.Show()
        return True
    
if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
