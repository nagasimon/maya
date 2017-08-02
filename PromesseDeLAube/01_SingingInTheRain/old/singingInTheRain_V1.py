import maya.cmds as cmds

# Parameters
bakeSteps=0.1
pointDensity=100000
timeDetailFactor=100
boxScl=10

sctBxLocator='BoxScatter_v01_boxScatterLocator'
sctNode='BoxScatter_v01_scatterShape1'
sctBox='BoxScatter_v01_polyCube1'
instancerNode='InstancerFromCurve_RandomRotateY_v01_rainInstancer'
curveToPointCloudNode='InstancerFromCurve_RandomRotateY_v01_curvesToPointCloud1'
instanceShape='RainScatterSample_v01_rainInstanceA'

#Common Variables
nurbsArray=[]


#### -------------------------------------------- Functions ------------------------------------------

def setPosRot(obj,posArr,rotArr):
    cmds.setAttr(obj+'.translateX',posArr[0])
    cmds.setAttr(obj+'.translateY',posArr[1])
    cmds.setAttr(obj+'.translateZ',posArr[2])
    cmds.setAttr(obj+'.rotateX',rotArr[0])
    cmds.setAttr(obj+'.rotateY',rotArr[1])
    cmds.setAttr(obj+'.rotateZ',rotArr[2])


#### -------------------------------------------- Core of the Script ------------------------------------------

cam=cmds.ls(sl=1)

# import BoxScatter reference
cmds.file( "/uvfx/Projects/Promesse_de_laube/Test/Sequence_202/BoxScatter_v01.ma",
    rpr="BoxScatter_v01",
    r=True,
    type="mayaAscii",
    ignoreVersion=True,
    mergeNamespacesOnClash=False,
    options="v=0;p=17;f=0")

# Setup the options
cmds.setAttr(sctNode+'.pointDensity',pointDensity)
cmds.setAttr(sctBxLocator+'.scaleX',boxScl)
cmds.setAttr(sctBxLocator+'.scaleY',boxScl)
cmds.setAttr(sctBxLocator+'.scaleZ',boxScl)    

# place at camera location
startFrame=cmds.playbackOptions(query=True, minTime=True)*timeDetailFactor
endFrame=cmds.playbackOptions(query=True, maxTime=True)*timeDetailFactor


for i in range(int(startFrame),int(endFrame),int(bakeSteps*timeDetailFactor)):
    cmds.currentTime(i/timeDetailFactor,edit=True)
    camLocPos=cmds.xform(cam,query=True,translation=True,worldSpace=True)
    camLocRot=cmds.xform(cam,query=True,rotation=True,worldSpace=True)
    setPosRot(sctBxLocator,camLocPos,camLocRot)
    
    cmds.setAttr(sctNode+'.seed',i)
    pointArray=cmds.getAttr(sctNode+'.outPositionPP.')
    for p in pointArray:
        nurbsArray.append(p)
    
#create the curve from the point array and remove the reference
curveSource=cmds.curve(name='curveBake'+str(i/timeDetailFactor),degree=1,p=nurbsArray)
cmds.file("/uvfx/Projects/Promesse_de_laube/Test/Sequence_202/BoxScatter_v01.ma",removeReference=True )
    
#import the rain scatter reference
cmds.file( "/uvfx/Projects/Promesse_de_laube/Test/Sequence_202/RainScatterSample_v01.ma",
    rpr="RainScatterSample_v01",
    r=True,
    type="mayaAscii",
    ignoreVersion=True,
    mergeNamespacesOnClash=False,
    options="v=0;p=17;f=0")

#import the reference for the instancer
cmds.file( "/uvfx/Projects/Promesse_de_laube/Test/Sequence_202/InstancerFromCurve_RandomRotateY_v01.ma",
    rpr="InstancerFromCurve_RandomRotateY_v01",
    r=True,
    type="mayaAscii",
    ignoreVersion=True,
    mergeNamespacesOnClash=False,
    options="v=0;p=17;f=0")
    
#connect the references
cmds.connectAttr(curveSource + '.local', curveToPointCloudNode + '.inCurves[0]')
cmds.connectAttr(instanceShape+'.matrix', instancerNode+'.inputHierarchy[0]' )

#setup the animation
timeConvert=cmds.createNode('timeToUnitConversion')
cmds.setAttr(timeConvert+'.conversionFactor',-0.0004)
cmds.connectAttr('time1.outTime',timeConvert+'.input')
cmds.addAttr(instancerNode,longName='rainSpeed',at='double',dv=100)
multiplierNode=cmds.createNode('multiplyDivide')
cmds.connectAttr(timeConvert+'.output',multiplierNode+'.input1.input1X.')
cmds.connectAttr(multiplierNode+'.outputX',instancerNode+'.ty')
cmds.connectAttr(instancerNode+'.rainSpeed',multiplierNode+'.input2.input2X.')
