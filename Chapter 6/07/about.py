# Chapter 6: Ways to Notify and Alert
# Recipe 7: Showing information about your app
#
import wx
import sys

class AboutRecipeFrame(wx.Frame):
    def __init__(self, parent, title):
        super(AboutRecipeFrame, self).__init__(parent, title=title)

        # Attributes
        self.panel = wx.Panel(self)

        # Setup Menus
        menubar = wx.MenuBar()
        helpmenu = wx.Menu()
        helpmenu.Append(wx.ID_ABOUT, "About")
        menubar.Append(helpmenu, "Help")
        self.SetMenuBar(menubar)

        # Setup StatusBar
        self.CreateStatusBar()
        self.PushStatusText("See About in the Menu")

        # Event Handlers
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)

    def OnAbout(self, event):
        """Show the about dialog"""
        info = wx.AboutDialogInfo()

        # Make a template for the description
        desc = ["\nwxPython Cookbook Chapter 6\n",
                "Platform Info: (%s,%s)",
                "License: Public Domain"]
        desc = "\n".join(desc)

        # Get the platform information
        py_version = [sys.platform,
                      ", Python ",
                      sys.version.split()[0]]
        platform = list(wx.PlatformInfo[1:])
        platform[0] += (" " + wx.VERSION_STRING)
        wx_info = ", ".join(platform)

        # Populate with information
        info.SetName("AboutBox Recipe")
        info.SetVersion("1.0")
        info.SetCopyright("Copyright (C) Joe Programmer")
        info.SetDescription(desc % (py_version, wx_info))

        # Create and show the dialog
        wx.AboutBox(info)

class AboutRecipeApp(wx.App):
    def OnInit(self):
        self.frame = AboutRecipeFrame(None,
                                      title="AboutDialog")
        self.frame.Show()
        return True

#------------------------------------------------------#

if __name__ == "__main__":
    app = AboutRecipeApp(False)
    app.MainLoop()
