# TODO:
# OPEN LOCKBOXES: http://doc.sikuli.org/finder.html?highlight=rows
print "[S1P00] Starting script."
print "[S1P01] Screen Height Detected: "+str(SCREEN.getBounds().width)

# Import libraries used
import argparse, os

# Global Settings to start with - these can be changed later
Settings.MoveMouseDelay = 0.5 # default 2 times a second
Settings.ObserveScanRate = 0.333 # default 3 times a second
Settings.DelayBeforeMouseDown = 0.5 # only applies to next click
#setFindFailedResponse(PROMPT) # try forver on fail - doesn't seem to play nice right now

# define globals
force_start_mode = False
#force_start_mode = "debug"
debug_popups = False
running = True
game_available = True
logged_in = True
auto_run_loop = False
auto_run_count = 0
fail_to_run = 0
map_to_run = 0
map_mode_to_run = 2
continue_run = True
img_collection = ()

# Allow control of force start mode
parser = argparse.ArgumentParser()
parser.add_argument("--force_start_mode", help="set to autoplay or debug")
parser.add_argument("--map_to_run", help="set to int of map to run")
parser.add_argument("--map_mode_to_run", help="set to 0, 1, or 2")
args = parser.parse_args()
if args.force_start_mode:
    print "force_start_mode: "+args.force_start_mode
    force_start_mode = args.force_start_mode
if args.map_to_run:
    print "map_to_run: "+args.map_to_run
    map_to_run = args.map_to_run
if args.map_mode_to_run:
    print "map_mode_to_run: "+args.map_mode_to_run
    map_mode_to_run = args.map_mode_to_run

#define regions (as of version 0.0.4 loaded dynamically)
rgn_game = SCREEN
rgn_top_bar = SCREEN
rgn_top_left = SCREEN
rgn_top_right = SCREEN


# setting ctrl+space as a hotkey to tell the bot to quit gracefully at will
def runHotKey(event):
    global running
    running = False
Env.addHotkey(Key.SPACE, KeyModifier.CTRL, runHotKey)

def runHotKey2(event):
    print "Sikuli Killstroke^"
    exit(0)
Env.addHotkey(Key.ESC, KeyModifier.WIN, runHotKey2)

# Setup image collection based on screen size
if( SCREEN.getBounds().width >= 1920):
    import krBot1920
    reload(krBot1920)
    img_collection = krBot1920
else:
    import krBot1440
    reload(krBot1440)
    img_collection = krBot1440


def debug_run():
    setup_game_regions(0)
    chooseMap()
    startAutoRun()
    waitForEndLevel()
    #moveToMapNPC()
    #map = Pattern(img_collection.collection_maps[map_to_run])
    #if exists(map,1):
    #    print "[D1P00] 1920 exists as expected~"+map.getFilename()
    exit(0)
    
# slow left mouse click
def mouse_click(delay = 0.3, button = Button.LEFT):
    mouseDown(button)
    sleep(delay)
    mouseUp(button)

# used to make sure popups only run when popups are enabled
def notify(message, lv = 1, prefix = "[D1S00]"):
    if debug_popups and message:
        popup(message) 
    if message:
        print prefix+" "+message

# detects if the game is still open based on window title
def isGameOpen(): 
    global game, game_available
    game = App('KingsRoad')
    switchApp(game)
    game_available = game.hasWindow()
    notify(game.getWindow())
    return game_available

# Unused currently, but needs to check on the flash area and confirm flash didn't crash / stop working
def isFlashWorking():
    global img_collection
    return exists(img_collection.img_game_icon)
    sleep(1)

# This thing is pretty slow, need a different way to check if logged in
def maybeLogin():
    global logged_in, img_collection
    if exists(img_collection.img_play, 1):
        click(img_collection.img_play)
        logged_in = True
        sleep(3)
        return True
    elif exists(img_collection.img_refresh, 1):
        hover(img_collection.img_refresh)
        mouse_click(0.3)
        logged_in = True
        sleep(2)
        return True
    return False

def maybeClosePopups():
    global img_collection
    if exists( img_collection.img_toclose_2 ):
        click()
        sleep(1)
    if exists(img_collection.img_toclose):
        notify('Found a popup, closing and looking again.')
        click()
        sleep(1)
        if exists(img_collection.img_yesconfirm):
            click()
            sleep(1)
        # return continue as true, we found one and there may be another
        return True
    if exists( img_collection.img_teamviewer_icon, 1 ):
        click( img_collection.img_teamviewer_ok )
    else:
        # return continue as false, we are done
        notify('No more popups found, moving on.')
        return False

def closeAllPopups():
    global running, img_collection
    while ( running and maybeClosePopups() ):
        sleep(0.1)
        
def moveToMapNPC():
    global continue_run, img_collection
    npc_offset = int( SCREEN.getBounds().width * -1 * 0.075 )
    
    if exists( img_collection.img_gem ):
        hover( Pattern(img_collection.img_gem).targetOffset(5,50) )
        mouse_click(2, Button.RIGHT)
    if exists( img_collection.img_town_statue_arm ):
        #maybe use 0.075 % of width
        hover( Pattern(img_collection.img_town_statue_arm).targetOffset(npc_offset,0) )
        mouse_click(2)
        return True
    elif exists( img_collection.img_town_window ):
        hover ( Pattern(img_collection.img_mana_bar).targetOffset(0,-24) )
        mouse_click(2, Button.RIGHT)
        if exists( img_collection.img_gem ):
            hover( Pattern(img_collection.img_gem).targetOffset(5,50) )
            mouse_click(2, Button.RIGHT)
        if exists( img_collection.img_town_statue_arm ):
            hover( Pattern(img_collection.img_town_statue_arm).targetOffset(npc_offset,0) )
            mouse_click(2)
            return True
    elif exists( img_collection.img_town, 1 ):
        click()
        wait(1)
        if exists( img_collection.img_yesconfirm ):
            click()
            wait(4)
    else:
        continue_run = False
    return False

def maybeZoomOut():
    global rgn_top_right, img_collection
    notify("Trying to zoom out")
    with rgn_top_right:
        if exists( img_collection.img_zoomout, 1 ):
            click()
            notify("Zoomed out just now.")
            return True
        notify("Zoomed out already.") 
    return False

def chooseMap():
    global map_to_run, img_collection
    notify("Check for map image: " + img_collection.collection_maps[map_to_run].getFilename() )
    if exists( img_collection.collection_maps[map_to_run] ):
        click( img_collection.collection_maps[map_to_run] )
        notify('Whoa, found that map you were looking for ;)');
    else:
        notify('Sigh, maps image recog failed again.')

def chooseMode():
    global continue_run, img_collection
    if exists( img_collection.collection_modes[map_mode_to_run] ):
        click()
        sleep(0.5)
        notify('Hey man, I totally clicked on that map for you. Your welcome.')
        if exists( img_collection.img_playalone ):
            click()
            notify('Yup, we confirmed playing solo.')
        sleep(2)
        continue_run = True
    else:
        notify('Something went wrong during choosing the mode.')
        continue_run = False
        exit

def startAutoRun():
    global auto_run_count, continue_run, img_collection, rgn_bottom_right
    autorunning = False
    while not autorunning:
        if exists( img_collection.img_declineinvite, 1 ):
            click()
            wait(2)
        try:
            rgn_auto = wait( img_collection.img_auto, 20 )
            hover( rgn_auto )
            mouse_click()
            hover( rgn_auto.offset(Location(0, 50)) )
            sleep(2)
            autorunning = not exists( img_collection.img_auto, 1)
            if autorunning == True:
                auto_run_count = auto_run_count + 1
                print "Auto Running ["+str(auto_run_count)+"]"
        except FindFailed:
            continue_run = False
    if continue_run == True:
        notify('Confirmed auto running clicked.')
        maybeBlessing()
    
def maybeBlessing():
    global img_collection
    if exists( img_collection.img_free, 2 ):
        click()
    if exists( img_collection.img_acheivements, 2 ):
        click( Pattern(img_collection.img_acheivements).targetOffset(0,55) )
    notify("Blessing and popup closure complete.")

def waitForEndLevel():
    global game, continue_run, img_collection
    #this is where you could do dynamic observes to watch for items, open lockboxes, or collect acheivements
    notify("Waiting for end of level now... will try twice then return to town")
    attempt = 1
    success = False
    try:
        while attempt < 3 and not success and wait( img_collection.img_end_level, 300 ):
            notify("End of level found, returning to town")
            click ( img_collection.img_end_level )
            wait( img_collection.img_return_to_town, 10 )
            #image starts disabled wait a moment
            sleep(1)
            click( img_collection.img_return_to_town )
            success = not exists( img_collection.img_end_level )
            attempt = attempt + 1
            return True
    except FindFailed:
        notify("End of level failed, safest course of action is to refresh.")
        #game.close()
        click( img_collection.img_game_icon )
        wait(6)
        continue_run = False
    return False

def setup_game_regions(show = 0):
    global rgn_game, rgn_top_bar, rgn_top_left, rgn_top_right, rgn_bottom_left, rgn_bottom_right, img_collection
    try:
        wait(img_collection.img_game_icon, 30)
    except FindFailed:
        notify("Never found game region")
        return False
    try:
        icon = find(img_collection.img_game_icon)
        rgn_game = Region(icon.x, icon.y+icon.h, icon.right().w,icon.below().h)
        rgn_game.highlight(show)
        hover(rgn_game.getCenter())
        rgn_top_bar = Region(icon.x, icon.y, icon.right().w,icon.h)
        rgn_top_bar.highlight(show)
        rgn_top_left = Region(icon.x, icon.y+icon.h, rgn_game.getCenter().x,rgn_game.getCenter().y-(icon.y+icon.h))
        rgn_top_left.highlight(show)
        rgn_top_right = Region(rgn_game.getCenter().x, icon.y+icon.h, rgn_game.getCenter().x,rgn_game.getCenter().y-(icon.y+icon.h))
        rgn_top_right.highlight(show)
        rgn_bottom_left = Region(icon.x, rgn_game.getCenter().y, rgn_game.getCenter().x,rgn_game.getCenter().y-(icon.y+icon.h))
        rgn_bottom_left.highlight(show)
        rgn_bottom_right = Region(rgn_game.getCenter().x, rgn_game.getCenter().y, rgn_game.getCenter().x,rgn_game.getCenter().y-(icon.y+icon.h))
        rgn_bottom_right.highlight(show)
        return True
    except FindFailed:
        notify("Error: Game icon disappeared")
        return False

op_play_type = ("autoplay", "autoplay-notify", "debug")
if( not force_start_mode ):
    option = select("Please choose a bot play type", options = op_play_type);
else:
    option = force_start_mode

# main constructor (init run)
while( running ):
    notify("Running Loop - moving to chosen play type.")
    if option == "debug":
        debug_run()
        option = select("Please choose a bot play type", options = op_play_type);
    elif option == "autoplay" or option == "autoplay-notify":
        if option == "autoplay-notify":
            debug_popups = True
        if False == isGameOpen():
            notify("Opening browser, game not found.")
            openApp(r"C:\Program Files\Google\Chrome\Application\chrome.exe https://apps.facebook.com/kingsroadgame/ -start-maximized")
            logged_in = False
            sleep(5)
        else:
            # Reset continue run since we are starting over here 
            continue_run = True
            setup_game_regions()
            if False == logged_in:
                sleep(0.1)
                notify('Not logged in yet :(')
            if maybeLogin():
                sleep(0.1) #do anything on login?
            if logged_in:
                notify('Found you logged in!')
                closeAllPopups()
                if( moveToMapNPC() ):
                    notify("Phew, found the map dude.")
                    if( continue_run ):
                        maybeZoomOut()
                    if( continue_run ):
                        chooseMap()
                    if( continue_run ):
                        chooseMode()
                    if( continue_run ):
                        startAutoRun()
                        notify('Stepping into waitForEndLevel')
                    if( continue_run ):
                        notify("Beginning waitforEndLevel")
                        waitForEndLevel()
                        notify("End of waitForEndLevel")
              #end of main loop, starting over
    else:
        running = False
# END OF FILE
notify("KingsRoad Is Complete!")
