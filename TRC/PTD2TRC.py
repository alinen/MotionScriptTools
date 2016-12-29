import os, string

def ConvertPTD2TRC(filename):
    ifile = open(filename, "r")
    newfilename = filename[0:-4]+".trc"

    ofile = open(newfilename, "w")
    numframes = int(ifile.readline())
    print "Reading", filename, "#lines", numframes
    ofile.writelines("PathFileType\t4\t(X/Y/Z)\t%s\n"%newfilename)
    ofile.writelines("DataRate\tCameraRate\tNumFrames\tNumMarkers\tUnits\tOrigDataRate\tOrigDataStartFrame\tOrigNumFrames\n")
    ofile.writelines("60\t60\t%d\t15\tcm\t60\t1\t%d\n"%(numframes, numframes))
    ofile.writelines("Frame#\tTime\tP1\t\t\tP2\t\t\tP3\t\t\tp4\t\t\tp5\t\t\tp6\t\t\tp7\t\t\tp8\t\t\tp9\t\t\tP10\t\t\tP11\t\t\tP12\t\t\tP13\t\t\tP14\t\t\tP15\t\t\n")
    ofile.writelines("\t\tX1\tY1\tZ1\tX2\tY2\tZ2\tX3\tY3\tZ3\tX4\tY4\tZ4\tX5\tY5\tZ5\tX6\tY6\tZ6\tX7\tY7\tZ7\tX8\tY8\tZ8\tX9\tY9\tZ9\tX10\tY10\tZ10\tX11\tY11\tZ11\tX12\tY12\tZ12\tX13\tY13\tZ13\tX14\tY14\tZ14\tX15\tY15\tZ15\n")

    count = 1
    time = 0
    dt = 1.0/60.0
    for inline in ifile:
        line = "%d\t%f\t"%(count, time)        
        tokens = string.split(inline)
        for i in range(0,len(tokens),3):
            xtoken = float(tokens[i])
            ytoken = float(tokens[i+1])
            ztoken = float(tokens[i+2])
            x = xtoken * 2.75
            y = ztoken * 2.75
            z = -ytoken * 2.75
            line += "%f\t%f\t%f\t"%(x,y,z)
        line += "\n"
        ofile.writelines(line)
        #print line
        time = time + dt
        count = count + 1

def ProcessDir(dirname):
    for root, dir, files in os.walk(dirname):
        for file in files:
            if file[-4:len(file)] == ".ptd":
               ConvertPTD2TRC(os.path.join(root,file))

def unzipAll(dirname):
    for root, dir, files in os.walk(dirname):
        print root
        for file in files:
            if file[-4:len(file)] == ".ptd":
               print file
    
#ConvertPTD2TRC("emm_pt\emm_knock_an_2_fin.ptd")
ProcessDir(".")
