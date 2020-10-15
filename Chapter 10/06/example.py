# Chapter 10: Getting your Application Ready for Release
# Recipe 6: Embedding your resources - example usage application
#
import wx
import resource

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title)

        panel = ImagePanel(self)
        sizer = wx.BoxSizer()
        sizer.Add(panel, 1, wx.EXPAND)
        self.Sizer = sizer
        
        self.SetInitialSize()

class ImagePanel(wx.Panel):
    def __init__(self, parent):
        super(ImagePanel, self).__init__(parent)

        sz = wx.BoxSizer()
        sb = wx.StaticBitmap(self, 
                             bitmap=resource.FaceGlasses.Bitmap)
        sz.Add(sb, 0, wx.ALIGN_CENTER|wx.ALL, 100)
        self.Sizer = sz

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, "Embedded Resource Usage")
        self.frame.Show()
        return True

if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
