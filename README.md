# MotionScriptTools
Scripting tools for matlab, motion builder, and maya

BVH/                   // utilities for working with BVH files
BVH/bvh_to_matrix.m    // imports a bvh file to matlab
BVH/matrix_to_bvh.m    // exports a bvh file from matlab (for modifying existing BVH files; 
                       // it does not support creating a new BVH file from scratch)
BVH/ImportBVH2Maya.py  // Import a BVH file to Maya
BVH/ExportBVHFile.py   // Export a BVH file from Maya
BVH/exportBindPose.mel // Export bind pose of skinned model

motion_builder                    // motion builder scripts
motion_builder/ExportContacts.py  // output text files of when end effectors are close to the floor
motion_builder/PrintCurve.py      // output channel curves, such as X,Y,Z translation
motion_builder/ToesToFloor.py     // clamp toes to the floor, cleanup foot sliding
