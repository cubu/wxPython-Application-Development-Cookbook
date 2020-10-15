# Chapter 10: Getting your Application Ready for Release
# Recipe 6: Embedding your resources
#
import sys
import os
import glob
import wx.tools.img2py as img2py

def generateIconModule(sourcePath, outModule):
    search = os.path.join(sourcePath, "*.png")
    lst = glob.glob(search)
    splitext = os.path.splitext
    basename = os.path.basename
    i = 0
    for i, png in enumerate(lst):
        name = splitext(basename(png))[0]
        name = name.replace('-', ' ').title()
        name = name.replace(' ', '')
        img2py.img2py(png, outModule, i > 0, imgName=name)
    return i

def printHelp():
    print("PNG image file embedder")
    print("embedded.py imgDirectory resource.py")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        printHelp()
        sys.exit()
    dName = sys.argv[1]
    print("Locating PNG images in %s" % dName)
    modName = sys.argv[2]
    n = generateIconModule(dName, modName)
    print("%d images embedded in %s" % (n, modName))
