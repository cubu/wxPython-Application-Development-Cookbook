# Chapter 9: Creating and Customizing Components
# Recipe 4: Providing your own Information Window
#
import os
from time import asctime, localtime
import stat
import mimetypes
import wx

class FileInfoDlg(wx.MiniFrame):
    def __init__(self, parent, fname):
        style = wx.DEFAULT_DIALOG_STYLE
        super(FileInfoDlg, self).__init__(parent, 
                                          style=style)

        sizer = wx.BoxSizer()
        panel = FileInfoPanel(self, fname)
        sizer.Add(panel, 1, wx.EXPAND)
        self.Sizer = sizer
        
        self.Title = panel.Label
        self.SetInitialSize()

        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, event):
        self.Destroy()
        event.Skip()

class FileInfoPanel(wx.Panel):
    def __init__(self, parent, fname):
        super(FileInfoPanel, self).__init__(parent)

        self._file = fname
        self.Label = os.path.basename(fname)
        
        self._DoLayout()

    def _DoLayout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)

        bmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, 
                                       wx.ART_CMN_DIALOG)
        staticBmp = wx.StaticBitmap(self, bitmap=bmp)
        sizer.Add(staticBmp, 0, wx.ALIGN_CENTER_HORIZONTAL)
        
        info = self._GetInfo()
        isize = wx.FlexGridSizer(len(info), 2, 3, 5)
        for k,v in info:
            label = wx.StaticText(self, label="%s:" % k)
            isize.Add(label, 0, wx.ALIGN_RIGHT)
            isize.Add(wx.StaticText(self, label=v), 0)
        
        sizer.Add(isize, 0, wx.EXPAND|wx.ALL, 5)
        self.Sizer = sizer

    def _GetInfo(self):
        fstat = os.stat(self._file)
        info = [
        ("Kind", GetFileType(self._file)),
        ("Size", GetSizeLabel(fstat[stat.ST_SIZE])),
        ("Created", asctime(localtime(fstat[stat.ST_CTIME]))),
        ("Modified", asctime(localtime(fstat[stat.ST_MTIME])))
        ]
        return info

def GetSizeLabel(bits):
    val = ('bytes', 'KB', 'MB', 'GB', 'TB')
    ind = 0
    while bits > 1024 and ind < len(val) - 1:
        bits = float(bits) / 1024.0
        ind += 1

    rval = "%.2f" % bits
    rval = rval.rstrip('.0')
    if not rval:
        rval = '0'
    rval = "%s %s" % (rval, val[min(ind, 4)])
    return rval

def GetFileType(fname):
    if os.path.isdir(fname):
        return "Folder"

    mtype = mimetypes.guess_type(fname)[0]
    if mtype is not None:
        return mtype
    else:
        return "Unknown"

#-----------------------------------------------------------#

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.Sizer = sizer
        
class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title)

        self.MenuBar = wx.MenuBar()
        fmenu = wx.Menu()
        fmenu.Append(wx.ID_OPEN, "View file info...")
        self.MenuBar.Append(fmenu, "File")

        sizer = wx.BoxSizer()
        self.panel = MyPanel(self)
        sizer.Add(self.panel, 1, wx.EXPAND)

        self.Sizer = sizer
        self.SetInitialSize((400, 300))
        
        self.Bind(wx.EVT_MENU, self.OnMenu)

    def OnMenu(self, event):
        if event.Id == wx.ID_OPEN:
            dlg = wx.FileDialog(self, "Select File", style=wx.FD_OPEN)
            if dlg.ShowModal() == wx.ID_OK:
                info = FileInfoDlg(self, dlg.GetPath())
                info.Show()
        event.Skip()

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Information Dialog")
        self.frame.Show()
        return True
    
if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
