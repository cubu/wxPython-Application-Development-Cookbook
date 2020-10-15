# Chapter 10: Getting your Application Ready for Release
# Recipe 8: Distributing an application
#
import wx
import sys
from esky import bdist_esky
from setuptools import setup
import version

APP = "EditorApp.py"
NAME = "FileEditor"
VERSION = version.VERSION
AUTHOR = "Author Name"
AUTHOR_EMAIL = "authorname@someplace.com"
URL = "http://fileeditor_webpage.foo"
LICENSE = "wxWidgets"
YEAR = "2015"

def BuildPy2Exe():
    import py2exe
    opts = dict(compressed = 0,
                optimize = 0,
                bundle_files = 3,
                includes = ["fileEditor", "EditorApp"],
                excludes = ["Tkinter",],
                dll_excludes = ["MSVCP90.dll"])
    icon = "Icon.ico"
    BundleEsky("py2exe", opts, icon)

def BuildOSXApp():
    """Build the OSX Applet"""
    copyright = "Copyright %s %s" % (AUTHOR, YEAR)
    appid = "com.%s.%s" % (NAME, NAME)
    plist = dict(CFBundleName = NAME,
                 CFBundleIconFile = 'Icon.icns',
                 CFBundleShortVersionString = VERSION,
                 CFBundleGetInfoString = NAME + " " + VERSION,
                 CFBundleExecutable = NAME,
                 CFBundleIdentifier = appid,
                 CFBundleTypeMIMETypes = ['text/plain',],
                 CFBundleDevelopmentRegion = 'English',
                 NSHumanReadableCopyright = copyright
    )
    icon = "Icon.icns"
    opts = dict(iconfile = icon,
                argv_emulation = True,
                optimize = True,
                plist = plist)
    
    BundleEsky("py2app", opts, icon)

def BundleEsky(freezer, options, icon):
    app = [bdist_esky.Executable(APP, gui_only=True, 
                                      icon=icon),]
    eskyOps = dict(freezer_module = freezer,
                   freezer_options = options,
                   enable_appdata_dir = True,
                   bundle_msvcrt = True)

    data = [ icon, ]

    setup(name = NAME,
          scripts = app,
          version = VERSION,
          author = AUTHOR,
          author_email = AUTHOR_EMAIL,
          license = LICENSE,
          url = URL,
          data_files = data,
          options = dict(bdist_esky = eskyOps))

if __name__ == '__main__':
    if wx.Platform == '__WXMSW__':
        # Windows
        BuildPy2Exe()
    elif wx.Platform == '__WXMAC__':
        # OSX
        BuildOSXApp()
    else:
        print "Unsupported platform: %s" % wx.Platform
