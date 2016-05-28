from sikuli import *

rgn_flash = Region(129,209,2277,1750)
rgn_th = Region(128,267,2280,894)

img_play = "img_play.png"
rgn_img_play = Region(1291,381,899,408)
img_refresh = "img_refresh.png"
rgn_img_refresh = Region(1283,1172,554,252)

img_specofferclose = Pattern("img_specofferclose.png").similar(0.80)
rgn_img_specofferclose = Region(1622,573,160,131)
rgn_img_offerclosetr = Region(2241,387,156,136)

img_closeyes = "img_closeyes.png"
rgn_img_closeyes = Region(1235,1064,370,232)

img_dailybonus = "img_dailybonus.png"
rgn_img_dailybonus = Region(2200,352,209,275)

img_zoomout = Pattern("img_zoomout.png").similar(0.90)
img_closemap = "img_closemap.png"
rgn_img_mapbtn = Region(1704,226,602,216)



img_adamar = "img_adamar.png"
rgn_img_adamar = Region(1651,405,341,345)
img_champ = "img_champ.png"
rgn_img_champ = Region(1574,1439,369,185)
img_alone = "img_alone.png"
rgn_img_alone = Region(912,1092,381,155)
img_mapobj = "img_mapobj.png"
rgn_img_mapobj = Region(2205,352,200,208)

img_freebuff = "img_freebuff.png"
rgn_img_freebuff = Region(755,1504,296,176)
rgn_closebuff = Region(1746,1163,65,67)
img_auto = Pattern("img_auto.png").similar(0.96)
rgn_img_auto = Region(2231,1549,148,193)
img_endlevel = "img_endlevel.png"
rgn_img_endlevel = Region(1058,1558,265,167)
img_returntown = "img_returntown.png"
rgn_img_returntown = Region(1088,1594,214,141)

img_gem = "img_gem.png"
img_town_statue_arm = "img_town_statue_arm.png"
img_town_window = "img_town_window.png"
img_mana_bar = "img_mana_bar.png"
img_mapnpc = Pattern("img_mapnpc.png").similar(0.92)