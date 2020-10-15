# Chapter 10: Getting your Application Ready for Release
# Recipe 5: Handling errors gracefully
#
import sys
import traceback
import wx
import wx.lib.dialogs as DIA

class ErrorHandlingApp(wx.App):
    def OnInit(self):
        sys.excepthook = self.ExceptionHook
        
        self.frame = TestFrame(None, "Unhandled error")
        self.frame.Show()

        return True

    def ExceptionHook(self, errType, value, trace):
        err = traceback.format_exception(errType, value, trace)
        errTxt = "\n".join(err)
        msg = "An unexpected error has occurred:\n%s" % errTxt
        if self and self.IsMainLoopRunning():
            # only use UI notification if APP is running
            if not self.HandleError(value):
                DIA.scrolledMessageDialog(None, msg, 
                                          "Unexpected Error")
                self.Exit()
        else:
            sys.stderr.write(msg)

    def HandleError(self, error):
        """Override in subclass to handle errors
        @return: True to allow program to continue running
        """
        return False

class TestFrame(wx.Frame):
    def __init__(self, parent, title):
        super(TestFrame, self).__init__(parent, title=title)

        panel = wx.Panel(self)
        psz = wx.BoxSizer()
        btn = wx.Button(panel, wx.NewId(), "Cause Error")
        psz.Add(btn, 0, wx.ALIGN_CENTER|wx.ALL, 100)
        panel.Sizer = psz
        
        sizer = wx.BoxSizer()
        sizer.Add(panel, 1, wx.EXPAND)
        self.Sizer = sizer
        self.SetInitialSize()

        self.Bind(wx.EVT_BUTTON, self.OnError, btn)

    def OnError(self, event):
        # cause an unhandled exception
        x = 1 / 0

if __name__ == '__main__':
    app = ErrorHandlingApp(False)
    app.MainLoop()
