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

def PrintCurve(nodeName, lStartFrame, lEndFrame):
    #'Lcl Translation/X','Lcl Translation/Y','Lcl Translation/Z', 'Lcl Rotation/X','Lcl Rotation/Y','Lcl Rotation/Z']:
    model = FBFindModelByName( nodeName )
    xcurve = findAnimationNode( 'Lcl Translation/X', model.AnimationNode ).FCurve
    ycurve = findAnimationNode( 'Lcl Translation/Y', model.AnimationNode ).FCurve
    zcurve = findAnimationNode( 'Lcl Translation/Z', model.AnimationNode ).FCurve
    for i in range(lStartFrame, lEndFrame):
        time = FBTime(0,0,0, i )
        value = xcurve.Evaluate(time)
        print i, value
        break

lSystem = FBSystem()
for lTakeIdx in range( len( lSystem.Scene.Takes )): # Go through each take
    print "Processing", lSystem.Scene.Takes[lTakeIdx].Name
    lSystem.CurrentTake = lSystem.Scene.Takes[lTakeIdx] # Change take

    lStartFrame = lSystem.CurrentTake.LocalTimeSpan.GetStart().GetFrame(True)
    lEndFrame = lSystem.CurrentTake.LocalTimeSpan.GetStop().GetFrame(True)
    print "Start/stop of current take is ", lStartFrame, lEndFrame
    PrintCurve('RightFootEffector', lStartFrame, lEndFrame)
    PrintCurve('LeftFootEffector', lStartFrame, lEndFrame)

# Cleanup of local variables.
del( lSystem )


# Get selected models
# lSelectedModels = FBModelList()
# FBGetSelectedModels( lSelectedModels )

#for lComp in FBSystem().Scene.Components:
#    if lComp != None:
#        print lComp.Name, FBFindModelByName(lComp.Name)
#        ltran = lComp.PropertyList.Find ( 'Translation (Lcl)' ).Data
#        if ltran: 
#            print ltran
#        else:
#            print "Can't find value"
