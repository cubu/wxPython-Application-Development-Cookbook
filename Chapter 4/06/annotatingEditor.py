# Chapter 4: Containers and Advanced Controls
# Recipe 6: Annotating the StyledTextCtrl
#
import sys
import pep8
try:
    from StringIO import StringIO ## for Python 2
except ImportError:
    from io import StringIO ## for Python 3
import wx
import wx.stc as stc
# Recipe 5 module
import codeEditor

# Constants
ANNOTATION_ERROR = 20
ANNOTATION_WARN = 21

class Pep8Editor(codeEditor.PythonCodeEditor):
    def __init__(self, parent):
        super(Pep8Editor, self).__init__(parent)

        # Setup annotation settings
        self.AnnotationSetVisible(stc.STC_ANNOTATION_BOXED)
        errStyle = "fore:#8B0000,bold,back:#FF967A"
        self.StyleSetSpec(ANNOTATION_ERROR, errStyle)
        warnStyle = "fore:#DD6A00,bold,back:#F5DEB3"
        self.StyleSetSpec(ANNOTATION_WARN, warnStyle)

    def SaveFile(self, fileName="", fileType=wx.TEXT_TYPE_ANY):
        super(Pep8Editor, self).SaveFile(fileName, fileType)

        # perform pep8 analysis after save
        self.AnnotationClearAll()
        self.DoPep8Check(fileName)

    def DoPep8Check(self, fileName):
        checker = pep8.Checker(fileName)
        
        stdio = sys.stdout
        sys.stdout = results = StringIO.StringIO()
        try:
            checker.check_all()
        finally:
            sys.stdout = stdio

        results.seek(0)
        findings = results.readlines()
        if findings:
            processed = self.ProcessFindings(findings)
            self.AddFindings(processed)

    def ProcessFindings(self, findings):
        processed = dict()
        for finding in findings:
            finding = finding.strip()
            parts = finding.split(':')
            line = int(parts[1]) - 1
            msg = parts[-1].strip()
            if processed.has_key(line):
                processed[line] += "\n" + msg
            else:
                processed[line] = msg
        return [ (l, m) for l, m in processed.iteritems() ]

    def AddFindings(self, findings):
        for line, msg in findings:
            self.AnnotationSetText(line, msg)
            if msg.startswith("E"):
                self.AnnotationSetStyle(line, ANNOTATION_ERROR)
            else:
                self.AnnotationSetStyle(line, ANNOTATION_WARN)

#-------------------------------------#

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Pep8 Annotations", size=(500,500))
        self.SetTopWindow(self.frame)
        self.frame.Show()

        return True

class MyFrame(wx.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(MyFrame, self).__init__(parent, *args, **kwargs)

        # Attributes
        accel = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('S'), wx.ID_SAVE)])
        self.SetAcceleratorTable(accel)
        self.panel = MyPanel(self)

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        self.Bind(wx.EVT_MENU, self.OnSave, id=wx.ID_SAVE)

    def OnSave(self, event):
        self.panel.Save()

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        # Attributes
        self._stc = Pep8Editor(self)
        
        # load itself
        self._stc.LoadFile(__file__)
        self._stc.DoPep8Check(__file__)

        # Layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self._stc, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def Save(self):
        copy = "Copy_%s" % __file__
        self._stc.SaveFile(copy)

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
    