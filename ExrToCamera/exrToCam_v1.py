##
## Pierre Lelievre - 06/2012
## Fabrice Macagno
## Inspiration Johannes Hezer, Ivan Busquet, Michael Garret and Frank Rueter
## Version 0.6
##
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
##
## This script sets a new camera node from metadata of an exr file (read node).
## Thanks to exr/worldToCamera and exr/worldToNDC, it sets position, orientation
## and the horizontal and vertical apertures relatively to the focal (set by default to 35mm).
##
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
##


import nuke
#import math


def listToMatrix(list):

    m = nuke.math.Matrix4()

    try: 
        for i in range(16):
            m[i] = list[i]
    except:
        raise
    return m


def mayaToNukeMatrixConv(m):

    flipZ=nuke.math.Matrix4()
    flipZ.makeIdentity()
    flipZ.scale(1,1,-1)

    m.transpose()
    m=m*flipZ

    return m


def tryReadNode():

    try:
        n = nuke.selectedNode()
    except:
        nuke.message("Please select a Read Node")
        raise

    if n.Class() != 'Read':
        nuke.message("Please select a Read Node")
        raise

    if n.metadata('input/filereader') != 'exr':
        nuke.message("Please read an EXR File")
        raise

    frame = nuke.frame()
    try:
        listToMatrix(n.metadata('exr/worldToCamera',frame))
        listToMatrix(n.metadata('exr/worldToNDC',frame))
    except:
        nuke.message('Sorry, no valid camera metadata')
        print "Sorry, no valid camera metadata"
        raise

    return n


def exrMetadata(x,index,frame):

    exrCamera = nuke.thisNode()
    exrNode = exrCamera['exrName'].node()
    focal = exrCamera['focal'].getValue()

    if x == 'matrix': 

        m = listToMatrix(exrNode.metadata('exr/worldToCamera',frame))
        m = mayaToNukeMatrixConv(m)
        m = m.inverse()

        return m[index]

    if x == 'haperture':
        worldToCameraMatrix = listToMatrix(exrNode.metadata('exr/worldToCamera',frame))
        worldToCameraMatrix = worldToCameraMatrix.inverse()        
        worldToNDCMatrix = listToMatrix(exrNode.metadata('exr/worldToNDC',frame))
        apertureMatrix = worldToNDCMatrix*worldToCameraMatrix
        haperture = 2*focal/apertureMatrix[0]

        return haperture

    if x == 'vaperture':
        worldToCameraMatrix = listToMatrix(exrNode.metadata('exr/worldToCamera',frame))
        worldToCameraMatrix = worldToCameraMatrix.inverse()        
        worldToNDCMatrix = listToMatrix(exrNode.metadata('exr/worldToNDC',frame))
        apertureMatrix = worldToNDCMatrix*worldToCameraMatrix
        vaperture = 2*focal/apertureMatrix[5]

        return vaperture


def bakeCamera():

    exrCamera = nuke.thisNode()
    exrNode = exrCamera['exrName'].node()
    focal = exrCamera['focal'].getValue()

    exrCamera['matrix'].clearAnimated()
    exrCamera['focal'].clearAnimated()
    exrCamera['haperture'].clearAnimated()
    exrCamera['vaperture'].clearAnimated()

    exrCamera['useMatrix'].setValue(1)

    exrCamera['matrix'].setAnimated()
    exrCamera['focal'].setAnimated()
    exrCamera['haperture'].setAnimated()
    exrCamera['vaperture'].setAnimated()

    for frame in range(int(exrNode["origfirst"].getValue()), 1 + int(exrNode["origlast"].getValue())):

        for i in range(16):
            exrCamera['matrix'].setValue(exrMetadata('matrix',i,frame),i , frame)

        exrCamera['focal'].setValueAt(focal, frame)
        exrCamera['haperture'].setValueAt(exrMetadata('haperture',0,frame), frame)
        exrCamera['vaperture'].setValueAt(exrMetadata('vaperture',0,frame), frame)

    exrCamera.removeKnob(exrCamera.knobs()['exrName'])


def setLink(exrCamera = 0):

    if exrCamera == 0:
        exrCamera = nuke.thisNode()

    ## Read Node validation.

    try:
        exrNode = tryReadNode()
    except:
        return

    ## Read Node reference update.

    if 'exrName' in exrCamera.knobs().keys():
        exrLinkKnob = exrCamera.knobs()['exrName']
        exrLinkKnob.makeLink(exrNode.name(), 'name')
    else:
        exrLinkKnob = nuke.Link_Knob('exrName')
        exrCamera.addKnob(exrLinkKnob)
        exrLinkKnob.setVisible(False)
        exrLinkKnob.makeLink(exrNode.name(), 'name')

    ## Clean Baked Animation

    exrCamera['matrix'].clearAnimated()
    exrCamera['focal'].clearAnimated()
    exrCamera['haperture'].clearAnimated()
    exrCamera['vaperture'].clearAnimated()

    ## Camera update.

    cameraName = 'exrCamera_' + exrNode.name()
    i = 1
    while nuke.toNode(cameraName) in nuke.allNodes():
        cameraName = cameraName + '_%d' % i
        i += 1
    exrCamera.setName(cameraName, uncollide=False)
    exrCamera['focal'].setValue(35.0)

    ## Link Values

    exrCamera['useMatrix'].setValue(1)
    for i in range(16):
        exrCamera['matrix'].setExpression("[python exrToCam.exrMetadata('matrix',%s,nuke.frame())]" %i ,i)
    exrCamera['haperture'].setExpression("[python exrToCam.exrMetadata('haperture',0,nuke.frame())]")
    exrCamera['vaperture'].setExpression("[python exrToCam.exrMetadata('vaperture',0,nuke.frame())]")


def exrToCam():

    ## Read Node validation..

    try:
        exrNode = tryReadNode()
    except:
        return

    ## Camera initialisation.

    exrCamera = nuke.nodes.Camera()

    ## Knobs initialisation.

    tabKnob = nuke.Tab_Knob("exrToCam")
    exrCamera.addKnob(tabKnob)
    
    setLinkKnob = nuke.PyScript_Knob("updateFunction","Change Read Node Reference","setLink()")
    exrCamera.addKnob(setLinkKnob)
    setLinkKnob.setTooltip("This button allows you to change the read node reference.\nYou can also unbake the camera with it.")

    dividerKnob = nuke.Text_Knob("divider","")
    exrCamera.addKnob(dividerKnob)

    bakeKnob = nuke.PyScript_Knob("bakeAnimation","Bake Camera","bakeCamera()")
    exrCamera.addKnob(bakeKnob)
    bakeKnob.setTooltip("This button allows you to bake the following camera parameters (matrix, focal, haperture, vaperture).")

    ## Initial Set Link 

    setLink(exrCamera)

    ## Select the camera node and execute the bake function
    sel = nuke.selectedNode()
    sel.setSelected(False)
    exrCamera.setSelected(True)
    nuke.PyScript_Knob.execute(bakeKnob)

exrToCam()