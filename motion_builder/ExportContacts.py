import sys, math
from pyfbsdk import *
from pyfbsdk_additions import *

def findAnimationNode( pName, pNode ):
    lResult = None
    lName = pName.split( '/' )
    for lNode in pNode.Nodes:
        if lNode.Name == lName[0]:
            if len( lName ) > 1:
                lResult = findAnimationNode( pName.replace( '%s/' % lName[0], '' ), lNode )
            else:
                lResult = lNode
    return lResult

def ExportContacts(LeftFoot, RightFoot, fps, lStart, lEnd):
    #'Lcl Translation/X','Lcl Translation/Y','Lcl Translation/Z', 'Lcl Rotation/X','Lcl Rotation/Y','Lcl Rotation/Z']:
    startms = lStart.GetMilliSeconds()
    endms = lEnd.GetMilliSeconds()        
    duration = (endms - startms)/1000.0
    numframes = (int)(duration*fps+0.5)
    print "Duration (s) of current take is ", duration, numframes   
    
    mleft = FBFindModelByName( LeftFoot )
    yleft = findAnimationNode( 'Lcl Translation/Y', mleft.AnimationNode ).FCurve

    mright = FBFindModelByName( RightFoot )
    yright = findAnimationNode( 'Lcl Translation/Y', mright.AnimationNode ).FCurve

    samplingRate = 1.0/fps
    startframe = (int) (fps*(startms/1000.0)+0.5)
    frame = startframe
    contacts = []
    for frame in range(startframe, startframe+numframes+1):
        t = (int) (frame*samplingRate*1000.0)
        time = FBTime(0,0,0,0)        
        time.SetMilliSeconds(t)
        vleft = yleft.Evaluate(time)
        vright = yright.Evaluate(time)
        contacts.append((frame, vleft <= 0, vright <= 0))
        frame = frame + 1
       
    dir = "c:/temp/"
    filename = dir + lSystem.CurrentTake.Name + ".ann"
    file = open(filename, "w")
    lastcontact = contacts[0] 
    for contact in contacts:
        if lastcontact[1] != contact[1] or lastcontact[2] != contact[2]:
            str = ""
            if lastcontact[1]: str = str + "ltoesSite"
            if lastcontact[2]: str = str + " rtoesSite"
            print lastcontact[0], contact[0]
            print str
            print
            file.writelines("%d %d\n%s\n\n"%(lastcontact[0], contact[0], str))
            lastcontact = contact
    
    str = ""
    if lastcontact[1]: str = str + "ltoesSite"
    if lastcontact[2]: str = str + " rtoesSite"
    print lastcontact[0], contacts[-1][0]
    print str
    print
    file.writelines("%d %d\n%s\n\n"%(lastcontact[0], contact[0], str))
    lastcontact = contact
    
fps = 120.0
lSystem = FBSystem()
for lTakeIdx in range( len( lSystem.Scene.Takes )): # Go through each take
    print "Processing", lSystem.Scene.Takes[lTakeIdx].Name
    lSystem.CurrentTake = lSystem.Scene.Takes[lTakeIdx] # Change take

    lStart = lSystem.CurrentTake.LocalTimeSpan.GetStart()
    lEnd = lSystem.CurrentTake.LocalTimeSpan.GetStop()
    ExportContacts('LeftFootEffector', 'RightFootEffector', fps, lStart, lEnd)
    break

# Cleanup of local variables.
del( lSystem )
