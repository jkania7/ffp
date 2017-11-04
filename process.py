"""jwk C2NOV2017, invoke with python process.py"""
import os, fnmatch, glob, shlex
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
    with open("/gbo/AGBT17A_477/share/{0}/toDO.txt".format(pulsar),'w') as toDO:
        toDO.write("THIS FILE IS REWRITTEN EVERYTIME process.py IS RUN\n")
        toDO.write("This is a list of pfds that need to be flagged and 'echo show_pfd>>log.dat'ed \n")
        #Is compares the lsit of pfd files to files that have been flagged and added to log.dat
        for file in glob.glob('/gbo/AGBT17A_477/share/{0}/*.pfd'.format(pulsar)):
            file = file.split('/')[-1]#Splits off dir info from glob
            foundINlog = False
            with open("/gbo/AGBT17A_477/share/{0}/log.dat".format(pulsar),'r') as logS:
                for log in logS:
                    if vverbose: print("file = {0}".format(file))
                    if vverbose: print("log = {0}".format(log))
                    if fnmatch.fnmatch(log, "*{0}*".format(file)):
                        if verbose: print("Found {0} as pfd and in log.dat, its flagged".format(file))
                        foundINlog = True
                        print("log = {0}".format(log))
                        parsed =  shlex.split(log)
                        p=[];i=[];k=[];
                        if vverbose: print("parsed={0}".format(parsed))
                        if vverbose: print("len(parsed)={0}".format(len(parsed)))
                        if vverbose: print("range(len(parsed))={0}".format(range(len(parsed))))
                        for q in range(len(parsed)):
                            if (parsed[int(q)] == "show_pfd"):
                                p = parsed[q+1]
                            elif (parsed[q] == "-killsubs"):
                                k = parsed[q+1]
                            elif parsed[q] == "-killparts":
                                i = parsed[q+1]
                        with open("/gbo/AGBT17A_477/share/{0}/toaMAKER".format(pulsar),'a+') as toaLIST:

                            if any(fnmatch.fnmatch(toa, "*{0}*".format(p)) for toa in toaLIST):
                                if verbose: print("I've found {0} in ../{1}/toaMAKER".format(p, pulsar))
                            else:
                                if (len(i)>0 and len(k)>0):
                                    if verbose: print("get_TOAs.py -n -g 0.1 -k {0}\t-i {1}\t{2}\n".format(k,i,p) )
                                    toaLIST.write("get_TOAs.py -n -g 0.1 -k {0}\t\t-i {1}\t{2}\n".format(k,i,p) )
                                elif (len(i)==0 and len(k)>0):
                                    if verbose: print("get_TOAs.py -n -g 0.1 -k {0}\t\t\t{1}\n".format(k,p) )
                                    toaLIST.write("get_TOAs.py -n -g 0.1 -k {0}\t\t\t{1}\n".format(k,p) )
                                elif (len(i)>0 and len(k)==0):
                                    if verbose: print("get_TOAs.py -n -g 0.1 -i {0}\t\t\t{1}\n".format(i,p) )
                                    toaLIST.write("get_TOAs.py -n -g 0.1 -i {0}\t\t\t{1}\n".format(i,p) )
                                elif (len(i)==0 and len(k)==0):
                                    if verbose: print("get_TOAs.py -n -g 0.1\t\t\t{0}\n".format(p) )
                                    toaLIST.write("get_TOAs.py -n -g 0.1\t\t\t{0}\n".format(p) )
                                else:
                                    print("Someting is wrong with the log.dat {0}".format(p))
                if (not foundINlog):
                    toDO.write("{0}\n".format(file))
