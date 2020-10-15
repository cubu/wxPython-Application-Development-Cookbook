# Chapter 6: Ways to Notify and Alert
# Recipe 5: Making a splash at startup
#
import wx

class ProgressSplash(wx.SplashScreen):
    def __init__(self, bmp, splashStyle, timeout, parent):
        super(ProgressSplash, self).__init__(bmp, splashStyle,
                                             timeout, parent)

        self._msg = wx.StaticText(self)

        # Create status display area
        self.CreateStatusBar()
        sbarHeight = self.StatusBar.Size.height
        self.SetSize((self.Size.width, 
                      sbarHeight + bmp.Height))
    
class SlowStartingApp(wx.App):
    def OnInit(self):
        mainw = wx.Frame(None, title="MyApp")
        
        bmp = wx.Bitmap('splash_img.png')
        splashStyle = wx.SPLASH_CENTRE_ON_SCREEN|\
                      wx.SPLASH_NO_TIMEOUT
        self.splash = ProgressSplash(bmp, splashStyle, 
                                     -1, mainw)
        self.splash.Show()

        # Do application setup tasks
        self.Initialize()
        self.splash.Destroy()
        return True

    def Initialize(self):
        self.LoadConfig()
        self.ConnectToServer()
        self.InitializeUI(mainw)

    def LoadConfig(self):
        # simulate long configuration load
        self.splash.PushStatusText("Loading config...")
        wx.Sleep(1)

    def ConnectToServer(self):
        # simulate setting up connections
        self.splash.PushStatusText("Connecting...")
        wx.Sleep(2)
        self.splash.PushStatusText("Connection Ok...")
        wx.Sleep(1)

    def InitializeUI(self, window):
        # simulate setup of UI
        self.splash.PushStatusText("Initializing UI...")
        wx.Sleep(1)
        window.Show()

#------------------------------------------------------#

if __name__ == "__main__":
    app = SlowStartingApp(False)
    app.MainLoop()
