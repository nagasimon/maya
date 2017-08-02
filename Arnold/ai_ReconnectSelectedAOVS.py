import maya.cmds as cmds

AOVS=cmds.ls(sl=1)
aiAovInput='defaultArnoldRenderOptions'

def relinkAOV(aovs):
    for aovI in aovs:
        try:
            (cmds.connectAttr(aovI+'.message',aiAovInput+'.aovList.',nextAvailable=True))
        except:
            print(str(aovI)+' already connected')
            
def deactivateAllAOV(aovs):
    #aovList=cmds.listConnections(aiAovInput+'.aovList.')
    aovList=aovs
    for aovI in aovList:
        try:
            cmds.setAttr(aovI+'.enabled',0)
        except:
            print (str(aovI)+' already disabled')
    print aovList
    
relinkAOV(AOVS)
deactivateAllAOV()