# Chapter 4: Containers and Advanced Controls
# Recipe 3: Configuring properties
#
import ast
import inspect
import wx
import wx.propgrid as propgrid

class ObjectInspector(propgrid.PropertyGrid):
    def __init__(self, parent):
        super(ObjectInspector, self).__init__(parent)
        self.Bind(propgrid.EVT_PG_CHANGED, self.OnChange)

    def OnChange(self, event):
        prop = event.GetProperty()
        name = prop.GetName()
        val = prop.GetValue()
        try:
            setattr(self.obj, name, val)
        except Exception, err:
            print(err)

    def SetObject(self, obj):
        self.Clear()
        self.obj = obj
        methods = list()
        if obj is not None:
            self.Append(propgrid.PropertyCategory("Attributes"))
            for name, val in inspect.getmembers(obj):
                if callable(val):
                    methods.append((name, val))
                else:
                    self.AddAttribute(name, val)
            
            # Add Method category
            self.Append(propgrid.PropertyCategory("Methods"))
            for name, val in methods:
                self.AddMethod(name, val)

        self.GetGrid().FitColumns()

    def GetProperty(self, attr, val):
        pmap = { bool : propgrid.BoolProperty,
                 int : propgrid.IntProperty,
                 str : propgrid.StringProperty,
                 unicode : propgrid.StringProperty,
                 wx.Colour : propgrid.ColourProperty,
                 wx.Font : propgrid.FontProperty,
                 wx.Size : SizeProperty
               }
        prop = pmap.get(type(val))
        if prop is None:
            prop = propgrid.StringProperty(attr, value=str(val))
            prop.Enable(False)
            return prop
        return prop(attr, value=val)

    def AddAttribute(self, name, val):
        prop = self.Append(self.GetProperty(name, val))
        if val is None:
            prop.Enable(False)
        elif isinstance(val, bool):
            prop.SetAttribute("UseCheckbox", True)

    def AddMethod(self, name, m):
        doc = inspect.getdoc(m)
        if doc is None:
            doc = "No Description"
        prop = propgrid.StringProperty(name, value=doc)
        prop.Enable(False)
        self.Append(prop)

class SizeProperty(propgrid.PyProperty):
    """Very simple custom property handler for wx.Size"""
    def __init__(self, label, name = propgrid.LABEL_AS_NAME, value=0):
        super(SizeProperty, self).__init__(label, name)
        self.SetValue(value)

    def ValueToString(self, value, flags):
        return str(value)

    def StringToValue(self, s, flags):
        # note: no error handling
        return (True, ast.literal_eval(s))

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        self.pg = ObjectInspector(self)
        
        ### Tell the grid to inspect itself
        ## Can change to any other Python object here to change what is inspected
        ## in the display.
        self.pg.SetObject(self.pg)

        sizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.pg, 1, wx.EXPAND)
        sizer.Add(hsizer, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
class MyFrame(wx.Frame):
    def __init__(self, parent, title=""):
        super(MyFrame, self).__init__(parent, title=title)
        
        # Set the panel
        sizer = wx.BoxSizer()
        sizer.Add(MyPanel(self), 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.SetInitialSize((300, 450))

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="PropertyGrid")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
