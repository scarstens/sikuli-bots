# TODO:
# OPEN LOCKBOXES: http://doc.sikuli.org/finder.html?highlight=rows


# Global Settings to start with - these can be changed later
Settings.MoveMouseDelay = 0.5 # default 2 times a second
Settings.ObserveScanRate = 0.333 # default 3 times a second
Settings.DelayBeforeMouseDown = 0.5 # only applies to next click
setShowActions(True)
#setFindFailedResponse(PROMPT) # try forver on fail - doesn't seem to play nice right now

# define globals
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


#define regions (as of version 0.0.4 loaded dynamically)
rgn_game = Screen
rgn_top_bar = Screen
rgn_top_left = Screen
rgn_top_right = Screen

# define images
img_game_icon = "img_game_icon.png"
img_play = "img_play.png"
img_refresh = Pattern("img_refresh.png").similar(0.80)
img_toclose = "img_toclose.png"
img_toclose_2 = "img_toclose_2.png"
img_yesconfirm = Pattern("img_yesconfirm.png").similar(0.85)
img_gem = Pattern("img_gem.png").similar(0.85)
img_town_statue_arm = Pattern("img_town_statue_arm.png").similar(0.80)
img_town_window = "img_town_window.png"
img_mana_bar = "img_mana_bar.png"
img_zoomout = Pattern("img_zoomout.png").similar(0.95)
img_goldbonus = Pattern("img_goldbonus.png").similar(0.40)
img_declineinvite = "img_declineinvite.png"
img_accept = "img_accept.png"
img_playalone = "img_playalone.png"
img_auto = Pattern("img_autoplay.png").similar(0.85)
img_free = "img_free.png"
img_acheivements = "img_acheivements.png"
img_end_level = "img_end_level.png"
img_boss_drops = Pattern("img_boss_drops.png").similar(0.50).targetOffset(-46,7)
img_return_to_town = "img_return_to_town.png"

# image collections


collection_maps = ("adamars_sanctum.png","inner_circle.png","battlements.png")
collection_maps_2 = (Pattern("maps_2_adamarssanctum.png").similar(0.50),"map_2_innercircle.png", "map_2_snake.png")
collection_npcs = (Pattern("npc_world.png").targetOffset(-3,23),Pattern("npc_helm.png").targetOffset(-2,29),Pattern("npc_dungeon-1.png").targetOffset(1,-70),Pattern("npc_swords.png").targetOffset(0,27),)
collection_modes = ("mode_normal.png","mode_heroic.png","mode_champion.png")
collection_lockboxes = ("lockbox_bossdrop.png","lockbox_dragon_blue.png","lockbox_prism.png","lockbox_skillrune.png","lockbox_heroessence.png",Pattern("locbox_xp.png").similar(0.80),"lockbox_tournament.png","lockbox_tournament_2.png")
collection_tournament_modes = ("tournament_mode_bronze.png","tournament_mode_silver.png","tournament_mode_gold.png")

# setting ctrl+space as a hotkey to tell the bot to quit gracefully at will
def runHotKey(event):
    global running
    running = False
Env.addHotkey(Key.SPACE, KeyModifier.CTRL, runHotKey)

# slow left mouse click
def left_mouse_click():
    mouseDown(Button.LEFT)
    sleep(0.3)
    mouseUp(Button.LEFT)

# used to make sure popups only run when popups are enabled
def notify(message):
    if debug_popups and message:
        popup(message)

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
    return exists(img_game_icon)
    sleep(1)

# This thing is pretty slow, need a different way to check if logged in
def maybeLogin():
    global logged_in
    if exists(img_play, 1):
        click(img_play)
        logged_in = True
        sleep(3)
        return True
    elif exists(img_refresh, 1):
        hover(img_refresh)
        left_mouse_click()
        logged_in = True
        sleep(2)
        return True
    return False

def maybeClosePopups():
    if exists(img_toclose):
        notify('Found a popup, closing and looking again.')
        click(img_toclose)
        sleep(1)
        if exists(img_yesconfirm):
            click(img_yesconfirm)
            sleep(1)
        # return continue as true, we found one and there may be another
        return True
    else:
        # return continue as false, we are done
        notify('No more popups found, moving on.')
        return False

def closeAllPopups():
    global running
    while ( running and maybeClosePopups() ):
        sleep(0.1)

def moveToMapNPC():
    global continue_run
    if exists( img_gem ):
        hover( Pattern(img_gem).targetOffset(5,50) )
        mouseDown(Button.RIGHT)
        sleep(2)
        mouseUp(Button.RIGHT)
    if exists( img_town_statue_arm ):
        hover( Pattern(img_town_statue_arm).targetOffset(-110,0) )
        mouseDown(Button.LEFT)
        sleep(2)
        mouseUp(Button.LEFT)
        return True
    elif exists( img_town_window ):
        hover ( Pattern(img_mana_bar).targetOffset(0,-24) )
        mouseDown(Button.RIGHT)
        sleep(2)
        mouseUp(Button.RIGHT)
        if exists( img_gem ):
            hover( Pattern(img_gem).targetOffset(5,50) )
            mouseDown(Button.RIGHT)
            sleep(2)
            mouseUp(Button.RIGHT)
        if exists( img_town_statue_arm ):
            hover( Pattern(img_town_statue_arm).targetOffset(-110,0) )
            mouseDown(Button.LEFT)
            sleep(2)
            mouseUp(Button.LEFT)
            return True
    else:
        continue_run = False
    return False

def maybeZoomOut():
    global rgn_top_right
    notify("Trying to zoom out")
    with rgn_top_right:
        if exists( img_zoomout, 1 ):
            click( img_zoomout )
            notify("Zoomed out just now.")
            return True
        notify("Zoomed out already.") 
    return False

def chooseMap():
    global map_to_run
    notify("Check for map image: " + collection_maps_2[map_to_run].getFilename() )
    if exists( collection_maps_2[map_to_run] ):
        click( collection_maps_2[map_to_run] )
        notify('Whoa, found that map you were looking for ;)');
    else:
        notify('Sigh, maps image recog failed again.')

def chooseMode():
    global continue_run
    if exists( collection_modes[map_mode_to_run] ):
        click( collection_modes[map_mode_to_run] )
        sleep(0.5)
        notify('Hey man, I totally clicked on that map for you. Your welcome.')
        if exists( img_playalone ):
            click( img_playalone )
            notify('Yup, we confirmed playing solo.')
        sleep(2)
        continue_run = True
    else:
        notify('Something went wrong during choosing the mode.')
        continue_run = False
        exit

def startAutoRun():
    autorunning = False
    while not autorunning:
        rgn_auto = wait( img_auto, 20 )
        hover( rgn_auto )
        left_mouse_click()
        hover( rgn_auto.offset(Location(0, 50)) )
        sleep(2)
        autorunning = not exists( img_auto, 1)
    notify('Confirmed auto running clicked.')
    maybeBlessing()
    
def maybeBlessing():
    if exists( img_free ):
        click( img_free )
    if exists( img_acheivements ):
        click( Pattern(img_acheivements).targetOffset(0,55) )
    notify("Blessing and popup closure complete.")

def waitForEndLevel():
    global game, continue_run
    notify("Waiting for end of level now... will try twice then return to town")
    attempt = 1
    success = False
    while attempt < 3 and not success and wait( img_end_level, 300 ):
        notify("End of level found, returning to town")
        click ( img_end_level )
        wait( img_return_to_town, 10 )
        #image starts disabled wait a moment
        sleep(1)
        click( img_return_to_town )
        success = not exists( img_end_level )
        attempt = attempt + 1
        return True
    notify("End of level failed, safest course of action is to refresh.")
    game.close()
    continue_run = False
    return False

def setup_game_regions(show = 0):
    global rgn_game, rgn_top_bar, rgn_top_left, rgn_top_right, rgn_bottom_left, rgn_bottom_right
    try:
        wait(img_game_icon, 30)
    except FindFailed:
        notify("Never found game region")
        return False
    try:
        icon = find(img_game_icon)
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
        #hover(rgn_top_bar)
        return True
    except FindFailed:
        notify("Error: Game icon disappeared")
        return False

op_play_type = ("autoplay", "autoplay-notify", "debug")
option = select("Please choose a bot play type", options = op_play_type);

# main constructor (init run)
while( running ):
    notify("Running Loop - moving to chosen play type.")
    if option == op_play_type[2]:
        setup_game_regions(0)
        waitForEndLevel()
        option = select("Please choose a bot play type", options = op_play_type);
    else:
        if option == op_play_type[1]:
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
# END OF FILE
popup("KingsRoad Is Complete!")
