
bundlepath = getBundlePath()



#just need to dynamically set the below based on current resolution




#def dosetthreebytwo():
libImg = "/3000x2000/myimages.Sikuli/"
execfile( bundlepath+libImg+"myImages.py" ) # to make the image variables known
setBundlePath(bundlepath+libImg) # could also be a statement in myImages.sikuli

libFunc = "/3000x2000/myfunctions.Sikuli"
execfile( bundlepath+libFunc+"/myfunctions.py" ) # to make your functions available

def test2():
    if exists(imgtest):
        popup("image found")
test1()
test2()




