"""jwk C2NOV2017, invoke with python process.py"""
import os, fnmatch, glob
from subprocess import call
pulsarS=['1929+16','1929+19']#list of pulsars to process
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

for pulsar in pulsarS:
    toDO = open("/gbo/AGBT17A_477/share/{0}/toDO.txt".format(pulsar),'w')
    toDO.write("THIS FILE IS REWRITTEN EVERYTIME process.py IS RUN\n")
    toDO.write("This is a list of pfds that need to be flagged and 'echo show_pfd>>log.dat'ed \n")
    #Is compares the lsit of pfd files to files that have been flagged and added to log.dat
    for file in glob.glob('/gbo/AGBT17A_477/share/{0}/*.pfd'.format(pulsar)):
        file = file.split('/')[-1]#Splits off dir info from glob
        foundINlog = False
        for log in open("/gbo/AGBT17A_477/share/{0}/log.dat".format(pulsar),'r'):
            if vverbose: print("file = {0}".format(file))
            if vverbose: print("log = {0}".format(log))
            if fnmatch.fnmatch(log, "*{0}*".format(file)):
                if verbose: print("Found {0} as pfd and in log.dat, its flagged".format(file))
                foundINlog = True
                
        if (not foundINlog):
            toDO.write("{0}\n".format(file))
