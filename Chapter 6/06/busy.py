# Chapter 6: Ways to Notify and Alert
# Recipe 6: Giving busy feedback
#
import threading
import wx
import wx.lib.agw.pybusyinfo as pbi

class ResultDisplay(wx.Frame):
    def __init__(self, parent, title):
        super(ResultDisplay, self).__init__(parent, title=title)

        sizer = wx.BoxSizer(wx.VERTICAL)
        panel = self._buildPanel()
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        self.SetInitialSize()

    def _buildPanel(self):
        panel = wx.Panel(self)
        msg = "Enter the nth Fibonacci # to calculate:"
        self.msg = wx.StaticText(panel, label=msg)
        self.ntxt = wx.TextCtrl(panel, value="500000")
        style = wx.TE_READONLY|wx.TE_RICH2
        self.result = wx.TextCtrl(panel, style=style)
        self.calc = wx.Button(panel, label="Calculate")
        self.calc.Bind(wx.EVT_BUTTON, self.OnCalculate)
        
        return self._layoutPanel(panel)
    
    def _layoutPanel(self, panel):
        sizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.msg, 0, wx.ALL, 5)
        hsizer.Add(self.ntxt, 0, wx.RIGHT, 5)
        
        sizer.Add(hsizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
        
        flags = wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL
        sizer.Add(self.result, 1, flags)

        sizer.Add(self.calc, 0, wx.ALIGN_CENTER_HORIZONTAL)
        panel.SetSizer(sizer)
        
        return panel

    def OnCalculate(self, event):
        self.info = pbi.PyBusyInfo("Calculating...", self)
        self.calc.Enable(False)

        num = int(self.ntxt.Value)
        t = FibonacciCalc(num, self.OnComplete)
        t.start()

    def OnComplete(self, value):
        def SafeUpdate(value):
            self.result.Value = str(value)
            self.calc.Enable(True)

        del self.info
        wx.CallAfter(lambda: SafeUpdate(value)) 

class FibonacciCalc(threading.Thread):
    def __init__(self, n, completeFunc):
        super(FibonacciCalc, self).__init__()
        assert callable(completeFunc)
        self.n = n
        self.complete = completeFunc

    def run(self):
        def fib(n):
            a,b = 1,1
            for i in xrange(n - 1):
                a,b = b,a+b
            return a

        val = fib(self.n)
        self.complete(val)

#------------------------------------------------------#

class FibonacciApp(wx.App):
    def OnInit(self):
        mainw = ResultDisplay(None, title="Fibonacci")
        mainw.Show()
        return True

if __name__ == "__main__":
    app = FibonacciApp(False)
    app.MainLoop()
