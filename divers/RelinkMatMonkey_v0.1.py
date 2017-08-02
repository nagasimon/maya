import maya.cmds as cmds

matArray = []


##### FUNCTIONS --------------
def shaderFromObject(source):
    shadingEngineInput = cmds.listConnections(source, type='shadingEngine')
    mat = ''
    for connection in shadingEngineInput:
        shadingInput = cmds.connectionInfo(connection + '.surfaceShader', sfd=1)
        splittedSource = shadingInput.split('.')
        mat = (splittedSource[0])
    return mat


def loadShaderList():
    sel = cmds.ls(sl=1)
    sel = cmds.listRelatives(sel, allDescendents=True)
    selRel = cmds.listRelatives(sel, shapes=True, allDescendents=True)
    matArray = list()
    for i in selRel:
        objI = []
        objI.append(i)
        mat = shaderFromObject(i)
        objI.append(mat)
        matArray.append(objI)
    print matArray
    return matArray


def applyMatList(matList):
    unfoundObject = []
    sel = cmds.ls(sl=1)
    sel = cmds.listRelatives(sel, allDescendents=True)
    print 'Selection input:'
    print sel
    selRel = cmds.listRelatives(sel, shapes=True, allDescendents=True)
    print 'Selection input extended:'
    print selRel
    print matList
    for i in selRel:
        iSplit = i.split(':')
        iSplit = iSplit[-1]
        match = False
        for u in matList:
            if str(u[0]) == iSplit:
                match == True
                print ('Corresponding object found for ' + str(i))
                matSG = cmds.listConnections(u[0], type='shadingEngine')
                matSG = matSG[0]
                cmds.select(i)
                cmds.sets(e=True, forceElement=matSG)
        if match == False:
            print ('No corresponding object found for ' + str(i))
            unfoundObject.append(i)
    print'------------------------'
    print ('FollowingObjects were skipped:')
    print unfoundObject
    print'------------------------'
    cmds.select(unfoundObject, replace=True)


#### Interface Functions -----------
"""
# ---- UiStartingPoint
"""

windowID = 'RelinkMatMonkey'

if cmds.window(windowID, exists=True):
    cmds.deleteUI(windowID)

RelinkMatMonkey = cmds.window(windowID, title=windowID, resizeToFitChildren=True, sizeable=True)

cmds.columnLayout(adjustableColumn=True)
cmds.button(label='Get Mat List', command='matArray=loadShaderList()')
cmds.button(label='Apply Mat List', command='applyMatList(matArray)')

cmds.showWindow(windowID)

cmds.showWindow()

cmds.select(unfoundObject, replace=True)