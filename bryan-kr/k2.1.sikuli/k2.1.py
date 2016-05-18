#define images
img_closemap = "img_closemap.png"
img_zoomout = "img_zoomout.png"
img_adamar = "img_adamar.png"
img_obj = "img_obj.png"
img_dailyreward = "img_dailyreward.png"
img_playingkr = "img_playingkr.png"
img_buffs = "img_buffs.png"
img_stop = "img_stop.png"
img_endlevel = "img_endlevel.png"
img_returntown = "img_returntown.png"
img_offer = "img_offer.png"
img_closeoffer = "img_closeoffer.png"
img_mapguy = "img_mapguy.png"

#define locations
loc_auto = (Location(2313, 1454))
loc_returntown = (Location(1161, 1577))
loc_yesdecline = (Location(1361, 1090))
#define regions

#definae global variables
pickmap = False
intown = False
playmap = False


#define functions

def setvariables():
    global pickmap
    global intown
    global playmap
    intown = False
    pickmap = False
    playmap = False
    if exists(img_closemap):
        pickmap = True
    elif exists(img_obj):
        playmap = True
    elif exists(img_dailyreward) or exists(img_offer):
        intown = True
    else:
        popup("you need to refresh")
    

def dostart():
    global pickmap
    global intown
    global playmap
    setvariables()
    if intown:
        dointown()
    elif pickmap:
        dopickmap()
    elif playmap:
        doplaymap()
    else:
        popup("you need to refresh")

def dopickmap():
    setvariables()
    global pickmap
    if not pickmap:
        dostart()
    popup("picking map")
    if exists(img_zoomout):
        click()
    elif exists(img_adamar):
        click()
        sleep(1)
        click(Location(1705, 1448))
        sleep(1)
        click(Location(1051, 1094))
        sleep(3)
        doplaymap()

    else:
        dostart()

def doplaymap():
    setvariables()
    global playmap
    if not playmap:
        dostart()
        
  
    if exists(img_buffs):
        click(Location(835, 1421))
        sleep(.5)
        click(Location(1715, 1024))
        sleep(.5)
    click(loc_auto)
    while exists(img_obj) and not exists(img_endlevel):
        popup("still playing")
    if exists(img_endlevel):
        click()
        sleep(2)
        click(loc_returntown)
        dointown()    
    
    

def dointown():
    setvariables()
    global intown   
    if not intown:
        dostart()
    
    if exists(img_dailyreward) or exists(img_offer):
        closedoffers = False
    sleep(2)
    
    while intown and not closedoffers:
         if exists(img_offer):
            click(img_closeoffer)
            sleep(1.5)
            click(loc_yesdecline)
            sleep(1.5)
        
         else: 
             closedoffers = True
    wait(.5) 
    while intown and closedoffers:
        
            for x in range(0, 3):
                hover(Location(1571, 403))
                sleep(1)
                mouseDown(Button.RIGHT)
                sleep(0.5)
                mouseUp(Button.RIGHT)
                if exists(img_mapguy):
                    hover()
                    sleep(0.5)
                    click()
                    dopickmap()
                    
                    
             
            for x in range(0, 3):
                hover(Location(1662, 1418))
                sleep(1)
                mouseDown(Button.RIGHT)
                sleep(0.5)
                mouseUp(Button.RIGHT)
                if exists(img_mapguy):   
                    hover()
                    sleep(0.5)
                    click()
                    dopickmap()
            
            closedoffers=False    
                
        
                    

if exists(img_playingkr):        
    
    dostart()

