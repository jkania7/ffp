"""jwk C2NOV2017, invoke with pyhton process.py"""
import os, fnmatch, glob
from subprocess import call
pulsarS=['1929+19','1929+16']#list of pulsars to process
vverbose = False; verbose= True
for (dirPATH, dirNAMEs, fileNAMEs) in os.walk('/gbo/AGBT17A_477/'):#dirPATH is path to dirctory
    #dirNames is all subdirs in a dir filesNames is all the files
    if '.git' in dirNAMEs:
        dirNAMEs.remove('.git')
    
    if verbose: print("\ndirPATH = {0}".format(dirPATH))
    if vverbose: print("dirNAMEs = {0}".format(dirNAMEs))
    if vverbose: print("fileNAMEs = {0}\n".format(fileNAMEs))
    for pulsar in pulsarS:
        for file in fileNAMEs:#looks for fits files
            if fnmatch.fnmatch(file, '*{0}*.fits'.format(pulsar)):
                if verbose: print("I have .fits {0}/{1}".format(dirPATH,file))
                #looking for correspnding pfd
                fitsNUM = "_".join((file.split('.')[0]).split('_')[-2:])
                pfd =  glob.glob('{0}/*{1}.pfd'.format(dirPATH,pulsar, fitsNUM))#This is an array
                if (len(pfd)>1): #multiple pfd 
                    print("Something is wrong with the pfd matching, or you have more than one pfd,killing script")
                    exit()
                elif (len(pfd) == 1 ): #one pfd
                    if verbose: print("I have .pfd {0}".format(pfd[0]))
                elif ( len(pfd) == 0 ):#doesn't find pfd
                    print("Creating pfd for {0}".format(file))
                    f = open("/gbo/AGBT17A_477/share/outputs/{0}.out".format(file),'a')#A file outputs of the runs
                    call(["echo", "prepfold","-timing","/gbo/AGBT17A_477/{0}.par".format(pulsar),"{0}/{1}".format(dirPATH,file),"-noxwin"])
                    call([ "prepfold","-timing","/gbo/AGBT17A_477/{0}.par".format(pulsar),"{0}/{1}".format(dirPATH,file),"-noxwin"],stdout=f)
                pfd =  glob.glob('{0}/*{1}.pfd'.format(dirPATH,pulsar, fitsNUM))
                if (len(pfd) == 0): print("Didn't create pfd, killing script"); exit()
                call(["echo","rsync","-at","{0}".format(pfd[0]),"/gbo/AGBT17A_477/share/{0}/".format(pulsar)]) 
                call(["rsync","-at","{0}".format(pfd[0]),"/gbo/AGBT17A_477/share/{0}/".format(pulsar)])  
