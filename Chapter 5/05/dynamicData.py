# Chapter 5: Data Displays and Grids
# Recipe 5: Displaying dynamic data
#
import os
import stat
import time
import wx
import wx.grid as gridlib

class FileInfo:
    def __init__(self, path):
        self.path = path
        fstat = os.stat(path)
        ltime = time.localtime(fstat[stat.ST_MTIME])
        self.modified = time.asctime(ltime)
        self.type = "Directory" if os.path.isdir(path) else "File"
        self.size = self.DisplaySize(fstat[stat.ST_SIZE])

    def DisplaySize(self, bits):
        for unit in ['B','KB','MB','GB']:
            if abs(bits) < 1024.0:
                return "%3.1f%s" % (bits, unit)
            bits /= 1024.0
        return "%.1f%s" % (bits, 'TB')

class DirDataSource(gridlib.PyGridTableBase):
    def __init__(self, directory):
        super(DirDataSource, self).__init__()

        self._dir = directory
        self._snapshot = os.listdir(self._dir)
        self._timer = wx.Timer()
        self._timer.Start(1000)
        
        self._timer.Bind(wx.EVT_TIMER, self.OnRefresh)

    def GetNumberRows(self):
        return len(self._snapshot)

    def GetNumberCols(self):
        return 4 # file, modified, type, size

    def GetValue(self, row, col):
        fname = self._snapshot[row]
        path = os.path.join(self._dir, fname)
        info = FileInfo(path)
        val = [fname, info.modified, info.type, info.size]
        return val[col]

    def GetColLabelValue(self, col):
        cols = ("File", "Modified", "Type", "Size")
        return cols[col]

    def OnRefresh(self, event):
        currentData = os.listdir(self._dir)
        if currentData == self._snapshot:
            return # no change

        curNumRows = len(self._snapshot)
        newNumRows = len(currentData)
        self._snapshot = currentData

        if curNumRows != newNumRows:
            self.ProcessUpdates(curNumRows, newNumRows)

        msgId = gridlib.GRIDTABLE_REQUEST_VIEW_GET_VALUES
        msg = gridlib.GridTableMessage(self, msgId) 
        self.View.ProcessTableMessage(msg)

    def ProcessUpdates(self, curNumRows, newNumRows):
        self.View.BeginBatch()
        if newNumRows < curNumRows:
            msg = gridlib.GridTableMessage(self,
                        gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,
                        curNumRows - newNumRows,
                        curNumRows - newNumRows)
            self.View.ProcessTableMessage(msg)

        if newNumRows > curNumRows:
            msg = gridlib.GridTableMessage(self,
                        gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED,
                        newNumRows - curNumRows)
            self.View.ProcessTableMessage(msg)
        self.View.EndBatch()

#------- Sample Application ---------#

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title)

        sizer = wx.BoxSizer()
        self._grid = gridlib.Grid(self)
        
        spaths = wx.StandardPaths_Get();
        temp = spaths.GetTempDir()
        self._table = DirDataSource(temp)
        
        self._grid.SetTable(self._table)
        self._grid.AutoSizeColumns()
        self._grid.EnableEditing(False)
        
        sizer.Add(self._grid, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetInitialSize((-1,400))
        
class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Data Grid")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
