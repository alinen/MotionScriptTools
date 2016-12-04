## Editing and annotating the feet with Motion Builder scripts

No matter how clean you try to make your C3D data and no matter carefully you try to fit that C3D marker data to a bone hierarchy which matches the capture subject, there are always artifacts that need fixing when you retarget the resulting motion to a character.

And for me at least, fixing and annotating the feet is quite the pain, but I’ve made some recent improvements to my workflow which I wish to share.

First, I’ve started using Motion Builder’s scripting interface for editing and querying FCurves directly (1). It’s fantastic, but some functionality didn’t work until I updated my python path to include the directory to the file pyfbsdk_additions.py

sys.path.append(‘C:\\Users\\alinen\\AppData\\Local\\Autodesk\\MB2011\\config\\Python’)

At neill3d.com and http://awforsythe.com/tutorials/pyfbsdk-5, there are good resources and tutorials for getting used to MoBu’s scripting APIs. But for my purposes, the best reference and tool was neill3d’s lovely and useful StayOnFloor script.

StayOnFloor is written for MoBu 2013 and I have MoBu 2011, so I had to make a few small edits to get the script to work, namely,

- Change GetFrame() to GetFrame(True). Otherwise, I had problems where the frames were not set correctly.
- Change FBCreateUniqueTool to CreateUniqueTool

I also often need to normalize the character’s ground contacts so that they are always at floor height. A simple approach is to find the minimum of the Y curve of each foot effector and then offset the curve so that the lowest point is at the target height. The script ToesToFloor.py will normalize the foot heights at contact for every take in the scene. If you run this after running StayOnFloor, most of the ground contact points will be perfect. Also, make sure that you’ve plotted the animation curves to a control rig and that the BaseAnimation layer is selected first.

 def ToesToFloor(nodeName):
    model = FBFindModelByName( nodeName )
    ycurve = findAnimationNode( 'Lcl Translation/Y', model.AnimationNode ).FCurve

    lowest = 99999999.0
    for lKey in ycurve.Keys:
        lowest = min(lowest, lKey.Value)

        offset = 0-lowest # translating to zero, could use user-specified value
        for lKey in ycurve.Keys:
            lKey.Value = lKey.Value + offset

 ToesToFloor('LeftFootEffector')
 ToesToFloor('RightFootEffector')


And similarly, the script ExportContacts.py will export annotations which indicate when foot contacts occur. The approach simply samples the curves for each foot and keeps track of the frames where they are zero.

    contacts = []
    samplingRate = 1.0/fps
    startframe = (int) (fps*(startms/1000.0)+0.5)
    for frame in range(startframe, startframe+numframes+1):
        t = (int) (frame*samplingRate*1000.0)
        time = FBTime(0,0,0,0)
        time.SetMilliSeconds(t)
        vleft = yleft.Evaluate(time)
        vright = yright.Evaluate(time)
        contacts.append((frame, vleft <= 0, vright <= 0))
        frame = frame + 1

    # Now save the result
    dir = "c:/temp/"
    filename = dir + lSystem.CurrentTake.Name + ".ann"
    file = open(filename, "w")
    lastcontact = contacts[0]
    for contact in contacts:
        if lastcontact[1] != contact[1] or lastcontact[2] != contact[2]: 
           str = ""
           if lastcontact[1]: str = str + "ltoesSite"
           if lastcontact[2]: str = str + " rtoesSite"
           file.writelines("%d %d\n%s\n\n"%(lastcontact[0], contact[0], str))
           lastcontact = contact

    str = ""
    if lastcontact[1]: str = str + "ltoesSite"
    if lastcontact[2]: str = str + " rtoesSite"
    file.writelines("%d %d\n%s\n\n"%(lastcontact[0], contact[0], str))
    lastcontact = contact
