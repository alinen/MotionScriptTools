import sys
MBHelperPath = 'C:\\Users\\alinen\\AppData\\Local\\Autodesk\\MB2011\\config\\Python'
if MBHelperPath not in sys.path:
    sys.path.append('C:\\Users\\alinen\\AppData\\Local\\Autodesk\\MB2011\\config\\Python')

from pyfbsdk import *
from pyfbsdk_additions import *

region1 = FBLabel()
editOffset = FBEditNumber()
buttonAction = FBButton()

def PopulateTool(t):
    #populate regions here

    x = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(80,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(25,FBAttachType.kFBAttachNone,"")
    t.AddRegion("region1","region1", x, y, w, h)

    t.SetControl("region1", region1)
    region1.Visible = True
    region1.ReadOnly = False
    region1.Enabled = True
    region1.Hint = ""
    region1.Caption = "Target Height"
    region1.Style = FBTextStyle.kFBTextStyleNone
    region1.Justify = FBTextJustify.kFBTextJustifyLeft
    region1.WordWrap = True
    
    x = FBAddRegionParam(100,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(80,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(25,FBAttachType.kFBAttachNone,"")
    t.AddRegion("editOffset","editOffset", x, y, w, h)

    t.SetControl("editOffset", editOffset)
    editOffset.Visible = True
    editOffset.ReadOnly = False
    editOffset.Enabled = True
    editOffset.Hint = ""
    editOffset.Value = 0.000000
    editOffset.Min = -9999.000000
    editOffset.Max = 9999.000000
    editOffset.Precision = 10.400000
    editOffset.LargeStep = 5.000000
    editOffset.SmallStep = 1.000000
    
    x = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(60,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(110,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(30,FBAttachType.kFBAttachNone,"")
    t.AddRegion("buttonAction","buttonAction", x, y, w, h)

    t.SetControl("buttonAction", buttonAction)
    buttonAction.Visible = True
    buttonAction.ReadOnly = False
    buttonAction.Enabled = True
    buttonAction.Hint = ""
    buttonAction.Caption = "Do it!"
    buttonAction.State = 0
    buttonAction.Style = FBButtonStyle.kFBPushButton
    buttonAction.Justify = FBTextJustify.kFBTextJustifyLeft
    buttonAction.Look = FBButtonLook.kFBLookNormal
    buttonAction.OnClick.Add(ButtonActionEvent)
    
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

def ToesToFloor(nodeName):
    model = FBFindModelByName( nodeName )
    ycurve = findAnimationNode( 'Lcl Translation/Y', model.AnimationNode ).FCurve
    
    lowest = 99999999.0
    for lKey in ycurve.Keys:
        lowest = min(lowest, lKey.Value)
    
    offset = editOffset.Value-lowest # translating to zero
    for lKey in ycurve.Keys:
        lKey.Value = lKey.Value + offset

def ButtonActionEvent(control, event):    
    lSystem = FBSystem()
    for lTakeIdx in range( len( lSystem.Scene.Takes )): # Go through each take
        print "Processing", lSystem.Scene.Takes[lTakeIdx].Name
        lSystem.CurrentTake = lSystem.Scene.Takes[lTakeIdx] # Change take

        lStartFrame = lSystem.CurrentTake.LocalTimeSpan.GetStart().GetFrame(True)
        lEndFrame = lSystem.CurrentTake.LocalTimeSpan.GetStop().GetFrame(True)
        print "Start/stop of current take is ", lStartFrame, lEndFrame
        ToesToFloor('RightFootEffector')
        ToesToFloor('LeftFootEffector')

    del( lSystem )

def CreateTool():
    t = CreateUniqueTool("Toes to floor (AlineN)")
    t.StartSizeX = 325
    t.StartSizeY = 200
    PopulateTool(t)
    ShowTool(t)  
  
CreateTool()


