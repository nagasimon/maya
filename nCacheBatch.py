# SetUp the batch parameters for caching fluids of the scene 
# Simon Legrand - simon.legrand.gib@gmail.com
# 2017/02/24

import maya.cmds as cmds


#generate the fluids groups
visibleFluids=cmds.ls(sl=0,type='fluidShape',visible=True)
if cmds.objExists('fluidSet'):
	#print "fluidSet already exist"
	cmds.delete('fluidSet')

cmds.sets(visibleFluids,n='fluidSet')

#set up the batch options
melOut="select fluidSet;"+ ' doCreateFluidCache 5 { "2", "1", "20", "OneFile", "1", "","0","","0", "add", "0", "1", "1", "0", "1", "mcx", "1", "1", "1", "1", "1", "1", "1" } ;'
cmds.setAttr('defaultRenderGlobals.preMel',melOut,type='string')
cmds.setAttr('defaultResolution.aspectLock',0)
cmds.setAttr('defaultResolution.width',2)
cmds.setAttr('defaultResolution.height',2)

#reactivate all fluids evaluation
for i in visibleFluids:
	cmds.setAttr(i+'.disableInteractiveEval',0)

#set the timelime to the frame 01
cmds.currentTime(1)