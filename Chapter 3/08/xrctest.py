# Chapter 7: Window Layout and Design
# Recipe 8: Using Xml Resources
#
import wx
import wx.xrc as xrc

class ResourceDialog(object):
    def __init__(self, parent):
        super(ResourceDialog, self).__init__()

        resource = xrc.XmlResource("xrcdlg.xrc")
        self.dlg = resource.LoadDialog(parent, "xrctestdlg")
        
        checkId = resource.GetXRCID("check_box")
        self.dlg.Bind(wx.EVT_CHECKBOX, self.OnCheck, id=checkId)
    
    def OnCheck(self, event):
        print("Checked: %s" % event.IsChecked())

    def ShowModal(self):
        result = self.dlg.ShowModal()
        if result == wx.ID_OK:
            print("Ok Clicked!")
        else:
            print("Cancel Clicked!")

#-------------------------------------------------------#

class XrcTestApp(wx.App):
    def OnInit(self):
        self.frame = XrcTestFrame(None,
                                  size=(300,300),
                                  title="Using Xrc")
        self.frame.Show()
        return True

class XrcTestFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(XrcTestFrame, self).__init__(*args, **kwargs)

        # Attributes
        self.panel = XrcTestPanel(self)

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)

class XrcTestPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(XrcTestPanel, self).__init__(*args, **kwargs)

        # Attributes
        self.button = wx.Button(self, label="Show Dialog")

        # Layout
        self._DoLayout()

        # Event Handlers
        self.Bind(wx.EVT_BUTTON, self.OnShowDialog)

    def _DoLayout(self):
        """Layout the controls"""
        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        vsizer.AddStretchSpacer()
        hsizer.AddStretchSpacer()
        hsizer.Add(self.button)
        hsizer.AddStretchSpacer()
        vsizer.Add(hsizer, 0, wx.EXPAND)
        vsizer.AddStretchSpacer()

        # Finally assign the main outer sizer to the panel
        self.SetSizer(vsizer)

    def OnShowDialog(self, event):
        ResourceDialog(self).ShowModal()

if __name__ == '__main__':
    app = XrcTestApp(False)
    app.MainLoop()
