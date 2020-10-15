# This file contains the cumulative code of the text editor
# that has been extended with recipes since Chapter 2.
#
# This file is used as a library module for other recipes.
import wx

ArtMap = { wx.ID_CUT : wx.ART_CUT,
           wx.ID_COPY : wx.ART_COPY,
           wx.ID_PASTE : wx.ART_PASTE,
           wx.ID_OPEN : wx.ART_FILE_OPEN,
           wx.ID_SAVE : wx.ART_FILE_SAVE,
           wx.ID_EXIT : wx.ART_QUIT,
         }

##------- Example Code adapted from Recipe 7 -----------##

class EasyMenu(wx.Menu):
    def AddEasyItem(self, id, label=""):
        item = wx.MenuItem(self, id, label)
        art = ArtMap.get(id, None)
        if art is not None:
            bmp = wx.ArtProvider.GetBitmap(art, wx.ART_MENU)
            if bmp.IsOk():
                item.SetBitmap(bmp)
        return self.AppendItem(item)

class Editor(wx.Frame):
    def __init__(self, parent, title=""):
        super(Editor, self).__init__(parent, title=title)
        
        # Setup the menus
        menubar = wx.MenuBar()
        self.DoSetupMenus(menubar)
        self.SetMenuBar(menubar)

        # Set the main panel
        self.txt = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_RICH2)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.txt, 1, wx.EXPAND)
        self.Sizer = sizer

    def DoSetupMenus(self, menubar):
        fileMenu = EasyMenu()
        self.RegisterMenuAction(fileMenu, wx.ID_OPEN, self.OnFile)
        self.RegisterMenuAction(fileMenu, wx.ID_SAVE, self.OnFile)
        fileMenu.AppendSeparator()
        self.RegisterMenuAction(fileMenu, wx.ID_EXIT, self.OnFile, 
                                "Exit\tCtrl+Q")
        menubar.Append(fileMenu, "File")

        editMenu = EasyMenu()
        self.RegisterMenuAction(editMenu, wx.ID_CUT, self.OnEdit)
        self.RegisterMenuAction(editMenu, wx.ID_COPY, self.OnEdit)
        self.RegisterMenuAction(editMenu, wx.ID_PASTE, self.OnEdit)
        menubar.Append(editMenu, "Edit")

    def RegisterMenuAction(self, menu, id, handler, label=""):
        item = menu.AddEasyItem(id, label)
        self.Bind(wx.EVT_MENU, handler, item)

    def OnFile(self, event):
        if event.Id == wx.ID_OPEN:
            raise NotImplementedError("Open not implemented")
        elif event.Id == wx.ID_SAVE:
            raise NotImplementedError("Save not implemented")
        elif event.Id == wx.ID_EXIT:
            self.Close()
        else:
            event.Skip()

    def OnEdit(self, event):
        action = { wx.ID_CUT : self.txt.Cut,
                   wx.ID_COPY : self.txt.Copy,
                   wx.ID_PASTE : self.txt.Paste }
        if action.has_key(event.Id):
            action.get(event.Id)()
        else:
            event.Skip()

##------- New Recipe 9 Code ---------------------##

class EasyToolBar(wx.ToolBar):
    def AddEasyTool(self, id, label=""):
        art = ArtMap.get(id, None)
        if art is not None:
            bmp = wx.ArtProvider.GetBitmap(art, wx.ART_TOOLBAR)
            if bmp.IsOk():
                self.AddSimpleTool(id, bmp)

class EditorWithToolBar(Editor):
    def __init__(self, parent, title=""):
        super(EditorWithToolBar, self).__init__(parent, title)

        # Add in the toolbar
        toolbar = EasyToolBar(self)
        self.DoSetupToolBar(toolbar)
        self.SetToolBar(toolbar)
        toolbar.Realize()

    def DoSetupToolBar(self, toolbar):
        toolbar.AddEasyTool(wx.ID_OPEN)
        toolbar.AddEasyTool(wx.ID_SAVE)
        toolbar.AddSeparator()
        toolbar.AddEasyTool(wx.ID_CUT)
        toolbar.AddEasyTool(wx.ID_COPY)
        toolbar.AddEasyTool(wx.ID_PASTE)

#-------------------------------------------------#

class FileEditor(EditorWithToolBar):
    def __init__(self, parent, title):
        super(FileEditor, self).__init__(parent, title)
        
        types = ["Python (*.py)|*.py",
                 "Text Files (*.txt)|*.txt"]
        self.wildcard = "|".join(types)
        self._file = None

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, value):
        self._file = value
        if self._file:
            self.Title = self._file

    def OnFile(self, event):
        """Override base event handler"""
        if event.Id == wx.ID_OPEN:
            self.OpenFile()
        elif event.Id == wx.ID_SAVE:
            self.SaveFile()
        else:
            super(FileEditor, self).OnFile(event)

    def OpenFile(self):
        dlg = wx.FileDialog(self, "Open File", 
                            wildcard=self.wildcard, 
                            style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            with open(path, "rb") as handle:
                text = handle.read()
                self.txt.SetValue(text)
                self.file = path
        dlg.Destroy()

    def SaveFile(self):
        if self.txt.IsModified():
            if self.file is None:
                # Save As
                style = wx.FD_SAVE|wx.OVERWRITE_PROMPT
                dlg = wx.FileDialog(self, "Save As", 
                                    wildcard=self.wildcard, 
                                    style=style)
                if dlg.ShowModal() == wx.ID_OK:
                    self.file = dlg.GetPath()
            self.WriteToDisk(self.file)

    def WriteToDisk(self, fileName):
        with open(fileName, "wb") as handle:
            handle.write(self.txt.Value)
            self.file = fileName
