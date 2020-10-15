# Chapter 4: Containers and Advanced Controls
# Recipe 7: Displaying hierarchical data with the TreeCtrl
#
import xml.etree.ElementTree as ET
import wx

class XMLOutliner(wx.TreeCtrl):
    def __init__(self, parent, xmlText):
        super(XMLOutliner, self).__init__(parent)
        
        rootElement = ET.fromstring(xmlText)
        root = rootElement.tag
        self._root = self.AddRoot(root)
        self.SetPyData(self._root, rootElement)
        self._populateTree(self._root, rootElement)
        
        self.Bind(wx.EVT_TREE_ITEM_GETTOOLTIP, self.OnToolTip)

    def _populateTree(self, parentNode, element):
        for child in element:
            node = self.AppendItem(parentNode, child.tag)
            self.SetPyData(node, element)
            self._populateTree(node, child)

    def _getDetails(self, element):
        xmlText = ET.tostring(element)
        items = xmlText.split('\n')
        return items[0]

    def OnToolTip(self, event):
        node = event.GetItem()
        data = self.GetPyData(node)
        tip = self._getDetails(data)
        event.SetToolTip(tip)

class XMLViewer(wx.Frame):
    def __init__(self, parent, title):
        super(XMLViewer, self).__init__(parent, title=title)

        xmlText = open("xrcdlg.xrc", "r").read()
        self._tree = XMLOutliner(self, xmlText)
        self._tree.ExpandAll()

class MyApp(wx.App):
    def OnInit(self):
        self.frame = XMLViewer(None, title="XML Viewer")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
