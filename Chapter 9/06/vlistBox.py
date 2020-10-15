# Chapter 9: Creating and Customizing Components
# Recipe 6: Drawing your own list control
#
import wx

class UserInfo(object):
    def __init__(self, name, email):
        super(UserInfo, self).__init__()

        self.name = name
        self.email = email

class UserListBox(wx.VListBox):
    def __init__(self, parent, users):
        super(UserListBox, self).__init__(parent)

        self.bmp = wx.Bitmap("system-users.png",
                             wx.BITMAP_TYPE_PNG)
        self.bh = self.bmp.GetHeight()
        self.users = users

        self.SetItemCount(len(self.users))

    def OnMeasureItem(self, index):
        bmpHeight = self.bh + 4
        nsize = self.GetTextExtent(self.users[index].name)
        esize = self.GetTextExtent(self.users[index].email)
        return max(bmpHeight, nsize[1] + esize[1] + 6)

    def OnDrawSeparator(self, dc, rect, index):
        oldpen = dc.GetPen()
        dc.SetPen(wx.Pen(wx.BLACK))
        dc.DrawLine(rect.x, rect.y,
                    rect.x + rect.width,
                    rect.y)
        rect.Deflate(0, 2)
        dc.SetPen(oldpen)

    def OnDrawItem(self, dc, rect, index):
        # Draw the bitmap
        dc.DrawBitmap(self.bmp, rect.x + 2,
                      ((rect.height - self.bh) / 2) + rect.y)
        # Draw the name label to the right of the bitmap
        textx = rect.x + 2 + self.bh + 2
        lblrect = wx.Rect(textx, rect.y,
                          rect.width - textx,
                          rect.height)
        user = self.users[index]
        dc.DrawLabel(user.name, lblrect,
                     wx.ALIGN_LEFT|wx.ALIGN_TOP)
        dc.DrawLabel(user.email, lblrect,
                     wx.ALIGN_LEFT|wx.ALIGN_BOTTOM)

    def AddItem(self, user):
        self.users.append(user)
        self.SetItemCount(len(self.users))

    def GetItem(self, index):
        return self.users[index]

    def RemoveItem(self, index):
        self.users.remove(index)
        self.SetItemCount(len(self.users))

#--------------------------------------------------------------#

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title)

        userLst = [ UserInfo(name, "%s@email.com" % name)
                    for name in ["George", "Toshio", "Mary", "Frank",
                                 "Susan", "Sally", "Jeff" ] ]
        userLst.append(UserInfo("Test", ""))
        self.lst = UserListBox(self, userLst)
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self.lst, 1, wx.EXPAND)

        self.Bind(wx.EVT_LISTBOX, self.OnSelectionChange)

    def OnSelectionChange(self, event):
        index = event.Selection
        print "selected: %s" % self.lst.GetItem(index).name

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Virtual ListBox")
        self.frame.Show()
        return True
    
if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
