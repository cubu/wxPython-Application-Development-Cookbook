# Chapter 5: Data Displays and Grids
# Recipe 3: Creating a data source
#
import urllib
import json
import wx
import wx.grid as gridlib

class MyDataSource(gridlib.PyGridTableBase):
    def __init__(self):
        super(MyDataSource, self).__init__()

        # Github change history for wxPython
        self._RetrieveData()

    def _RetrieveData(self):
        url = "https://api.github.com/repos/RobinD42/wxPython/"
        query = "commits?path=%s&per_page=100"
        changes = query % "CHANGES.txt"
        fp = urllib.urlopen(url+changes)
        headers = dict(fp.info())
        self._data = json.load(fp)

    def GetNumberRows(self):
        """Override to tell grid how many columns to show"""
        return len(self._data)

    def GetNumberCols(self):
        """Override to tell grid how many rows of data there are"""
        return 3

    def GetValue(self, row, col):
        """Get the value for a specific cell from data source"""
        data = self._data[row]['commit']
        keys = { 0 : ('author', 'date'),
                 1 : ('author', 'name'),
                 2 : ('message',) }
        value = ""
        temp = data
        for key in keys[col]:
            value = temp[key]
            temp = value
        return value

    def GetColLabelValue(self, col):
        """Get the label for the column"""
        cols = ["Date", "Name", "Comment"]
        return cols[col]

    def GetRowLabelValue(self, row):
        """Get label for the given row"""
        return abs(self.GetNumberRows() - row)

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title)

        sizer = wx.BoxSizer()
        self._grid = gridlib.Grid(self)
        self._data = MyDataSource()
        self._grid.SetTable(self._data)
        self._grid.EnableEditing(False)
        self._grid.AutoSizeColumns()
        
        sizer.Add(self._grid, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetInitialSize()

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Creating a data source")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
