# Chapter 7: Requesting and Retrieving Information
# Recipe 3: Filtering through the choices
#
import wx
import wx.lib.itemspicker as IP

class ListMaker(wx.Frame):
    def __init__(self, parent, choices, title):
        super(ListMaker, self).__init__(parent, title=title)

        style = IP.IP_REMOVE_FROM_CHOICES
        self.picker = IP.ItemsPicker(self, choices=choices, 
                                     ipStyle=style)
        style = wx.TE_RICH2|wx.TE_MULTILINE
        self.txt = wx.TextCtrl(self, style=style)
        
        self._DoLayout()
        self.picker.Bind(IP.EVT_IP_SELECTION_CHANGED, 
                         self.OnChange)

    def _DoLayout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.picker, 1, wx.EXPAND)
        sizer.Add(self.txt, 1, wx.EXPAND)
        self.Sizer = sizer
        self.SetInitialSize()

    def OnChange(self, event):
        msg = "Shopping List:\n\n"
        items = "\n".join(event.GetItems())
        self.txt.Value = msg + items

#-------------------------------------------#

class MyApp(wx.App):
    def OnInit(self):
        choices = ["Apples", "Oranges", "Strawberries",
                   "Eggs", "Bread", "Milk", "Cheese" ]
        self.frame = ListMaker(None, choices, title="Filtering choices")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
