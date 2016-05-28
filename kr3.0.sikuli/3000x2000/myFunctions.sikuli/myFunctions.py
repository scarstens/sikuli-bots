from sikuli import *

def mouse_click(delay = 0.3, button = Button.LEFT):
    mouseDown(button)
    sleep(delay)
    mouseUp(button)

def appearclick(event):
    notify("observed")
    notify(event.getRegion())
    rgnvar = event.getRegion()
    imgvar = getPattern()
    rgnvar.click(exists(imgvar))
    notify("clicked")

def clickimgplay():
    if exists(img_play):
        click(rgn_img_play)

def closeoffers():
    closedspam = False
    while not closedspam:
        if rgn_img_specofferclose.exists(img_specofferclose,1):
            notify("found special offer")
            rgn_img_specofferclose.click(img_specofferclose)
            sleep(.1)
            rgn_img_closeyes.click(rgn_img_closeyes.exists(img_closeyes))
            wait(1)
        elif rgn_img_offerclosetr.exists(img_specofferclose,1):
            rgn_img_offerclosetr.click(img_specofferclose)
            wait(1)
        else:
            notify("spam should be closed")
            closedspam = True
            notify("looking for npc")
            return True

def moveToMapNPC():

    while not rgn_img_mapbtn.exists(img_closemap):

        npc_offset = int( SCREEN.getBounds().width * -1 * 0.075 )
        if exists( img_gem ):
            hover( Pattern(img_gem).targetOffset(5,50) )
            mouse_click(2, Button.RIGHT)
        if exists( img_town_statue_arm ):
            #maybe use 0.075 % of width
            hover( Pattern(img_town_statue_arm).targetOffset(npc_offset,0) )
            mouse_click(2)
            wait(1)
            if rgn_img_mapbtn.exists(img_closemap):
                break
                return True
            
            
            
        elif exists(img_town_window ):
            hover ( Pattern(img_mana_bar).targetOffset(0,-150) )
            mouse_click(2, Button.RIGHT)
            if exists( img_gem ):
                hover( Pattern(img_gem).targetOffset(5,50) )
                mouse_click(2, Button.RIGHT)
            if exists( img_town_statue_arm ):
                hover( Pattern(img_town_statue_arm).targetOffset(npc_offset,0) )
                mouse_click(2)
                wait(1)
                if rgn_img_mapbtn.exists(img_closemap):
                    break
                    return True
   
        


                

def getlocation():
    if rgn_img_refresh.exists(img_refresh,0):
        rgn_img_refresh.click(img_refresh)
        sleep(2)
    if rgn_img_dailybonus.exists(img_dailybonus,0) or rgn_img_offerclosetr.exists(img_specofferclose,0):
        return "intown"
    elif rgn_img_mapbtn.exists(img_closemap,0):
        return "pickmap"
    elif rgn_img_mapobj.exists(img_mapobj,0):
        return "playingmap"

def whileintown():
    rgn.img_special



def mapevents(event):
    print("observe event")
    print(event.getName())
    imgmatch = event.getMatch()
    print imgmatch
    hover(imgmatch)
    sleep(3)
    print(event.getPattern())
    setInactive(event)
    

def whilepickmap():
    if rgn_img_adamar.exists(img_adamar):
        click(rgn_img_adamar)
    if rgn_img_champ.exists(img_champ):
        click(rgn_img_champ)
    if rgn_img_alone.exists(img_alone):
        click(rgn_img_alone)
        if rgn_map_obj.exists(img_mapobj,30):
            locvar = "playmap"
            return locvar
        

def whileplaymap():
  if rgn_img_freebuff.exists(img_freebuff):
      hover(rgn_img_freebuff)
      mouse_click(2)
      hover(rgn_closebuff)
      mouse_click(2)
      closebuffs = True
  else:
      hover(rgn_closebuff)
      mouse_click(2)
      closebuffs = True
  while closebuffs:
      if rgn_img_auto.exists(img_auto):
          hover(img_auto)
          mouse_click(2)
          rgn_img_endlevel.wait(img_endlevel,300)
          if rgn_img_endlevel.exists(img_endlevel):
              hover(img_endlevel)
              mouse_click(2)
              wait(2)
              rgn_img_returntown.wait(img_returntown)
              hover(rgn_img_returntown)
              mouse_click(2)
              closebuffs = False
              wait(2)
          
      

 