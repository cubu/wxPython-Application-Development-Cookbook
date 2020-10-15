# Chapter 6: Retrieving Information from Users, Common Dialogs
# Recipe 5: PrintDialog
#
import wx

# Recipe 4's sample module
import imagedlg

class PrintBitmapFrame(imagedlg.ImageDialogFrame):
    def __init__(self, *args, **kwargs):
        super(PrintBitmapFrame, self).__init__(*args, **kwargs)

        # Attributes
        self.printer = BitmapPrinter(self)

        # Setup
        menub = wx.MenuBar()
        filemenu = wx.Menu()
        filemenu.Append(wx.ID_PAGE_SETUP, "Page Setup")
        filemenu.Append(wx.ID_PREVIEW_PRINT, "Print Preview")
        filemenu.Append(wx.ID_PRINT, "Print\tCtrl+P")
        menub.Append(filemenu, "File")
        self.SetMenuBar(menub)

        # Event Handlers
        self.Bind(wx.EVT_MENU, self.OnMenu)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI)

    def OnMenu(self, event):
        """Handle the Print actions"""
        bmp = self.panel.GetBitmap()
        if event.Id == wx.ID_PAGE_SETUP:
            self.printer.PageSetup()
        elif event.Id == wx.ID_PRINT:
            self.printer.Print(bmp)
        elif event.Id == wx.ID_PREVIEW_PRINT:
            self.printer.Preview(bmp)
        else:
            event.Skip()

    def OnUpdateUI(self, event):
        if event.Id in (wx.ID_PRINT,
                        wx.ID_PREVIEW_PRINT):
            # Only enable print when there is a bitmap
            bmp = self.panel.GetBitmap()
            event.Enable(bmp.IsOk())
        else:
            event.Skip()

#---- Printer Classes ----#

class BitmapPrinter(object):
    def __init__(self, parent):
        super(BitmapPrinter, self).__init__()

        self.parent = parent
        self.print_data = wx.PrintData()

    def CreatePrintout(self, bmp):
        assert bmp.IsOk(), "Invalid Bitmap!"
        data = wx.PageSetupDialogData(self.print_data)
        return BitmapPrintout(bmp, data)

    def PageSetup(self):
        # Make a copy of our print data for the setup dialog
        dlg_data = wx.PageSetupDialogData(self.print_data)
        print_dlg = wx.PageSetupDialog(self.parent, dlg_data)
        if print_dlg.ShowModal() == wx.ID_OK:
            # Update the printer data
            newdata = dlg_data.GetPrintData()
            self.print_data = wx.PrintData(newdata)
            paperid = dlg_data.GetPaperId()
            self.print_data.SetPaperId(paperid)
        print_dlg.Destroy()

    def Preview(self, bmp):
        printout = self.CreatePrintout(bmp)
        printout2 = self.CreatePrintout(bmp)
        preview = wx.PrintPreview(printout, printout2,
                                  self.print_data)
        preview.SetZoom(100)
        if preview.IsOk():
            pre_frame = wx.PreviewFrame(preview,
                                        self.parent,
                                        "Print Preview")
            # Default size of the preview frame needs help
            dsize = wx.GetDisplaySize()
            width = self.parent.GetSize()[0]
            height = dsize.GetHeight() - 100
            pre_frame.SetInitialSize((width, height))
            pre_frame.Initialize()
            pre_frame.Show()
        else:
            wx.MessageBox("Failed to create print preview",
                          "Print Error",
                          style=wx.ICON_ERROR|wx.OK)

    def Print(self, bmp):
        pdd = wx.PrintDialogData(self.print_data)
        printer = wx.Printer(pdd)
        printout = self.CreatePrintout(bmp)
        result = printer.Print(self.parent, printout)
        if result:
            # Store copy of print data for future use
            dlg_data = printer.GetPrintDialogData()
            newdata = dlg_data.GetPrintData()
            self.print_data = wx.PrintData(newdata)
        elif printer.GetLastError() == wx.PRINTER_ERROR:
            wx.MessageBox("Printer error detected.",
                          "Printer Error",
                          style=wx.ICON_ERROR|wx.OK)
        printout.Destroy()

class BitmapPrintout(wx.Printout):
    def __init__(self, bmp, data):
        super(BitmapPrintout, self).__init__()

        self.bmp = bmp
        self.data = data

    def GetPageInfo(self):
        # min, max, from, to
        return (1, 1, 1, 1)

    def HasPage(self, page):
        return page == 1

    def OnPrintPage(self, page):
        dc = self.GetDC()
        bmpW, bmpH = self.bmp.GetSize()

        # Check if we need to scale the bitmap to fit
        self.MapScreenSizeToPageMargins(self.data)
        rect = self.GetLogicalPageRect()
        w, h = rect.width, rect.height
        if (bmpW > w) or (bmpH > h):
            # Image is large so apply some scaling
            self.FitThisSizeToPageMargins((bmpW, bmpH),
                                          self.data)
            x, y = 0, 0
        else:
            # try to center it
            x = (w - bmpW) / 2
            y = (h - bmpH) / 2

        # Draw the bitmap to DC
        dc.DrawBitmap(self.bmp, x, y)

        return True

#-------------------------------------------------------#

class PrintBitmapApp(wx.App):
    def OnInit(self):
        self.frame = PrintBitmapFrame(None,
                                      title="Print Dialog")
        self.frame.Show()
        return True
    
if __name__ == '__main__':
    app = PrintBitmapApp(False)
    app.MainLoop()
