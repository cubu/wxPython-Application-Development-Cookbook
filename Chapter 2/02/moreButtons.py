# Chapter 2: Common User Controls
# Recipe 2: Pushing all the buttons
#
import wx
import wx.lib.platebtn as platebtn

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        # Layout sizers
        vsizer = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        vsizer.Add(sizer)

        # Toggle Button
        toggle = wx.ToggleButton(self, label="Toggle Me")
        sizer.Add(toggle)
        toggle = wx.ToggleButton(self, label="Me Too")
        sizer.Add(toggle)

        # PlateButton
        plate = platebtn.PlateButton(self, label="PlateButton")
        sizer.Add(plate)

        plate = platebtn.PlateButton(self, label="WithMenu")
        menu = wx.Menu("Action Menu")
        menu.Append(wx.ID_OPEN, "Open it")
        menu.Append(wx.ID_CLOSE, "Close it")
        plate.SetMenu(menu)
        sizer.Add(plate)

        # Command Link Button
        note = """Long detail message that informs user
more about what this action does."""
        cmdLnk = wx.CommandLinkButton(self, mainLabel="CommandLink",
                                      note=note)
        vsizer.Add(cmdLnk)

        self.SetSizer(vsizer)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnToggle)
        self.Bind(wx.EVT_BUTTON, self.OnButton)

    def OnToggle(self, event):
        button = event.EventObject
        print("%s toggle button was pushed!" % button.Label)
        print("ToggleState: %s" % button.Value)

    def OnButton(self, event):
        button = event.EventObject
        print("%s was pushed!" % button.Label)
        event.Skip()

class MyFrame(wx.Frame):
    def __init__(self, parent, title=""):
        super(MyFrame, self).__init__(parent, title=title)
        
        # Set the panel
        self.panel = MyPanel(self)

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="More Buttons")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
