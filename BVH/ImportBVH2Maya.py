# ImportBVH2Maya.py, Aline Normoyle 2013
# Defines the Maya fucntion: loadBVHFile()
# If a skeleton already exists in the scene, only edits keyframes; otherwise, it creates the skeleton too
# To run, drag n drop this file into Maya, or cut and paste into the Python script window
# NOTE: This script does not work with a pre-rotation (needs updating)

import string
import maya.cmds as cmds
import pymel.core.datatypes as dt

class Joint:
    def __init__(self):
        self.offset = []
        self.channels = []
        self.name = ""
        self.children = []
        self.parent = None
        self.id = 0
        self.channelvals = []
        self.rotOrder = "xyz"

class BVHReader:

    def __init__(self):
        self.clear()

    def clear(self):
        self.joints = []
        self.jointMap = {}
        self.root = None
        self.frames = []
        self.frameRate = 30

    def load(self, filename):
        self.clear()

        file = open(filename)
        lines = file.readlines()
        if "HIERARCHY" not in lines[0]:
           return False

        parent = None
        current = None
        motion = False

        for line in lines[1:len(lines)]:
            tokens = string.split(line)
            if len(tokens) == 0: # Empty line
                continue

            if tokens[0] in ["ROOT", "JOINT", "End"]:

               if current is not None:
                  parent = current

               current = Joint()
               current.name = tokens[1]

               current.id = len(self.joints)
               if current.id == 0:
                   self.root = current

               current.parent = parent
               if parent is not None:
                   current.parent.children.append(current)

               self.joints.append(current)
               self.jointMap[current.name] = current

            elif "OFFSET" in tokens[0]:
                 offset = []
                 for i in range(1,len(tokens)):
                     offset.append(float(tokens[i]))
                 current.offset = offset

            elif "CHANNELS" in tokens[0]:
                 current.channels = tokens[2:len(tokens)]
                 for i in range(len(current.channels)):
                     current.channelvals.append(0)

                 str = ""
                 chans = list(current.channels)
                 chans.reverse()
                 for channel in chans:
                     if channel == "Xrotation": str += "x"
                     elif channel == "Yrotation": str += "y"
                     elif channel == "Zrotation": str += "z"
                 current.rotOrder = str

            elif "{" in tokens[0]:
                 pass

            elif "}" in tokens[0]:
                 current = current.parent
                 if current: 
                     parent = current.parent

            elif "MOTION" in tokens[0]:
                 motion = True

            elif "Frames:" in tokens[0]:
                 pass 

            elif "Frame" in tokens[0]:
                 self.frameRate = 1.0/float(tokens[2])

            elif motion: # Read frame data
                 vals = []
                 for token in tokens:
                     vals.append(float(token))
                 self.frames.append(vals)

    def printHierarchyJoint(self, joint, indent = ''):
        print indent, joint.name
        for child in joint.children:
            self.printHierarchyJoint(child, indent+"  ")

    def printHierarchy(self):
        self.printHierarchyJoint(self.root)

    def numFrames(self):
        return len(self.frames)

    def applyFrame(self, frameNum):
        idx = 0
        for joint in self.joints:
            for i in range(len(joint.channels)): 
                v = self.frames[frameNum][idx]
                joint.channelvals[i] = v
                idx = idx + 1

    def jointPos(self, joint):
        pos = [0, 0, 0]
        try:
           pos[0] = joint.channelvals[joint.channels.index("Xposition")]
           pos[1] = joint.channelvals[joint.channels.index("Yposition")]
           pos[2] = joint.channelvals[joint.channels.index("Zposition")]
        except: pass
        return pos

    def joint(self, jointName):
        joint = self.jointMap[jointName]
        return joint

    def jointRot(self, joint):
        rot = [0, 0, 0]
        try:
           rot[0] = joint.channelvals[joint.channels.index("Xrotation")]
           rot[1] = joint.channelvals[joint.channels.index("Yrotation")]
           rot[2] = joint.channelvals[joint.channels.index("Zrotation")]
        except: pass
        return rot

    def jointRotRoo(self, joint, roo):
        rot = [0, 0, 0]
        try:
           rot[0] = joint.channelvals[joint.channels.index("Xrotation")]
           rot[1] = joint.channelvals[joint.channels.index("Yrotation")]
           rot[2] = joint.channelvals[joint.channels.index("Zrotation")]

           euler = dt.EulerRotation()
           euler.setValue(dt.Vector(rot) * Deg2Rad, joint.rotOrder.upper())
           euler.reorderIt(roo.upper())

           rot[0] = euler[0] * Rad2Deg
           rot[1] = euler[1] * Rad2Deg
           rot[2] = euler[2] * Rad2Deg
        except: pass
        return rot    
    
def createMayaJoint(joint):
    offset = (joint.offset[0], joint.offset[1], joint.offset[2])
    if joint.parent:
        cmds.select(joint.parent.name)
    name = cmds.joint(name=joint.name, p=offset, relative=True, roo=joint.rotOrder)
    joint.name = cmds.ls(name, long=True)[0]
    #print "CREATE", joint.name

    for child in joint.children:
        createMayaJoint(child)

def createSkeleton(reader):
    createMayaJoint(reader.root)

def setMayaKeyframe(reader, frameNum):
    cmds.currentTime(frameNum+1)
    reader.applyFrame(frameNum)
    for joint in reader.joints:
        if len(joint.channels) == 0: continue
        if not cmds.objExists(joint.name): continue

        cmds.select(joint.name)
        if joint == reader.root:
           scale = cmds.getAttr(joint.name+'.scale')     
           (sx,sy,sz) = scale[0]          
           pos = reader.jointPos(joint)
           cmds.xform(translation=(sx*pos[0],sy*pos[1],sz*pos[2]), absolute=True)
        rot = reader.jointRot(joint)
        # TODO: Be mindful of target joint rotation
        cmds.xform(roo=joint.rotOrder)
        cmds.xform(rotation=(rot[0],rot[1],rot[2]), objectSpace=True)
        cmds.joint(o=(0,0,0), e=True)
    cmds.select(reader.root.name, hierarchy=True)
    cmds.setKeyframe(at='translate')
    cmds.setKeyframe(at='rotate')
    
def setMayaKeyframes(reader):
    for i in range(reader.numFrames()):
        setMayaKeyframe(reader, i)

def loadBVHFile(): # TODO: Support creating multiple skeletons in the scene
    filenames = cmds.fileDialog2(fileMode=1, caption="Import BVH")
    filename = filenames[0]
    reader = BVHReader()    
    reader.load(filename)
    reader.printHierarchy()

    if not cmds.objExists(reader.root.name):
        createSkeleton(reader)
    setMayaKeyframes(reader)

loadBVHFile()
