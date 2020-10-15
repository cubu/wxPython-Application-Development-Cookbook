# Chapter 7: Requesting and Retrieving Information
# Recipe 2: Searching text with a FindReplaceDialog
#
import wx
import fileEditor as FE # previous recipe module

# extend the art map
FE.ArtMap[wx.ID_FIND] = wx.ART_FIND
FE.ArtMap[wx.ID_REPLACE] = wx.ART_FIND_AND_REPLACE

class TextEditorWithFind(FE.FileEditor):
    def __init__(self, parent, title):
        super(TextEditorWithFind, self).__init__(parent, title)

        self.finddlg = None
        self.finddata = wx.FindReplaceData()
        self._SetupFindActions()

    def _SetupFindActions(self):
        menub = self.MenuBar
        editMenu = menub.GetMenu(1)
        editMenu.AppendSeparator()
        self.RegisterMenuAction(editMenu, wx.ID_FIND, self.OnEdit)
        self.RegisterMenuAction(editMenu, wx.ID_REPLACE, self.OnEdit)
        
        toolb = self.ToolBar
        toolb.AddSeparator()
        toolb.AddEasyTool(wx.ID_FIND)
        toolb.AddEasyTool(wx.ID_REPLACE)
        toolb.Realize()

        # Find Dialog actions
        self.Bind(wx.EVT_FIND, self.OnFind)
        self.Bind(wx.EVT_FIND_NEXT, self.OnFind)
        self.Bind(wx.EVT_FIND_REPLACE, self.OnReplace)
        self.Bind(wx.EVT_FIND_REPLACE_ALL, self.OnReplaceAll)
        self.Bind(wx.EVT_FIND_CLOSE, self.OnFindClose)

    def _InitFindDialog(self, mode):
        if self.finddlg:
            self.finddlg.Destroy()
        style = (wx.FR_NOUPDOWN|wx.FR_NOMATCHCASE
                 |wx.FR_NOWHOLEWORD)
        if mode == wx.ID_REPLACE:
            style |= wx.FR_REPLACEDIALOG
            title = "Find/Replace"
        else:
            title = "Find"
        dlg = wx.FindReplaceDialog(self, self.finddata,
                                   title, style)
        self.finddlg = dlg

    def OnEdit(self, event):
        if event.Id in (wx.ID_FIND, wx.ID_REPLACE):
            self._InitFindDialog(event.Id)
            self.finddlg.Show()
        else:
            super(TextEditorWithFind, self).OnEdit(event)

    def OnFind(self, event):
        findstr = self.finddata.GetFindString()
        if not self.FindString(findstr):
            wx.Bell() # beep at the user for no match

    def OnReplace(self, event):
        rstring = self.finddata.GetReplaceString()
        fstring = self.finddata.GetFindString()
        cpos = self.GetInsertionPoint()
        start, end = cpos, cpos
        if fstring:
            if self.FindString(fstring):
                start, end = self.txtctrl.GetSelection()
        self.txtctrl.Replace(start, end, rstring)

    def OnReplaceAll(self, event):
        rstring = self.finddata.GetReplaceString()
        fstring = self.finddata.GetFindString()
        text = self.txt.GetValue()
        newtext = text.replace(fstring, rstring)
        self.txt.SetValue(newtext)

    def OnFindClose(self, event):
        if self.finddlg:
            self.finddlg.Destroy()

    def FindString(self, findstr):
        text = self.txt.GetValue()
        csel = self.txt.GetSelection()
        if csel[0] != csel[1]:
            cpos = max(csel)
        else:
            cpos = self.txt.GetInsertionPoint()

        if cpos == self.txt.GetLastPosition():
            cpos = 0

        # Simple case insensitive search
        text = text.upper()
        findstr = findstr.upper()
        found = text.find(findstr, cpos)
        if found != -1:
            end = found + len(findstr)
            self.txt.SetSelection(end, found)
            self.txt.SetFocus()
            return True
        return False

#-------------------------------------------------#

class MyApp(wx.App):
    def OnInit(self):
        self.frame = TextEditorWithFind(None, title="Find and Replace")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
