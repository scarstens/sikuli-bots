# import related libraries
import os, inspect, sikuli
# Pulls all sikuli modules for use here
from sikuli import *

# Start subscript by changing bundle (images) directory
print "[S2P00] LOADED: krBot1920:R108"
print "[S2P01] Old Image Path: "+sikuli.getBundlePath()
path_current_file = os.path.dirname( inspect.getfile(inspect.currentframe()) )
sikuli.setBundlePath(path_current_file)
print "[S2P02] New Image Path: "+sikuli.getBundlePath()

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


collection_maps = (Pattern("adamars_sanctum.png").similar(0.60),"inner_circle.png","battlements.png")
collection_npcs = (Pattern("npc_world.png").targetOffset(-3,23),Pattern("npc_helm.png").targetOffset(-2,29),Pattern("npc_dungeon-1.png").targetOffset(1,-70),Pattern("npc_swords.png").targetOffset(0,27),)
collection_modes = ("mode_normal.png","mode_heroic.png","mode_champion.png")
collection_lockboxes = ("lockbox_bossdrop.png","lockbox_dragon_blue.png","lockbox_prism.png","lockbox_skillrune.png","lockbox_heroessence.png",Pattern("locbox_xp.png").similar(0.80),"lockbox_tournament.png","lockbox_tournament_2.png")
collection_tournament_modes = ("tournament_mode_bronze.png","tournament_mode_silver.png","tournament_mode_gold.png")
