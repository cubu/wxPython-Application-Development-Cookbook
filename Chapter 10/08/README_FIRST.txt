To try out the code in this recipe you will need to do a few things to setup a
test environment. The steps to do this are included below.

1) Build a version 1 of the program
  * Run: python setup.py bdist_esky
  * This will generate an esky zip bundle in the dist folder
2) Bump the version number in the version.py to a higher number
3) Build the new version same as in step 1
  * Should now see two zip bundles named with the appropriate version numbers
4) Unzip the version 1 build to a location on your computer
5) Start a webserver on your localhost to act as the update server
  * Run: python -m SimpleHTTPServer
  * This will start an HTTP server on port 8000 of your PC
  * The web root directory is set to your home folder
6) Copy the 2 zip files that were previously built to the web root
7) We now have a webserver running and two versions of our application at
   the expected URL.
8) Go to where you unzipped the version 1 of the application and run the built
   application.
   * You should be prompted to be notified of a new version being available
   * Accept the update and see the new version get installed automatically.
