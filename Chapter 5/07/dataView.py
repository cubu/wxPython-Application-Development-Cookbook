# Chapter 5: Data Displays and Grids
# Recipe 7: Displaying your model
#
import inspect
import wx
import wx.dataview as dv

# Recipe 6 module
import dataModel as dm

class ExtendedModel(dm.ClassDataModel):
    def GetValue(self, item, col):
        obj = self.ItemToObject(item)
        bmp = wx.ArtProvider.GetIcon(wx.ART_FOLDER_OPEN, 
                                     wx.ART_MENU, (16,16))
        sf = dv.DataViewIconText(self.getSourceFile(obj), bmp)
        vMap = { 0 : obj.name,
                 1 : len(obj.subs),
                 2 : self.isBase(obj),
                 3 : sf
               }
        return vMap[col]

    def isBase(self, obj):
        bases = obj.item.__bases__
        lcount = len(bases)
        return lcount == 0 or (lcount == 1 and object in bases)

    def getSourceFile(self, obj):
        try:
            return inspect.getsourcefile(obj.item)
        except:
            return "Unknown"

class ClassDataView(dv.DataViewCtrl):
    def __init__(self, parent, data):
        style = dv.DV_ROW_LINES | dv.DV_HORIZ_RULES
        super(ClassDataView, self).__init__(parent, style=style)

        self.model = ExtendedModel(data)
        self.AssociateModel(self.model)

        flags = dv.DATAVIEW_COL_SORTABLE|\
                dv.DATAVIEW_COL_RESIZABLE
        autosize = wx.COL_WIDTH_AUTOSIZE
        self.AppendTextColumn("Class", 0, width=autosize, 
                              flags=flags)
        self.AppendTextColumn("Subclasses", 1, width=autosize, 
                              align=wx.ALIGN_CENTER)
        self.AppendToggleColumn("IsBase", 2, width=autosize)
        self.AppendIconTextColumn("Source File", 3, 
                                  width=autosize, flags=flags)

        self.Bind(dv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, 
                  self.OnContext)

    def OnContext(self, event):
        menu = wx.Menu()
        iconTxt = self.model.GetValue(event.GetItem(), 3)
        fname = iconTxt.GetText()
        menu.Append(wx.ID_OPEN, "Open Module '%s'" % fname)
        
        obj = self.model.ItemToObject(event.GetItem())
        item = menu.Append(wx.ID_ANY, obj.docs)
        item.Enable(False)

        self.PopupMenu(menu)
        menu.Destroy()

#------- Sample Application ---------#

class ClassViewer(wx.Frame):
    def __init__(self, parent, title):
        super(ClassViewer, self).__init__(parent, title=title)

        # Look at all classes in wx namespace
        data = list()
        for x in dir(wx):
            item = getattr(wx, x)
            if inspect.isclass(item):
                data.append(dm.HierarchyInfo(item, None))

        self.dvc = ClassDataView(self, data)
        
        sizer = wx.BoxSizer()
        sizer.Add(self.dvc, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetInitialSize((500, 300))
        
        self.CreateStatusBar()

class MyApp(wx.App):
    def OnInit(self):
        self.frame = ClassViewer(None, title="DataView Control")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
