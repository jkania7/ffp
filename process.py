"""Created by jwkania to process five faint pulsars.C26OCT2017:U26OCT2017"""
import os,fnmatch
#loopnumber = 0
verbose=True #prints out tests
pulsars=["1929+16"] #list of pulsars you want to process.

for pulsar in pulsars:
    for dirname,dirnames, filenames  in os.walk('..'):
        if '.git' in dirnames:#removes git dir
            dirnames.remove('.git')
        if verbose: print("dirname = {0}".format( dirname))
        goAgain = True
        while goAgain:
            containsFit = False; contiansPFD = False; fitsNUM=[];fitsNAME=[];
            for fitsNAME in filenames:
                if verbose: print("fitsNAME= {0}".format(fitsNAME))
                if fnmatch.fnmatch(fitsNAME,'*{0}*.fits'.format(pulsar)):
                    containsFIT = True
                    fitsNUM = (fitsNAME.split('.')[0]).split('_')[-1]#parses .fits file to get number
                    if verbose: print("fitsNUM={0}".format(fitsNUM))

            for filename in filenames:
                if fnmatch.fnmatch(filename,'*{0}_PSR_{1}.pfd'.format(fitsNUM,pulsar)):
                    containsPFD = True
                    if  any(os.path.isfile(os.path.join("./{0}/".format(pulsar),i)) for i in os.listdir("./{0}/".format(pulsar))):
                        print("You need a {0}/".format(pulsar))
            if containsFit and not containsPFD:
                print('You need a PFD {0}_PSR_{1}.pfd file in {1}'.format(fitsNum,pulsar,dirname))
                os.system("predfold -timing ../{0}.par {1}/{2}".format(pulsar,dirname,fitsNAME))#tries to make the pfd file, par one up
            else:
                goAgain = False #ends the loop after all fits files have been made
    """
    for subdirnames in dirnames:
        print(os.path.join(dirname, subdirnames))

    for filename in filenames:
        print(os.path.join(dirname,filename))

    print("\n\n")
    loopnumber = loopnumber +1 

print loopnumber
"""
