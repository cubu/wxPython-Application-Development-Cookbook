# Chapter 5: Data Displays and Grids
# Recipe 6: Modelling your data
#
import inspect
import wx
import wx.dataview as dv

class HierarchyInfo:
    def __init__(self, item, parent):
        self.item = item
        self.parent = parent

        self.name = item.__name__
        self.docs = item.__doc__
        if self.docs:
            self.docs = self.docs.replace("\n", "")
        self.subs = list()
        
        self._searchSubs()

    def _searchSubs(self):
        if hasattr(self.item, '__subclasses__'):
            for t in self.item.__subclasses__():
                self.subs.append(HierarchyInfo(t, self))

class ClassDataModel(dv.PyDataViewModel):
    def __init__(self, data):
        super(ClassDataModel, self).__init__()
        self.data = data
        self.objmapper.UseWeakRefs(True)

    def GetChildren(self, parent, children):
        # check root node
        if not parent:
            for item in self.data:
                children.append(self.ObjectToItem(item))
            return len(self.data)

        node = self.ItemToObject(parent)
        for item in node.subs:
            children.append(self.ObjectToItem(item))
        return len(node.subs)

    def HasContainerColumns(self, item):
        return True

    def IsContainer(self, item):
        if not item:
            return True

        obj = self.ItemToObject(item)
        return len(obj.subs) > 0

    def GetParent(self, item):
        if not item:
            return dv.NullDataViewItem

        obj = self.ItemToObject(item)
        if obj.parent is None:
            return dv.NullDataViewItem
        else:
            return self.ObjectToItem(obj.parent)
    
    def GetValue(self, item, col):
        obj = self.ItemToObject(item)
        vMap = { 0 : obj.name,
                 1 : len(obj.subs),
                 2 : obj.docs
               }
        return vMap[col]

    def SetValue(self, value, item, col):
        pass

    def GetAttr(self, item, col, attr):
        if col == 1:
            attr.Bold = True
            return True
        return False

#------- Sample Application ---------#

class ClassViewer(wx.Frame):
    def __init__(self, parent, title):
        super(ClassViewer, self).__init__(parent, title=title)

        # Look at all classes in wx namespace
        data = list()
        for x in dir(wx):
            item = getattr(wx, x)
            if inspect.isclass(item):
                data.append(HierarchyInfo(item, None))

        dvc = dv.DataViewCtrl(self, style=dv.DV_VERT_RULES)
        model = ClassDataModel(data)
        dvc.AssociateModel(model)
        
        autosize = wx.COL_WIDTH_AUTOSIZE
        dvc.AppendTextColumn("Class", 0, width=autosize)
        dvc.AppendTextColumn("Subclasses", 1, width=autosize, 
                             align=wx.ALIGN_CENTER)
        dvc.AppendTextColumn("Docstring", 2, width=autosize)

        sizer = wx.BoxSizer()
        sizer.Add(dvc, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetInitialSize((400, 200))
        
class MyApp(wx.App):
    def OnInit(self):
        self.frame = ClassViewer(None, title="DataView Model")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
