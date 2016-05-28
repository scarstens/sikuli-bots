Debug.setDebugLevel(3)
Settings.WaitScanRate=5
bundlepath = getBundlePath()
libFunc = "/3000x2000/myfunctions.Sikuli"
execfile( bundlepath+libFunc+"/myfunctions.py" ) # to make your functions available

libImg = "/3000x2000/myImages.Sikuli/"
setBundlePath(bundlepath+libImg) # could also be a statement in myImages.sikuli
execfile( bundlepath+libImg+"myImages.py" )

def notify(message):

        print(message)
playingkr = True

debug = False
if debug:
    whilepickmap()


while playingkr:
    clickimgplay()
    locvar = getlocation()
    if locvar == "intown":
        notify(locvar)
        closedspam = False
        closedspam = closeoffers()
        if closedspam:
            moveToMapNPC()
        
    elif locvar == "pickmap":
        notify("picking map")
        whilepickmap()
        
    elif locvar == "playingmap":
        notify("playingmap")
        whileplaymap()
    
    else: 
        notify("broken")

        
