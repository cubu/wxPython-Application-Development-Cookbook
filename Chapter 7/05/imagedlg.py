# Helper module to pick an image to print in the sample
import wx
import wx.lib.imagebrowser as imagebrowser

class ImageDialogFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(ImageDialogFrame, self).__init__(*args, **kwargs)

        # Attributes
        self.panel = ImageDialogPanel(self)

class ImageDialogPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(ImageDialogPanel, self).__init__(*args, **kwargs)

        # Attributes
        self.lastpath = None
        self.bmp = wx.StaticBitmap(self)
        self.btn = wx.Button(self, label="Choose Image")

        # Layout
        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        vsizer.Add(self.bmp, 0, wx.ALIGN_CENTER)
        vsizer.AddSpacer((5, 5))
        vsizer.Add(self.btn, 0, wx.ALIGN_CENTER)
        hsizer.AddStretchSpacer()
        hsizer.Add(vsizer, 0, wx.ALIGN_CENTER)
        hsizer.AddStretchSpacer()
        self.SetSizer(hsizer)

        # Event Handlers
        self.Bind(wx.EVT_BUTTON, self.OnShowDialog, self.btn)

    def OnShowDialog(self, event):
        # Create the dialog with the path cached
        # from the last time it was opened
        dlg = imagebrowser.ImageDialog(self, self.lastpath)
        if dlg.ShowModal() == wx.ID_OK:
            # Save the last used path
            self.lastpath = dlg.GetDirectory()
            imgpath = dlg.GetFile()
            bitmap = wx.Bitmap(imgpath)
            if bitmap.IsOk():
                self.bmp.SetBitmap(bitmap)
                self.Layout()
                self.bmp.Refresh()
        dlg.Destroy()

    def GetBitmap(self):
        return self.bmp.GetBitmap()