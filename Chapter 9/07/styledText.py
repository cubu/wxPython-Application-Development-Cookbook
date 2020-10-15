# Chapter 9: Creating and Customizing Components
# Recipe 7: Implementing highlighting in the StyledTextCtrl
#
import wx
import wx.stc as stc

# Style IDs for the KeywordLexer
STC_STYLE_KW_DEFAULT, \
STC_STYLE_KW_KEYWORD = range(2)

class KeywordLexer(object):
    def __init__(self):
        super(KeywordLexer, self).__init__()
        self._kw = list()

    def SetKeywords(self, kws):
        self._kw = kws

    def StyleText(self, event):
        buffer = event.EventObject
        lastStyled = buffer.GetEndStyled()
        startPos = buffer.PositionFromLine(lastStyled)
        startPos = max(startPos, 0)
        endPos = event.GetPosition()
        
        curWord = ""
        while startPos < endPos:
            c = chr(buffer.GetCharAt(startPos))
            curWord += c
            if c.isspace():
                curWord = curWord.strip()
                if curWord in self._kw:
                    style = STC_STYLE_KW_KEYWORD
                else:
                    style = STC_STYLE_KW_DEFAULT

                wordStart = max(0, startPos - (len(curWord)))
                buffer.StartStyling(wordStart, 0x1f)
                buffer.SetStyling(len(curWord), style)
                buffer.SetStyling(1, STC_STYLE_KW_DEFAULT)
                curWord = ""
            startPos += 1

class KeywordSTC(stc.StyledTextCtrl):
    def __init__(self, parent):
        super(KeywordSTC, self).__init__(parent)

        self._lexer = None

        self.Bind(stc.EVT_STC_STYLENEEDED, self.OnStyle)

    def OnStyle(self, event):
        if self._lexer:
            self._lexer.StyleText(event)
        else:
            event.Skip()

    def SetKeyWords(self, idx, keywords):
        if self._lexer:
            self._lexer.SetKeywords(keywords.split())
        else:
            super(KeywordSTC, self).SetKeyWords(idx, keywords)

    def SetLexer(self, lexerID):
        if lexerID == stc.STC_LEX_CONTAINER:
            self._lexer = KeywordLexer()
        super(KeywordSTC, self).SetLexer(lexerID)

#-----------------------------------------------------------#

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title)

        sizer = wx.BoxSizer()
        self.stc = KeywordSTC(self)
        sizer.Add(self.stc, 1, wx.EXPAND)

        self.stc.SetLexer(stc.STC_LEX_CONTAINER)
        self.stc.SetKeyWords(0, "Hello World Highlight Me")
        self.stc.StyleSetSpec(STC_STYLE_KW_DEFAULT, 
                              "fore:#0000FF,back:#FFFFFF")
        self.stc.StyleSetSpec(STC_STYLE_KW_KEYWORD,
                              "fore:#FF0000,bold")
        self.Sizer = sizer
        self.SetInitialSize((400, 300))
        
class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Custom STC Lexer")
        self.frame.Show()
        return True
    
if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
