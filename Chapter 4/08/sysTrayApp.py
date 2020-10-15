# Chapter 4: Containers and Advanced Controls
# Recipe 8: Building a system tray application
#
import urllib
import json
import wx

ID_GET_CITY = wx.NewId()

class WeatherTray(wx.TaskBarIcon):
    def __init__(self):
        super(WeatherTray, self).__init__()
        self.data = { 'desc' : "Unknown", 'temp' : "??" }
        self.UpdateData("London,UK")
        self.Bind(wx.EVT_MENU, self.OnMenu)

    def UpdateData(self, city):
        src = "http://api.openweathermap.org/data/2.5/weather?q=%s"
        try:
            formatted = city.replace(' ', "%20")
            url = urllib.urlopen(src % formatted)
            j = json.load(url)

            weather = j['weather'][0]
            temp = j['main']['temp']
            self.data = dict()
            self.data['desc'] = weather['main']
            self.data['icon'] = weather['icon']
            c = float(temp) - 273.15
            self.data['temp'] = c
            
            self.city = city
            self.UpdateIcon()
        except:
            pass

    def UpdateIcon(self):
        img = None
        try:
            loc = "http://openweathermap.org/img/w/%s.png"
            url = urllib.urlopen(loc % self.data['icon'])
            img = wx.ImageFromStream(url, wx.BITMAP_TYPE_PNG)
            img = wx.BitmapFromImage(img)
        except:
            img = wx.Bitmap('errIcon.png')
        icon = wx.IconFromBitmap(img)
        self.SetIcon(icon)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        
        data = (self.city, 
                "Weather: %s" % self.data['desc'], 
                "Temp: %s C" % self.data['temp'])
        for d in data:
            item = menu.Append(wx.ID_ANY, d)
            item.Enable(False)

        menu.AppendSeparator()
        menu.Append(ID_GET_CITY, "Enter city name...")
        menu.AppendSeparator()
        menu.Append(wx.ID_CLOSE)
        return menu

    def OnMenu(self, event):
        if event.Id == wx.ID_CLOSE:
            self.Destroy()
        elif event.Id == ID_GET_CITY:
            t = wx.GetTextFromUser("Enter City Name (City,Country):", 
                                   default_value=self.city)
            if t:
                self.UpdateData(t)
        else:
            event.Skip()

class WeatherTrayApp(wx.App):
    def OnInit(self):
        self._trayIcon = WeatherTray()
        return True

if __name__ == "__main__":
    app = WeatherTrayApp(False)
    app.MainLoop()
    