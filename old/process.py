"""Created by jwkania to process five faint pulsars.C26OCT2017:U26OCT2017"""
import os,fnmatch
#loopnumber = 0
verbose = True#prints out tests
pulsars = ["1929+16","1929+19"] #list of pulsars you want to process.

for pulsar in pulsars:
    for dirname, dirnames, filenames  in os.walk('..'):
        if '.git' in dirnames:#removes git dir
            dirnames.remove('.git')
        if verbose: print("dirname = {0}".format(dirname))
        goAgain = 0;
        while (goAgain < 5):
            containsFIT = False; fitsNUMs=[];fitsNAME=[];
            for fileNAME in filenames:
                if verbose: print("fileNAME= {0}".format(fileNAME))
                if fnmatch.fnmatch(fileNAME,'*{0}*.fits'.format(pulsar)):
                    if verbose: print("Examining: {0}".format(fileNAME))
                    containsFIT = True
                    fitsNUMs.append("_".join([(fileNAME.split('.')[0]).split('_')[-2], (fileNAME.split('.')[0]).split('_')[-1]]))#parses .fits file to get number
                    fitsNAME.append(fileNAME)
                    if verbose: print("fitsNUMs={0}".format(fitsNUMs))
 
            for filename in filenames:
                #print(len(fitsNUMs))
                for i, fitsNUM in enumerate(fitsNUMs):
                    containsPFD = False
                    print(pulsar)
                    if fnmatch.fnmatch(filename,'*{0}_PSR_{1}.pfd'.format(fitsNUM,pulsar)):
                        print("filename={0}".format(filename))
                        containsPFD = True
                        print("os.path.isfile(format(pulsar,filename))= {0}".format(os.path.isfile("./{0}/{1}".format(pulsar,filename))))
                        if not os.path.isfile("./{0}/{1}".format(pulsar,filename)):
                            print("You need {0} in {1}".format(filename,pulsar))
                            os.system("cp {0}/{1} ./{2}".format(dirname,filename, pulsar))
                    if (containsFIT) and (not containsPFD):
                        print('You need a PFD {0}_PSR_{1}.pfd file in {2}'.format(fitsNUM,pulsar,dirname))
                        os.system("prepfold -timing /gbo/AGBT17A_477/{0}.par /gbo/AGBT17A_477{1}/{2} -noxwin".format(pulsar,dirname[2:],fitsNAME[i]))#tries to make the pfd file, par one up
                    else:
                        goAgain = 10 #ends the loop after all fits files have been made
            print("goAgain = {0}".format(goAgain))
            goAgain = goAgain + 1#kills the loop after 10 tries 
    """
    for subdirnames in dirnames:
        print(os.path.join(dirname, subdirnames))

    for filename in filenames:
        print(os.path.join(dirname,filename))

    print("\n\n")
    loopnumber = loopnumber +1 

print loopnumber
"""
