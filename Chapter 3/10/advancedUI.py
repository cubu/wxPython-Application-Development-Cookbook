# Chapter 7: Window Layout and Design
# Recipe 10: Advancing your UI with AuiManager
#
import wx
import wx.lib.mixins.listctrl as listmix
import wx.lib.sized_controls as sized
import wx.lib.agw.aui as aui

#-------------------------------------------------------#

class AuiFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(AuiFrame, self).__init__(*args, **kwargs)

        # Attributes
        self._mgr = aui.AuiManager(self)

        # Panels
        self._phone = PhoneDialerPanel(self)
        self._contacts = ContactList(self)
        self._callLog = wx.ListBox(self)

        # Layout
        self.SetupMgr()
        self.SetInitialSize((750, 350))

    def SetupMgr(self):
        # Contacts Pane
        info = aui.AuiPaneInfo().Center().Name("Contacts")
        info = info.CloseButton(False).Caption("Contact List")
        self._mgr.AddPane(self._contacts, info)
        
        # Phone dialer pane
        self._phone.SetInitialSize()
        size = self._phone.BestSize
        info = aui.AuiPaneInfo().Right().Name("Phone")
        info = info.BottomDockable(False).TopDockable(False)
        info = info.Layer(0).Caption("Phone")
        info = info.Fixed().Snappable(True)
        self._mgr.AddPane(self._phone, info)
        
        # Call Log
        info = aui.AuiPaneInfo().Right().Layer(0).Position(1)
        info = info.Name("Log").Caption("Call Log")
        info = info.BestSize(size).MinSize(size)
        self._mgr.AddPane(self._callLog, info)

        # Commit layout to manager
        self._mgr.Update()

#-------------------------------------------------------#

class PhoneDialerPanel(wx.Panel):
    """Panel to hold all phone dialing controls"""
    def __init__(self, parent):
        super(PhoneDialerPanel, self).__init__(parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.display = wx.TextCtrl(self, style=wx.TE_READONLY|wx.TE_RIGHT)
        sizer.Add(self.display, 0, wx.EXPAND)
        
        sizer.Add(PhoneButtonPanel(self), 0, wx.EXPAND)
        
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
        
class PhoneButtonPanel(sized.SizedPanel):
    """Panel based widget to provide phone button input"""
    def __init__(self, parent):
        super(PhoneButtonPanel, self).__init__(parent)

        self.SetSizerType("grid", {"rows":4, "cols":3})
        lbls = ["1", "2", "3", "4", "5", "6", 
                "7", "8", "9", "*", "0", "#"]
        for lbl in lbls:
            btn = wx.Button(self, label=lbl, name=lbl)

#-------------------------------------------------------#

class ContactList(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        super(ContactList, self).__init__(parent, style=wx.LC_REPORT)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

        self.InsertColumn(0, "Last Name")
        self.InsertColumn(1, "First Name")
        self.InsertColumn(2, "Phone #")
        self.InsertColumn(3, "Address")
        # note: resize mixin counts columns starting at 1...
        self.setResizeColumn(4)

#-------------------------------------------------------#

class MyApp(wx.App):
    def OnInit(self):
        self.frame = AuiFrame(None,
                              size=(300,300),
                              title="AuiManager")

        # Stick some mock data in the display
        self.frame._contacts.Append(("Body", "Some", "123-456-7890", "123 Water st."))
        self.frame._contacts.Append(("Python", "wx", "456-789-1011", "34 Library Way."))
        self.frame._contacts.Append(("Manager", "Aui", "121-314-1516", "19 Plain Dr."))
        self.frame._callLog.AppendItems(["12:01am Call Started", "12:16am Call Ended"])

        self.frame.Show()
        return True

if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
