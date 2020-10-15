# Chapter 7: Requesting and Retrieving Information
# Recipe 1: Selecting files with a FileDialog
#
import wx

# Code from Chapter 2 Working with Toolbars
import chapter2Editor as c2e

class FileEditor(c2e.EditorWithToolBar):
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

#-------------------------------------------------#

class MyApp(wx.App):
    def OnInit(self):
        self.frame = FileEditor(None, title="Using a FileDialog")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
