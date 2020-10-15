# Chapter 4: Containers and Advanced Controls
# Recipe 5: Styling text with the StyledTextCtrl
#
import wx
import wx.stc as stc
import keyword

class CodeEditorBase(stc.StyledTextCtrl):
    def __init__(self, parent):
        super(CodeEditorBase, self).__init__(parent)

        # Attributes
        font = wx.Font(10, wx.FONTFAMILY_MODERN,
                           wx.FONTSTYLE_NORMAL,
                           wx.FONTWEIGHT_NORMAL)
        self.face = font.GetFaceName()
        self.size = font.GetPointSize()

        # Setup
        self.SetupBaseStyles()

    def EnableLineNumbers(self, enable=True):
        if enable:
            self.SetMarginType(1, stc.STC_MARGIN_NUMBER)
            self.SetMarginMask(1, 0)
            self.SetMarginWidth(1, 25)
        else:
            self.SetMarginWidth(1, 0)

    def GetFaces(self):
        return dict(font=self.face, size=self.size)

    def SetupBaseStyles(self):
        faces = self.GetFaces()
        default = "face:%(font)s,size:%(size)d" % faces
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, default)
        line = "back:#C0C0C0," + default
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER, line)
        self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR,
                          "face:%(font)s" % faces)

class PythonCodeEditor(CodeEditorBase):
    def __init__(self, parent):
        super(PythonCodeEditor, self).__init__(parent)

        # Setup
        self.SetLexer(wx.stc.STC_LEX_PYTHON)
        self.SetupKeywords()
        self.SetupStyles()
        self.EnableLineNumbers(True)

    def SetupKeywords(self):
        kwlist = " ".join(keyword.kwlist)
        self.SetKeyWords(0, kwlist)

    def SetupStyles(self):
        # Python styles
        faces = self.GetFaces()
        fonts = "face:%(font)s,size:%(size)d" % faces
        tmpl = "fore:%s," + fonts
        default = "fore:#000000," + fonts

        # Default 
        self.StyleSetSpec(stc.STC_P_DEFAULT, default)
        # Comments
        self.StyleSetSpec(stc.STC_P_COMMENTLINE, tmpl % "#007F00")
        # Number
        self.StyleSetSpec(stc.STC_P_NUMBER, tmpl % "#007F7F")
        # String
        self.StyleSetSpec(stc.STC_P_STRING, tmpl % "#7F007F")
        # Single quoted string
        self.StyleSetSpec(stc.STC_P_CHARACTER, tmpl % "#7F007F")
        # Keyword
        self.StyleSetSpec(stc.STC_P_WORD, tmpl % "#00007F,bold")
        # Triple quotes
        self.StyleSetSpec(stc.STC_P_TRIPLE, tmpl % "#7F0000")
        # Triple double quotes
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, tmpl % "#7F0000")
        # Class name definition
        self.StyleSetSpec(stc.STC_P_CLASSNAME, tmpl % "#0000FF,bold")
        # Function or method name definition
        self.StyleSetSpec(stc.STC_P_DEFNAME, tmpl % "#007F7F,bold")
        # Operators
        self.StyleSetSpec(stc.STC_P_OPERATOR, "bold," + fonts)
        # Identifiers
        self.StyleSetSpec(stc.STC_P_IDENTIFIER, default)
        # Comment-blocks
        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK, tmpl % "#7F7F7F")
        # End of line where string is not closed
        eol_style = "fore:#000000,back:#E0C0E0,eol," + fonts
        self.StyleSetSpec(stc.STC_P_STRINGEOL, eol_style)

#---- End Recipe Code ----#

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="StyledTextCtrl", size=(400,500))
        self.SetTopWindow(self.frame)
        self.frame.Show()

        return True

class MyFrame(wx.Frame):
    def __init__(self, parent, *args, **kwargs):
        wx.Frame.__init__(self, parent, *args, **kwargs)

        # Attributes
        self.panel = MyPanel(self)

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
class MyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Attributes
        self._stc = PythonCodeEditor(self)
        self._stc.LoadFile(__file__)

        # Layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self._stc, 1, wx.EXPAND)
        self.SetSizer(sizer)

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
