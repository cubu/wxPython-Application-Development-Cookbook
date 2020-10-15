# Chapter 2: Common User Controls
# Recipe 8: Displaying a context menu
#
import wx

class ContextMenuMgr(object):
    def __init__(self, parent):
        super(ContextMenuMgr, self).__init__()

        assert isinstance(parent, wx.Window)
        assert hasattr(parent, 'GetPopupMenu'), \
               "parent must implement GetPopupMenu"
        
        self.window = parent
        self.window.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)

    def OnContextMenu(self, event):
        menu = self.window.GetPopupMenu()
        if menu:
            self.window.PopupMenu(menu)
            menu.Destroy()

# define some menu ids for our examples
ID_BLUE = wx.NewId()
ID_RED = wx.NewId()

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        self._menuMgr = ContextMenuMgr(self)

        self.Bind(wx.EVT_MENU, self.OnMenu)

    def OnMenu(self, event):
        evtId = event.Id
        if evtId == ID_BLUE:
            self.BackgroundColour = wx.BLUE
            self.Refresh()
        elif evtId == ID_RED:
            self.BackgroundColour = wx.RED
            self.Refresh()
        else:
            event.Skip()

    def GetPopupMenu(self):
        menu = wx.Menu()
        menu.Append(ID_BLUE, "Blue")
        menu.Append(ID_RED, "Red")
        return menu

#----------------------------------------------------------#

class MyFrame(wx.Frame):
    def __init__(self, parent, title=""):
        super(MyFrame, self).__init__(parent, title=title)
        self.panel = MyPanel(self)

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Menus and Accelerators")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
