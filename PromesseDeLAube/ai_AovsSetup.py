import maya.cmds as cmds
import mtoa.aovs as aovs

#help(aovs)

aovNameFilter=cmds.itemFilter(byName='*AOV*')
aovFilter=cmds.itemFilter(byType='aiAOV')
intersectionFilter = cmds.itemFilter( intersect=(aovNameFilter, aovFilter) )

AOVS = cmds.lsThroughFilter( intersectionFilter )
aiAovInput = 'defaultArnoldRenderOptions'
aovItemListInput=['N',
                  'P',
                  'Z',
                  'motionvector',
                  'direct_diffuse',
                  'direct_specular',
                  'indirect_diffuse',
                  'indirect_specular',
                  'opacity',
                  'refraction',
                  'refraction_opacity',
                  'sss',
                  'volume',
                  'volume_opacity'
                  ]

def relinkAOV(aovs):
    for aovI in aovs:
        try:
            (cmds.connectAttr(aovI + '.message', aiAovInput + '.aovList.', nextAvailable=True))
        except:
            print(str(aovI) + ' already connected')

def deactivateAllAOV(aovs):
    if aovs=='all':
        aovList=cmds.listConnections(aiAovInput+'.aovList.')
    else :
        aovList = aovs
    for aovI in aovList:
        try:
            cmds.setAttr(aovI + '.enabled', 0)
        except:
            print (str(aovI) + ' already disabled')
    print aovList

def createAOVList(aovItemList):
    AOVbibi = aovs.AOVInterface()

    for aov in aovItemList:
        if cmds.objExists('aiAOV_'+str(aov))==False:
            try:
                AOVbibi.addAOV(str(aov))
            except:
                print (str(aovI) + ' already disabled')

try:
    relinkAOV(AOVS)
except:
    print'noAOV to relink'

createAOVList(aovItemListInput)

try:
    deactivateAllAOV('all')
except:
    print'noAOV to disable'
