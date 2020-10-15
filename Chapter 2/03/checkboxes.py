# Chapter 2: Common User Controls
# Recipe 3: Offering options with CheckBoxes
#
import wx

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        # Layout sizers
        vsizer = wx.BoxSizer(wx.VERTICAL)

        # Toggle Button
        self.allCB = wx.CheckBox(self, label="All Selected",
                                 style=wx.CHK_3STATE)
        vsizer.Add(self.allCB)
        self.option1 = wx.CheckBox(self,label="Option 1")
        vsizer.Add(self.option1, flag=wx.LEFT, border=10)
        self.option2 = wx.CheckBox(self, label="Option 2")
        vsizer.Add(self.option2, flag=wx.LEFT, border=10)

        self.SetSizer(vsizer)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)

    def OnCheckBox(self, event):
        check = event.EventObject
        if check is self.allCB:
            self.option1.Value = check.Value
            self.option2.Value = check.Value
        else:
            values = [self.option1.Value, self.option2.Value]
            if all(values):
                self.allCB.Set3StateValue(wx.CHK_CHECKED)
            elif any(values):
                self.allCB.Set3StateValue(wx.CHK_UNDETERMINED)
            else:
                self.allCB.Set3StateValue(wx.CHK_CHECKED)

class MyFrame(wx.Frame):
    def __init__(self, parent, title=""):
        super(MyFrame, self).__init__(parent, title=title)
        
        # Set the panel
        self.panel = MyPanel(self)

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Using Checkboxes")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
