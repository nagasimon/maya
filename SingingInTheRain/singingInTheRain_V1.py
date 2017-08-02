import maya.cmds as cmds

# Parameters
bakeSteps = 0.5
pointDensity = 100
timeDetailFactor = 100
boxScl = 30

sctBxLocator = 'BoxScatter_v01_boxScatterLocator'
sctNode = 'BoxScatter_v01_scatterShape1'
sctBox = 'BoxScatter_v01_polyCube1'
instancerNode = 'InstancerFromCurve_RandomRotateY_v01_rainInstancer'
curveToPointCloudNode = 'InstancerFromCurve_RandomRotateY_v01_curvesToPointCloud1'
instanceShape = 'RainScatterSample_v01_rainInstanceA'

# Common Variables
nurbsArray = []
camNode = ''
curveSource = ''

#### -------------------------------------------- Functions ------------------------------------------

def setPosRot(obj, posArr, rotArr):
    cmds.setAttr(obj + '.translateX', posArr[0])
    cmds.setAttr(obj + '.translateY', posArr[1])
    cmds.setAttr(obj + '.translateZ', posArr[2])
    cmds.setAttr(obj + '.rotateX', rotArr[0])
    cmds.setAttr(obj + '.rotateY', rotArr[1])
    cmds.setAttr(obj + '.rotateZ', rotArr[2])


def evaluateCamPath():
    nurbsArray = []

    # place at camera location
    startFrame = cmds.playbackOptions(query=True, minTime=True) * timeDetailFactor
    endFrame = cmds.playbackOptions(query=True, maxTime=True) * timeDetailFactor

    for i in range(int(startFrame), int(endFrame), int(bakeSteps * timeDetailFactor)):
        cmds.currentTime(i / timeDetailFactor, edit=True)
        camLocPos = cmds.xform(camNode, query=True, translation=True, worldSpace=True)
        camLocRot = cmds.xform(camNode, query=True, rotation=True, worldSpace=True)
        setPosRot(sctBxLocator, camLocPos, camLocRot)

        cmds.setAttr(sctNode + '.seed', i)
        pointArray = cmds.getAttr(sctNode + '.outPositionPP.')
        try:
            for p in pointArray:
                nurbsArray.append(p)
                # create the curve from the point array and remove the reference
        except:
            print 'No point evaluated'
            cmds.confirmDialog(title='Invalid evaluation',
                               message='No point was evaluated, change the parameter and retry if you dare ...',
                               button=['Ok'],
                               defaultButton='Ok',
                               cancelButton='Ok',
                               dismissString='Ok')
    try:
        curveSource = cmds.curve(name='curveBake', degree=1, p=nurbsArray)
        cmds.file("/uvfx/Projects/Promesse_de_laube/Test/Sequence_202/BoxScatter_v01.ma", removeReference=True)
    except:
        print 'bad ending'


def generateRainRig():
    # import the rain scatter reference
    cmds.file("/uvfx/Projects/Promesse_de_laube/Test/Sequence_202/RainScatterSample_v01.ma",
              rpr="RainScatterSample_v01",
              r=True,
              type="mayaAscii",
              ignoreVersion=True,
              mergeNamespacesOnClash=False,
              options="v=0;p=17;f=0")

    # import the reference for the instancer
    cmds.file("/uvfx/Projects/Promesse_de_laube/Test/Sequence_202/InstancerFromCurve_RandomRotateY_v01.ma",
              rpr="InstancerFromCurve_RandomRotateY_v01",
              r=True,
              type="mayaAscii",
              ignoreVersion=True,
              mergeNamespacesOnClash=False,
              options="v=0;p=17;f=0")

    # connect the references
    cmds.connectAttr('curveBake' + '.local', curveToPointCloudNode + '.inCurves[0]')
    cmds.connectAttr(instanceShape + '.matrix', instancerNode + '.inputHierarchy[0]')

    # setup the animation
    timeConvert = cmds.createNode('timeToUnitConversion')
    cmds.setAttr(instancerNode + '.levelOfDetail', 1)
    cmds.setAttr(timeConvert + '.conversionFactor', -0.0004)
    cmds.connectAttr('time1.outTime', timeConvert + '.input')
    cmds.addAttr(instancerNode, longName='rainSpeed', at='double', dv=100)
    multiplierNode = cmds.createNode('multiplyDivide')
    cmds.connectAttr(timeConvert + '.output', multiplierNode + '.input1.input1X.')
    cmds.connectAttr(multiplierNode + '.outputX', instancerNode + '.ty')
    cmds.connectAttr(instancerNode + '.rainSpeed', multiplierNode + '.input2.input2X.')


### ----------------------------------    UI    ------------------------------------###
#######################################################################################


# Transfer Brightness from B to A
def brightnessCol(A, b):
    import colorsys

    hsvA = colorsys.rgb_to_hsv(A[0], A[1], A[2])
    rgbOut = colorsys.hsv_to_rgb(hsvA[0], hsvA[1], (hsvA[2] + b))
    return rgbOut


# Add b in saturation to A color
def saturationCol(A, b):
    import colorsys

    hsvA = colorsys.rgb_to_hsv(A[0], A[1], A[2])
    rgbOut = colorsys.hsv_to_rgb(hsvA[0], (hsvA[1] + b), hsvA[2])
    return rgbOut


def importBoxScatterRig():
    # import BoxScatter reference
    cmds.file("/uvfx/Projects/Promesse_de_laube/Test/Sequence_202/BoxScatter_v01.ma",
              rpr="BoxScatter_v01",
              r=True,
              type="mayaAscii",
              ignoreVersion=True,
              mergeNamespacesOnClash=False,
              options="v=0;p=17;f=0")


def parameterChange():
    global bakeSteps, boxScl, pointDensity

    bakeSteps = cmds.floatFieldGrp(bakeStepField, query=True, value=True)[0]
    boxScl = cmds.floatFieldGrp(boxScaleField, query=True, value=True)[0]
    pointDensity = int(cmds.floatFieldGrp(pointDensityField, query=True, value=True)[0])

    # Setup the options
    cmds.setAttr(sctNode + '.pointDensity', pointDensity)
    cmds.setAttr(sctBxLocator + '.scaleX', float(boxScl / 3))
    cmds.setAttr(sctBxLocator + '.scaleY', float(boxScl / 3))
    cmds.setAttr(sctBxLocator + '.scaleZ', float(boxScl / 3))


def displayModeInstancer():
    val = cmds.getAttr(instancerNode + '.levelOfDetail')
    if val == 0:
        cmds.setAttr(instancerNode + '.levelOfDetail', 1)
    else:
        cmds.setAttr(instancerNode + '.levelOfDetail', 0)


def importEvalRig(cameraNode):
    importBoxScatterRig()
    camLocPos = cmds.xform(cameraNode, query=True, translation=True, worldSpace=True)
    camLocRot = cmds.xform(cameraNode, query=True, rotation=True, worldSpace=True)
    setPosRot(sctBxLocator, camLocPos, camLocRot)
    parameterChange()


def camFromSelection():
    global camNode
    camNode = cmds.ls(sl=1)
    cmds.textFieldButtonGrp(camField, edit=True, text=str(camNode))

def rainParameterChange():
    cmds.setAttr(instancerNode + '.rainSpeed', cmds.floatFieldGrp(rainSpeedField, query=True, value1=True))


"""
# ---- UiStartingPoint
"""

windowID = 'Singing in the rain'
windowW = 350
colorBase = [0.1, 0.2, 0.4]
contrastVal = 0.2
contrastSatVal = -0.1
colorLevelA = brightnessCol(saturationCol(colorBase, contrastSatVal), contrastVal)
colorLevelB = brightnessCol(saturationCol(colorLevelA, contrastSatVal), contrastVal)
colorLevelC = brightnessCol(saturationCol(colorLevelB, contrastSatVal), contrastVal)

try:
    if cmds.window(SingingInTheRain, exists=True):
        cmds.deleteUI(SingingInTheRain)
except:
    print 'first iteration of Singing in the rain'

SingingInTheRain = cmds.window(windowID, title=windowID, resizeToFitChildren=True, sizeable=True, w=windowW, h=150)

cmds.columnLayout()
cmds.text(label=windowID, w=windowW, h=25, bgc=colorBase)
cmds.text(label='', w=windowW, h=5)
cmds.text(label='Camera Evaluation', w=windowW, h=15, bgc=colorLevelA)
cmds.text(label='', w=windowW, h=5)

camField= cmds.textFieldButtonGrp(label='Camera', text='', buttonLabel='from selection',bc='camFromSelection()', cw3=[60, 160, 50])
cmds.text(label='', w=windowW, h=5)
cmds.button("Import evaluation rig", h=30, w=windowW, c='importEvalRig(camNode)')
cmds.text(label='', w=windowW, h=5)

bakeStepField = cmds.floatFieldGrp(numberOfFields=1, label='Bake steps length', value1=bakeSteps,
                                   cc='parameterChange()', extraLabel='frame')
boxScaleField = cmds.floatFieldGrp(numberOfFields=1, label='Evaluation box scale', value1=boxScl,
                                   cc='parameterChange()', extraLabel='meter')
pointDensityField = cmds.floatFieldGrp(numberOfFields=1, label='Point density', value1=pointDensity,
                                       cc='parameterChange()')

cmds.rowLayout(nc=2, cw2=[windowW / 2, windowW / 2], ct2=['both', 'both'])
cmds.button(" Evaluate Camera", h=30, c='evaluateCamPath()')
cmds.button("Undo", h=30, bgc=[0.5, 0.2, 0.2], c='cmds.delete("curveBake")')
cmds.setParent('..')

cmds.text(label='', w=windowW, h=10)
cmds.text(label='Rain setup', w=windowW, h=15, bgc=colorLevelA)
cmds.text(label='', w=windowW, h=5)

cmds.button("Make rain instancer", h=30, w=windowW, c='generateRainRig()')
cmds.text(label='', w=windowW, h=5)

cmds.rowLayout(nc=2, cw2=[windowW / 2, windowW / 2], ct2=['both', 'both'])
cmds.button("Display Mode", h=30, c='displayModeInstancer()')
cmds.button("Select Instancer", h=30, bgc=[0.5, 0.2, 0.2], c='cmds.select(instancerNode,replace=True)')
cmds.setParent('..')
cmds.text(label='', w=windowW, h=5)

rainSpeedField = cmds.floatFieldGrp(numberOfFields=1, label='Rain speed', value1=100, cc='rainParameterChange()',
                                    cl3=['left', 'left', 'left'])

cmds.setParent('..')

cmds.showWindow(SingingInTheRain)


#initiate the camera

camNode=cmds.ls(cameras=1)[0]
cmds.textFieldButtonGrp(camField, edit=True, text=str(camNode))
