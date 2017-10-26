import os,fnmatch
#loopnumber = 0
for dirname,dirnames, filenames  in os.walk('..'):
    if '.git' in dirnames:
        dirnames.remove('.git')

    containsFit = False; contiansPFD = False
    for filename in filenames:
        if fnmatch.fnmatch(filename,'1929+16*.fit'):
            containsFIT = True
        if fnmatch.fnmatch(filename,'_1929+16.pfd'):
            containsPFD = True
    if containsFit and not containsPFD:
        print('I need a PFD file in {0}'.format(dirname))
    """
    for subdirnames in dirnames:
        print(os.path.join(dirname, subdirnames))

    for filename in filenames:
        print(os.path.join(dirname,filename))

    print("\n\n")
    loopnumber = loopnumber +1 

print loopnumber
"""
