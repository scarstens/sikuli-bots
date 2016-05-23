
bundlepath = getBundlePath()
execfile( bundlepath+"/getres.sikuli/getres.py" )
dogetres()
setBundlePath(bundlepath+libImg) # could also be a statement in myImages.sikuli
execfile( bundlepath+libImg+"myImages.py" ) # to make the image variables known
execfile( bundlepath+libFunc+"/myfunctions.py" ) # to make your functions available

def test2():
    if exists(imgtest):
        popup(imgtest.getFilename())
test1()
test2()




