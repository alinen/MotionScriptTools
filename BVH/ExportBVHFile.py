# ExportBVHFile.py, Aline Normoyle 2013
# Defines the Maya fucntion: exportBVHPose()
# To load, drag n drop this file into Maya, or cut and paste into the Python script window
# To run, select the root joint and then run exportBVHPose()
# The current time bar range will be exported to the given file
# The script exports 120 FPS motion (assumes Maya timebar is at 30 FPS (NTSC))

import string
import maya.cmds as cmds
import maya.OpenMaya as OM

Rad2Deg = 57.295779513082320876798154814105
Deg2Rad = 0.017453292519943295769236907684886

rooStr2Int = {'xyz':0, 'yzx':1, 'zxy':2, 'xzy':3, 'yxz':4, 'zyx':5}
rooInt2Str = {0:'xyz', 1:'yzx', 2:'zxy', 3:'xzy', 4:'yxz', 5:'zyx'}


def euler2mat(_euler, _roo, degrees = True):        
        roo = _roo.lower()

        if degrees:
            rx = _euler[0] * Deg2Rad
            ry = _euler[1] * Deg2Rad
            rz = _euler[2] * Deg2Rad
        else:
            rx = _euler[0] 
            ry = _euler[1] 
            rz = _euler[2] 

	euler = OM.MEulerRotation(rx,ry,rz,rooStr2Int[roo]) 
        return euler.asMatrix()

def mat2euler(_m, _roo, degrees = True):
        roo = _roo.lower()

        m = OM.MTransformationMatrix(_m) # MMAtrix to MTransformationMatrix
        euler = m.eulerRotation()

	euler = euler.reorder(rooStr2Int[roo])
        if degrees: euler = euler * Rad2Deg
        return [euler[0], euler[1], euler[2]]

class BVHExporter:

    def __init__(self):
        self.frameData = []
        self.dataCount = 0
        self.scale = [1.0, 1.0, 1.0]


    def writeJoint(self, fileid, sjoint, indent):
        parents = cmds.listRelatives(sjoint, allParents=True) 

        translate = []
        euler = []
        if parents is not None:
           translate = cmds.xform(sjoint, q=True, translation=True)
           euler = cmds.xform(sjoint, q=True, rotation=True)

           x = self.scale[0] * translate[0] 
           y = self.scale[1] * translate[1] 
           z = self.scale[2] * translate[2] 
           line1 = "%sOFFSET %.4f %.4f %.4f\n"%(indent, x, y, z)
           line2 = "%sCHANNELS 3 "%(indent)
           #print line1
           #print line2
           fileid.writelines(line1)
           fileid.writelines(line2)

        else:
           translate = cmds.xform(sjoint, worldSpace=True, q=True, translation=True)
           euler = cmds.xform(sjoint, worldSpace=True, q=True, rotation=True)

           line1 = "%sOFFSET 0.0 0.0 0.0"%(indent)
           line2 = "%sCHANNELS 6 Xposition Yposition Zposition "%(indent)
           fileid.writelines(line1+"\n")
           fileid.writelines(line2)

           self.frameData.append(translate)
           self.dataCount = self.dataCount + 1

        ro = cmds.xform(sjoint, q=True, roo=True)
        #if ro == "zyx": print "Xrotation Yrotation Zrotation\n"
        #if ro == "yzx": print "Xrotation Zrotation Yrotation\n"
        #if ro == "zxy": print "Yrotation Xrotation Zrotation\n"
        #if ro == "xzy": print "Yrotation Zrotation Xrotation\n"
        #if ro == "yxz": print "Zrotation Xrotation Yrotation\n"
        #if ro == "xyz": print "Zrotation Yrotation Xrotation\n"

        if ro == "zyx": fileid.writelines ("Xrotation Yrotation Zrotation\n")
        if ro == "yzx": fileid.writelines ("Xrotation Zrotation Yrotation\n")
        if ro == "zxy": fileid.writelines ("Yrotation Xrotation Zrotation\n")
        if ro == "xzy": fileid.writelines ("Yrotation Zrotation Xrotation\n")
        if ro == "yxz": fileid.writelines ("Zrotation Xrotation Yrotation\n")
        if ro == "xyz": fileid.writelines ("Zrotation Yrotation Xrotation\n") 

        # Apply joint orientation as well
        jroo = cmds.joint(sjoint, q=True, roo=True)
        jeuler = cmds.joint(sjoint, q=True, o=True)
        jmat = euler2mat(jeuler, jroo, True)
        mat = euler2mat(euler, ro, True)
        newmat = mat * jmat
        neweuler = mat2euler(newmat, ro, True)

        if ro == "zyx": self.frameData.append([neweuler[0], neweuler[1], neweuler[2]])
        if ro == "yzx": self.frameData.append([neweuler[0], neweuler[2], neweuler[1]])
        if ro == "zxy": self.frameData.append([neweuler[1], neweuler[0], neweuler[2]])
        if ro == "xzy": self.frameData.append([neweuler[1], neweuler[2], neweuler[0]])
        if ro == "yxz": self.frameData.append([neweuler[2], neweuler[0], neweuler[1]])
        if ro == "xyz": self.frameData.append([neweuler[2], neweuler[1], neweuler[0]])
  
        self.dataCount =  self.dataCount + 1

    def getJoint(self, sjoint):
        parents = cmds.listRelatives(sjoint, allParents=True) 

        translate = []
        euler = []
        if parents is not None:
           translate = cmds.xform(sjoint, q=True, translation=True, objectSpace=True)
           euler = cmds.xform(sjoint, q=True, rotation=True, objectSpace=True)

           x = self.scale[0] * translate[0] 
           y = self.scale[1] * translate[1] 
           z = self.scale[2] * translate[2] 

        else:
           translate = cmds.xform(sjoint, worldSpace=True, q=True, translation=True)
           euler = cmds.xform(sjoint, worldSpace=True, q=True, rotation=True)

           self.frameData.append(translate)
           self.dataCount = self.dataCount + 1

        ro = cmds.xform(sjoint, q=True, roo=True)

        # Apply joint orientation as well	
        jroo = cmds.joint(sjoint, q=True, roo=True)
        jeuler = cmds.joint(sjoint, q=True, o=True)
        jmat = euler2mat(jeuler, jroo, True)
        mat = euler2mat(euler, ro, True)
        newmat = mat * jmat
        neweuler = mat2euler(newmat, ro, True)
	
        if ro == "zyx": self.frameData.append([neweuler[0], neweuler[1], neweuler[2]])
        if ro == "yzx": self.frameData.append([neweuler[0], neweuler[2], neweuler[1]])
        if ro == "zxy": self.frameData.append([neweuler[1], neweuler[0], neweuler[2]])
        if ro == "xzy": self.frameData.append([neweuler[1], neweuler[2], neweuler[0]])
        if ro == "yxz": self.frameData.append([neweuler[2], neweuler[0], neweuler[1]])
        if ro == "xyz": self.frameData.append([neweuler[2], neweuler[1], neweuler[0]])
  
        self.dataCount =  self.dataCount + 1

    def exportJoint(self, fileid, root, indent):
        jointName = string.split(root, '|')[-1]
        line1 = "%sJOINT %s"%(indent, jointName)
        line2 = "%s{"%(indent)
        #print line1
        #print line2
        fileid.writelines(line1+"\n")
        fileid.writelines(line2+"\n")

        self.writeJoint(fileid, root, indent + "\t");

        children = cmds.listRelatives(root, children=True, type='joint', fullPath=True) 
        if children is not None:
            for eachChild in children:
                 self.exportJoint(fileid, eachChild, indent + "\t")

        line2 = "%s}"%(indent)
        fileid.writelines(line2+"\n")

    def getJointData(self, root):
        self.getJoint(root)

        children = cmds.listRelatives(root, children=True, type='joint', fullPath=True) 
        if children is not None:
            for eachChild in children:
                 self.getJointData(eachChild)

    def exportBindPose(self, fileid):

        root = cmds.ls(sl=True, type='joint')
        print root
        if root is None or len(root) == 0:
           print "ERROR: Please select the root joint\n"
           return
  
        self.dataCount = 0
        self.frameData = []
        self.scale = cmds.xform(root, q=True, scale=True)

        print "HIERARCHY"
        fileid.writelines("HIERARCHY\n")
        self.exportJoint(fileid, root[0], "")
        print "\n"
        fileid.writelines("\n")
        print "MOTION"
        print "Frames: 1"
        print "Frame Time: 0.0"
       
        fileid.writelines("MOTION\n")
        fileid.writelines("Frames: 1\n")
        fileid.writelines("Frame Time: 0.033333\n")

        for each in self.frameData:
            print "%.4f %.4f %.4f "%(each[0], each[1], each[2])
            fileid.writelines("%.4f %.4f %.4f "%(each[0], each[1], each[2]))

    def exportAllPoses(self, fileid):

        root = cmds.ls(sl=True, type='joint')
        print root
        if root is None or len(root) == 0:
           print "ERROR: Please select the root joint\n"
           return
  
        startFrame = cmds.playbackOptions(minTime=True, query=True)
        endFrame = cmds.playbackOptions(maxTime=True, query=True)
        cmds.currentTime(startFrame, edit=True)
        print "Exporting", startFrame, "to", endFrame

        self.dataCount = 0
        self.frameData = []
        self.scale = cmds.xform(root, q=True, scale=True)

        fileid.writelines("HIERARCHY\n")
        self.exportJoint(fileid, root[0], "")
        fileid.writelines("\n")
       
        numFrames = 4*(endFrame - startFrame + 1) # Assumes 120 fps, upsamples by 4, make sure Maya sample rate is 30 fps

        fileid.writelines("MOTION\n")
        fileid.writelines("Frames: %d\n"%(numFrames))
        fileid.writelines("Frame Time: 0.00833333\n") # Assumes 120 fps

        for each in self.frameData:
            #print "%.4f %.4f %.4f "%(each[0], each[1], each[2])
            fileid.writelines("%.4f %.4f %.4f "%(each[0], each[1], each[2]))        

        dt = 0.25
        for i in range(1, numFrames):
            cmds.currentTime(startFrame + i*dt, edit=True)
            self.frameData = []
            self.getJointData(root[0])
            fileid.writelines("\n")
            for each in self.frameData:
                fileid.writelines("%.4f %.4f %.4f "%(each[0], each[1], each[2]))            

    def exportPose(self, filename):
        fileid = open(filename, "w")
        self.exportBindPose(fileid)
        fileid.close()

    def exportMotion(self, filename):
        fileid = open(filename, "w")
        self.exportAllPoses(fileid)
        fileid.close()

def exportBVHPose():
    filenames = cmds.fileDialog2(fileMode=0, caption="Export BVH Pose")

    num = len(filenames)
    if num > 0:
      fileName = filenames[0]
      print fileName
      exporter = BVHExporter()
      exporter.exportPose(fileName)

def exportBVHFile():
    filenames = cmds.fileDialog2(fileMode=0, caption="Export BVH File")

    num = len(filenames)
    if num > 0:
      fileName = filenames[0]
      print fileName
      exporter = BVHExporter()
      exporter.exportMotion(fileName)

exportBVHFile()

