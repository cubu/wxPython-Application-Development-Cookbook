# Chapter 8: User Interface Primitives
# Recipe 3: Customizing grid labels
#
import wx
import wx.grid as gridlib
import wx.lib.mixins.gridlabelrenderer as glr

class FancyGrid(gridlib.Grid, glr.GridWithLabelRenderersMixin):
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent)
        glr.GridWithLabelRenderersMixin.__init__(self)

class FancyRowLabelRenderer(glr.GridLabelRenderer):
    def __init__(self, color):
        super(FancyRowLabelRenderer, self).__init__()
        self.color = color

    def Draw(self, grid, dc, rect, row):
        dc.SetBrush(wx.Brush(self.color))
        dc.DrawRoundedRectangleRect(rect, -0.4)
        text = grid.GetRowLabelValue(row)
        hAlign, vAlign = grid.GetRowLabelAlignment()
        self.DrawText(grid, dc, rect, text, hAlign, vAlign)

class FancyColLabelRenderer(glr.GridLabelRenderer):
    def __init__(self, color):
        super(FancyColLabelRenderer, self).__init__()
        self.color = color
        
    def Draw(self, grid, dc, rect, col):
        dc.SetBrush(wx.Brush(self.color))
        dc.DrawRoundedRectangleRect(rect, -0.4)
        text = grid.GetColLabelValue(col)
        hAlign, vAlign = grid.GetColLabelAlignment()
        self.DrawText(grid, dc, rect, text, hAlign, vAlign)

class FancyCornerLabelRenderer(glr.GridLabelRenderer):
    def __init__(self, color):
        super(FancyCornerLabelRenderer, self).__init__()
        self.color = color

    def Draw(self, grid, dc, rect, rc):
        dc.SetBrush(wx.Brush(self.color))
        dc.DrawRectangleRect(rect)
        bmp = wx.ArtProvider.GetBitmap(wx.ART_HARDDISK)
        x = rect.left + (rect.width - bmp.Width) / 2
        y = rect.top + (rect.height - bmp.Height) / 2
        dc.DrawBitmap(bmp, x, y, True)

class GridPanel(wx.Panel):
    def __init__(self, parent):
        super(GridPanel, self).__init__(parent)

        self.grid = FancyGrid(self)
        squareGrid = 5
        self.grid.CreateGrid(squareGrid, squareGrid)

        # Assign our custom corner renderer
        corRender = FancyCornerLabelRenderer("#FF6666")
        self.grid.SetCornerLabelRenderer(corRender)

        # Assign column and row renderers
        rowRender = FancyRowLabelRenderer("#6666FF")
        self.grid.SetDefaultRowLabelRenderer(rowRender)
        colRender = FancyColLabelRenderer("#66FF66")
        self.grid.SetDefaultColLabelRenderer(colRender)

        self.Sizer = wx.BoxSizer()
        self.Sizer.Add(self.grid, 1, wx.EXPAND)

#-----------------------------------------------------------#

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title)

        sizer = wx.BoxSizer()
        self.panel = GridPanel(self)
        sizer.Add(self.panel, 1, wx.EXPAND)

        self.Sizer = sizer
        self.SetInitialSize()

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Custom Grid Labels")
        self.frame.Show()
        return True
    
if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
