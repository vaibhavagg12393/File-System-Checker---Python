'''

File System Checker

Coded By: 
Name: Swena Gupta
Net ID: sg4423
N#: N13186820
It is assumed that the all the fusedata files are kept in ./FS

'''
import sys           
import json
import time
import calendar
import math
import os
import ast
filepath="FS/fusedata.";
blocksize=4096;


# Function in order to check if all the times are in the past and nothing in future. It also updates the time to present time if the condition doesn't satisfy

def timechecker(timeinode,ptime,timestr,loc,dirname):
    for key,value in timeinode.iteritems():
        if timestr.lower() in key.lower():
            if(value>ptime):
                print "Error: Wrong "+key+" in "+dirname+"\n"
                timeinode[key]=presenttime
                filewp=open(filepath+str(loc),"w")
                json.dump(timeinode,filewp,indent=4)
                filewp.close()
                print key+" updated in "+dirname+"\n"
            else:
                print "Right value of "+key+" in "+dirname+"\n"
    for tinode in timeinode["filename_to_inode_dict"]:
        if tinode["type"]=='d':
            if tinode["name"]!="." and tinode["name"]!="..":
                newloc=tinode["location"]
                newdir=tinode["name"]
                fp1=open(filepath+str(newloc),"r").read()
                newnode=json.loads(fp1)
                timechecker(newnode,ptime,timestr,newloc,newdir)
        elif tinode["type"]=='f':
            newloc=tinode["location"]
            newdir=tinode["name"]
            fp1=open(filepath+str(newloc),"r").read()
            timeinode=json.loads(fp1)
            for key,value in timeinode.iteritems():
                if timestr.lower() in key.lower():
                    if(value>ptime):
                        print "Error: Wrong "+key+" in "+newdir+"\n"
                        timeinode[key]=presenttime
                        filewp=open(filepath+str(newloc),"w")
                        json.dump(timeinode,filewp,indent=4)
                        filewp.close()
                        print key+" updated in "+newdir+"\n"
                    else:
                        print "Right value of "+key+" in "+newdir+"\n"   

# Function in order to check if each directory contains . and .. and their block numbers are correct. It also modifies the block numbers to their correct values if they are incorrect and also add the directories if they are missing 

def dotdirchecker(par,cur,name,subfuninode):
    countsub=0
    parentloc=par
    currentloc=cur
    currentdirname=name
    countdict=0
    countdotdict=0
    flag1=0
    flag2=0
    for subnestedjson in subfuninode["filename_to_inode_dict"]:
        if subnestedjson["type"]=='d':
            flagdot=0
            flagdotdot=0
            if subnestedjson["name"] in ".":
                if subnestedjson["location"]!=currentloc:
                    print "Error: Wrong location of "+subnestedjson["name"]+" directory in "+currentdirname+"\n"
                    flagdot=1
                else:
                    print "Right location of "+subnestedjson["name"]+" directory in "+currentdirname+"\n"
                flag1=1
                countdotdict=countdotdict+1
            elif subnestedjson["name"] in "..":
                if subnestedjson["location"]!=parentloc:
                    print "Error: Wrong location of "+subnestedjson["name"]+" directory in "+currentdirname+"\n"
                    flagdotdot=1
                else:
                    print "Right location of "+subnestedjson["name"]+" directory in "+currentdirname+"\n"
                flag2=1
                countdotdict=countdotdict+1
            if flagdot==1:
                subfuninode["filename_to_inode_dict"][countdict]["location"]=currentloc
            elif flagdotdot==1:
                subfuninode["filename_to_inode_dict"][countdict]["location"]=parentloc
            if flagdot==1 or flagdotdot==1:
                filewp=open(filepath+str(currentloc),"w")
                json.dump(subfuninode,filewp,indent=4)
                filewp.close()
                print "location updated in "+currentdirname+"\n"
        countdict=countdict+1
    for nodejson in subfuninode["filename_to_inode_dict"]:
        if nodejson["type"]=='d':
            if nodejson["name"]!="." and nodejson["name"]!="..":
                newloc=nodejson["location"]
                newdirname=nodejson["name"]
                fp2=open(filepath+str(newloc),"r").read()
                newinode=json.loads(fp2)
                dotdirchecker(currentloc,newloc,newdirname,newinode)
  
    if flag1==0:
        subinode["filename_to_inode_dict"].append({"type":'d',"name":".","location":str(currentloc)})
        print "Error: Missing . in "+currentdirname+" inode\n"
    if flag2==0:
        subinode["filename_to_inode_dict"].append({"type":'d',"name":"..","location":str(parentloc)})
        print "Error: Missing .. in "+currentdirname+" inode\n"
    filewp=open(filepath+str(currentloc),"w")
    json.dump(subinode,filewp,indent=4)
    filewp.close()
    if flag1==1 and flag2!=1:
        print "Added .. in "+currentdirname+" inode\n"
    elif flag1!=1 and flag2==1:
        print "Added . in "+currentdirname+" inode\n"
    elif flag1!=1 and flag2!=1:
        print "Added . and .. in "+currentdirname+" inode\n"


# Function in order to check that if indirect=1, then the data pointed to by the location pointer is an array. It also updates the indirect value if the data is not an array 

def arraychecker(fileinode):
    for fjson in fileinode["filename_to_inode_dict"]:
        if fjson["type"]=='f':
            loc=fjson["location"]
            fp=open(filepath+str(loc),"r").read()
            filenode=json.loads(fp)
            if filenode["indirect"]==1:
                arrloc=filenode["location"]
                filerp=open(filepath+str(arrloc),"r")
                strfile=filerp.read()
                strfilenew=strfile[1:-1]
                if strfile[0]=='[' and strfile[-1]==']':
                    arrval=strfilenew.split(",")
                    flagno=0
                    for x in arrval:
                        if not x.isdigit():
                            flagno=1
                    if flagno!= 1:
                        print fjson["name"]+" has indirect=1 and also the data in the block pointed to by the location pointer is an array\n"

                    else:
                        print "Error: "+fjson["name"]+" has indirect=1 but the data in the block pointed to by the location pointer is not an array. Hence, updating the indirect to 0"
                        filenode["indirect"]=0
                        filewp=open(filepath+str(loc),"w")
                        json.dump(filenode,filewp,indent=4)
                        filewp.close()
                        print "\nindirect updated\n"
                else:
                   print "Error: "+fjson["name"]+" has indirect=1 but the data in the block pointed to by the location pointer is not an array. Hence, updating the indirect to 0"
                   filenode["indirect"]=0
                   filewp=open(filepath+str(loc),"w")
                   json.dump(filenode,filewp,indent=4)
                   filewp.close()
                   print "\nindirect updated\n" 
            else:
                print "indirect=0 for "+fjson["name"]+". Hence, not checking the block pointed to by the location pointer\n";                   

        elif fjson["type"]=='d':
            if fjson["name"] != '.' and fjson["name"] != '..':
                newloc=fjson["location"]
                filenewrp=open(filepath+str(newloc),"r").read()
                dirinode=json.loads(filenewrp)
                arraychecker(dirinode) 

# Function in order to validate the size of the file with the number of block pointers in the location array. It also updates the size if it does not validate

def sizechecker(fileinode):
    for fjson in fileinode["filename_to_inode_dict"]:
        if fjson["type"]=='f':
            loc=fjson["location"]
            fp=open(filepath+str(loc),"r").read()
            filenode=json.loads(fp)
            if filenode["indirect"]==0:
                if filenode["size"]>=blocksize:
                    print "Error: Wrong filesize of "+fjson["name"]+" which should be smaller in size than a blocksize\n"
                    filenode["size"]=blocksize-1
                    filewp=open(filepath+str(loc),"w")
                    json.dump(filenode,filewp,indent=4)
                    filewp.close()
                    print "Filesize updated\n"
                else:
                    print "Right filesize of "+fjson["name"]+" which had to be smaller in size than a blocksize\n"
            else:
                newloc=filenode["location"]
                fp3=open(filepath+str(newloc),"r").read()
                fparr=ast.literal_eval(fp3)
                arrlen=len(fparr)
                if filenode["size"]>(blocksize*arrlen):
                    print "Error: Wrong filesize of "+fjson["name"]+" which should be less than "+str(arrlen)+"*"+str(blocksize)+"\n"
                    newloc=filenode["location"]
                    fp3=open(filepath+str(newloc),"r").read()
                    fparr=ast.literal_eval(fp3)
                    arrlen=len(fparr)
                    filenode["size"]=(arrlen*blocksize)-1
                    filewp=open(filepath+str(loc),"w")
                    json.dump(filenode,filewp,indent=4)
                    filewp.close()
                    print "Filesize of "+fjson["name"]+" updated\n"
                    
                elif filenode["size"]<((blocksize*arrlen)-1):
                    print "Error: Wrong filesize of "+fjson["name"]+" which should be greater than ("+str(arrlen)+"*"+str(blocksize)+")-1\n"
                    newloc=filenode["location"]
                    fp3=open(filepath+str(newloc),"r").read()
                    fparr=ast.literal_eval(fp3)
                    arrlen=len(fparr)
                    filenode["size"]=(arrlen*blocksize)
                    filewp=open(filepath+str(loc),"w")
                    json.dump(filenode,filewp,indent=4)
                    filewp.close()
                    print "Filesize of "+fjson["name"]+" updated\n"
                else:
                    print "Right filesize of "+fjson["name"]+"\n"
        elif fjson["type"]=='d':
            if fjson["name"]!="." and fjson["name"]!="..":
                newloc=fjson["location"]
                fp4=open(filepath+str(newloc),"r").read()
                dirinode=json.loads(fp4)
                sizechecker(dirinode)             
                  
filerp=open(filepath+"0","r").read()
superblock=json.loads(filerp)
deviceid=superblock["devId"]
creationtime=superblock["creationTime"]
mounted=superblock["mounted"]
freestart=superblock["freeStart"]
freeend=superblock["freeEnd"]
root=superblock["root"]
maxblocks=superblock["maxBlocks"]

# Checking the device id to be equal to 20 else exiting the function
if(deviceid==20):
    print "\nRight value of devId in superblock\n"

# Checking and updating the time in the superblock if it is in future
    presenttime=int(time.time())
    timestring="time"
    for key,value in superblock.iteritems():
        if timestring.lower() in key.lower():
            if(value>presenttime):
                print "Error: Wrong "+key+" in superblock\n"
                superblock[key]=presenttime
                filewp=open(filepath+"0","w")
                json.dump(superblock,filewp,indent=4)
                filewp.close()
                print key+" updated in superblock\n"
            else:
                print "Right value of "+key+" in superblock\n"
    filerootp=open(filepath+str(root),"r").read()
    rootinode=json.loads(filerootp)

# Calling function in order to check and update the time for all the directories and files starting from root directory

    timechecker(rootinode,presenttime,timestring,root,"root")    
    count=0
    countdotdirs=0;
    flag1=0
    flag2=0
    for nestedjson in rootinode["filename_to_inode_dict"]:
        if nestedjson["type"]=='d':
            if nestedjson["name"] in "." or nestedjson["name"] in ".." :
                if nestedjson["name"] in ".":
                    flag1=1;
                if nestedjson["name"] in "..":
                    flag2=1
                if nestedjson["location"] != root:
                    print "Error: Wrong location of "+nestedjson["name"]+" directory in root\n"
                    rootinode["filename_to_inode_dict"][count]["location"]=root
                    filewp=open(filepath+str(root),"w")
                    json.dump(rootinode,filewp,indent=4)
                    filewp.close()
                    print "location updated for "+nestedjson["name"]+" in root\n"
                else:
                    print "Right location of "+nestedjson["name"]+" directory in root\n" 
                count=count+1
                continue
            else:
                loc=nestedjson["location"]
                filesubp=open(filepath+str(loc),"r").read()
                subinode=json.loads(filesubp)
                dotdirchecker(root,loc,nestedjson["name"],subinode)    
        count=count+1
    if flag1==0:
        rootinode["filename_to_inode_dict"].append({"type":'d',"name":".","location":str(root)})
        print "Error: Missing . in root inode\n"
    if flag2==0:
        rootinode["filename_to_inode_dict"].append({"type":'d',"name":"..","location":str(root)})
        print "Error: Missing .. in root inode\n"
    filewp=open(filepath+str(root),"w")
    json.dump(rootinode,filewp,indent=4)
    filewp.close()
    if flag1!=1 and flag2==1:
        print "Added . in root inode\n"
    elif flag1==1 and flag2!=1:
        print "Added .. in root inode\n"
    elif flag1!=1 and flag2!=1:
        print "Added . and .. in root inode\n"
     
    numlist=range(0,maxblocks)
    perblock=400
    flagblock=0;
    freelist=[]
# Creating a free block list of the blocks mentioned in the File system 

    for counter in range(freestart,freeend+1):
        f=open(filepath+str(counter),"r").read()
        arr=ast.literal_eval(f)
        freelist=freelist+arr

# Comparing the actual free block list with the ones present in the File system and also making sure that their are no files or directories stored on items listed in the free blocks
        
    for x in numlist:
       if not os.path.exists(filepath+str(x)):
           y=int(math.floor(x/float(perblock)))
           if x not in freelist:
               print "Error: Block "+str(x)+" does not exist in the freeblock list\n"
               newloc=y+freestart
               f=open(filepath+str(newloc),"r").read()
               arr1=ast.literal_eval(f)
               arr1.append(x)
               g=open(filepath+str(newloc),"w")
               g.write(str(arr1))
               g.close()
               print str(x)+" added to the free block list in fusedata."+str(newloc)+"\n"
               flagblock=1
       else:
           if x in freelist:
               print "Error: Block "+str(x)+" exists in the freeblock list although it is not a freeblock\n"
               y=int(math.floor(x/float(perblock)))
               newloc=y+freestart
               f=open(filepath+str(newloc),"r").read()
               arr1=ast.literal_eval(f)
               arr1.remove(x)
               g=open(filepath+str(newloc),"w")
               g.write(str(arr1))
               g.close()
               print str(x)+" removed from the free block list in fusedata."+str(newloc)+"\n"
    if flagblock==0:
        print "All the freeblocks already exist\n"
    arraychecker(rootinode)
    sizechecker(rootinode)
else:
    print "\nDevice ID is wrong! Exiting...\n"
    sys.exit()


