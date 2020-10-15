# Chapter 10: Getting your Application Ready for Release
# Recipe 1: Storing your configuration with StandardPaths
#
import os
import json
import wx

class AppConfig(object):
    _instance = None
    def __init__(self):
        super(AppConfig, self).__init__()

        # create base dir if it doesnt exist
        if not os.path.exists(self.UserConfigDir):
            os.mkdir(self.UserConfigDir)

        self.data = dict()
        if os.path.exists(self.ConfigFile):
            with open(self.ConfigFile) as dataFile:
                self.data = json.load(dataFile)

    @property
    def UserConfigDir(self):
        return wx.StandardPaths_Get().GetUserDataDir()

    @property
    def ConfigFile(self):
        appName = wx.GetApp().AppName
        return os.path.join(self.UserConfigDir, 
                            "%s.json" % appName)

    def GetConfigFile(self, relPath):
        return os.path.join(self.UserConfigDir, relPath)

    def ConfigFileExists(self, relPath):
        path = self.GetConfigFile(relPath)
        return os.path.exists(path)

    def GetValue(self, key, default=None):
        return self.data.get(key, default)

    def WriteValue(self, key, value):
        self.data[key] = value

    def SaveConfig(self):
        with open(self.ConfigFile, 'w') as configFile:
            json.dump(self.data, configFile)

    @staticmethod
    def Instance():
        if AppConfig._instance is None:
            AppConfig._instance = AppConfig()
        return AppConfig._instance

#--------------------------------------------------------------#

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title)

        sizer = wx.BoxSizer()
        sizer.Add(MyPanel(self), 1, wx.EXPAND)
        self.Sizer = sizer
        
        self.Bind(wx.EVT_CLOSE, self.OnExit)

    def OnExit(self, event):
        AppConfig.Instance().SaveConfig()
        event.Skip()

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        cfg = AppConfig.Instance()

        sizer = wx.BoxSizer(wx.VERTICAL)
        cb1 = wx.CheckBox(self, label="Option 1", name="opt1")
        cb1.Value = cfg.GetValue(cb1.Name, False)
        cb2 = wx.CheckBox(self, label="Option 2", name="opt2")
        cb2.Value = cfg.GetValue(cb2.Name, False)
        sizer.AddMany([(cb1, 0, wx.ALL, 10), (cb2, 0, wx.ALL, 10)])
        self.Sizer = sizer

        self.Bind(wx.EVT_CHECKBOX, self.OnCheck)

    def OnCheck(self, event):
        obj = event.EventObject
        AppConfig.Instance().WriteValue(obj.Name, obj.Value)
        event.Skip()

class MyApp(wx.App):
    def OnInit(self):
        self.SetAppName("wxPythonTestApp")
        self.frame = MyFrame(None, title="Standard Paths")
        self.frame.Show()
        return True

if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
