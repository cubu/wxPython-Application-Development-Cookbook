# Chapter 5: Data Displays and Grids
# Recipe 1: Displaying lists of data
#
import wx

class BaseList(wx.ListCtrl):
    def __init__(self, parent):
        super(BaseList, self).__init__(parent, 
                                       style=wx.LC_REPORT)

        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRClick)
        self.Bind(wx.EVT_MENU, self.OnMenu, id=wx.ID_COPY)
        self.Bind(wx.EVT_MENU, self.OnMenu, id=wx.ID_SELECTALL)

    def OnRClick(self, event):
        menu = wx.Menu()
        menu.Append(wx.ID_COPY)
        menu.Append(wx.ID_SELECTALL)
        self.PopupMenu(menu)
        menu.Destroy()

    def OnMenu(self, event):
        if event.Id == wx.ID_COPY:
            self.Copy()
        elif event.Id == wx.ID_SELECTALL:
            self.SelectAll()
        else:
            event.Skip()

    def Copy(self):
        """Copy selected data to clipboard"""
        text = self.GetSelectedText()
        data_o = wx.TextDataObject()
        data_o.SetText(text)
        if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():
            wx.TheClipboard.SetData(data_o)
            wx.TheClipboard.Flush()
            wx.TheClipboard.Close()

    def GetSelectedText(self):
        items = list()
        nColumns = self.ColumnCount
        for item in range(self.ItemCount):
            if self.IsSelected(item):
                items.append(self.GetRowText(item))
        text = "\n".join(items)
        return text

    def GetRowText(self, idx):
        txt = list()
        for col in range(self.ColumnCount):
            txt.append(self.GetItemText(idx, col))
        return "\t".join(txt)

    def SelectAll(self):
        """Select all items"""
        for item in range(self.ItemCount):
            self.Select(item, 1)

class PersonnelList(BaseList):
    def __init__(self, parent):
        super(PersonnelList, self).__init__(parent)

        # Add column headers
        self.InsertColumn(0, "ID")
        self.InsertColumn(1, "Name")
        self.InsertColumn(2, "Email")
        self.InsertColumn(3, "Phone#")
    
    def AddEmployee(self, id, name, email, phone):
        item = self.Append((id, name, email, phone))

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title)

        self._list = PersonnelList(self)
        
        # add some data
        self._list.AddEmployee("123", "Frank", "f@email.com", "555-1234")
        self._list.AddEmployee("124", "Jane", "j@email.com", "555-1434")
        self._list.AddEmployee("125", "Thor", "t@email.com", "555-1274")

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Displaying lists of data")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
