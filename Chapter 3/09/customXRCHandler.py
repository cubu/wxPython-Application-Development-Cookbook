# Chapter 7: Window Layout and Design
# Recipe 9: Using Xml Resources
#
import wx
import wx.xrc as xrc
import wx.lib.sized_controls as sized

class PhoneBtnPanelHandler(xrc.XmlResourceHandler):
    def CanHandle(self, node):
        return self.IsOfClass(node, "PhoneButtonPanel")

    def DoCreateResource(self):
        panel = PhoneButtonPanel(self.GetParentAsWindow())
        self.SetupWindow(panel)
        self.CreateChildren(panel)
        return panel

class PhoneButtonPanel(sized.SizedPanel):
    """Panel based widget to provide phone button input"""
    def __init__(self, parent):
        super(PhoneButtonPanel, self).__init__(parent)

        self.SetSizerType("grid", {"rows":4, "cols":3})
        lbls = ["1", "2", "3", "4", "5", "6", 
                "7", "8", "9", "*", "0", "#"]
        for lbl in lbls:
            btn = wx.Button(self, label=lbl, name=lbl)

class CustomXmlResource(xrc.XmlResource):
    def __init__(self, fileName):
        super(CustomXmlResource, self).__init__(fileName)
        
        # insert custom handler(s)
        self.InsertHandler(PhoneBtnPanelHandler())

#-------------------------------------------------------#

class PhoneDialog(wx.Dialog):
    """Example usage of the PhonePanel"""
    def __init__(self, parent, title):
        super(PhoneDialog, self).__init__(parent, title=title)
        
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Load the custom resource
        resource = CustomXmlResource("custom.xrc")
        panel = resource.LoadPanel(self, "dialog_panel")
        self.display = panel.FindWindowByName("display")
        sizer.Add(panel, 0, wx.EXPAND)
        
        # Add additional buttons
        bsizer = wx.BoxSizer(wx.HORIZONTAL)
        back = wx.Button(self, name="back")
        back.Bitmap = wx.ArtProvider.GetBitmap(wx.ART_GO_BACK)
        bsizer.Add(back, 1, wx.EXPAND)
        forward = wx.Button(self, name="send")
        forward.Bitmap = wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD)
        bsizer.Add(forward, 1, wx.EXPAND)
        sizer.Add(bsizer, 0, wx.EXPAND)

        self.SetSizer(sizer)
        self.SetInitialSize()

        self.Bind(wx.EVT_BUTTON, self.OnPhoneButton)

    def OnPhoneButton(self, event):
        name = event.EventObject.Name
        if name.isdigit():
            self.display.AppendText(name)
        elif name == "back":
            txt = self.display.Value
            if len(txt):
                txt = txt[0:-1]
                self.display.Value = txt
        elif name == "send":
            print("Calling %s ..." % self.display.Value)

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
        self.button = wx.Button(self, label="Open Phone")

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
        PhoneDialog(self, "PhoneDialog").Show()

if __name__ == '__main__':
    app = XrcTestApp(False)
    app.MainLoop()
