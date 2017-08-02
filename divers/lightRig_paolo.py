import maya.cmds as cmds

vertexlist = cmds.ls(sl=True, fl=True)
mesh = vertexlist[0].split('.')[0]
cmds.select(mesh)
meshShape = cmds.listRelatives(shapes=True)[0]
orig = cmds.duplicate(mesh, name=mesh + 'Orig')
todelete = cmds.ls(sl=True)
cpv = cmds.rename(meshShape, mesh + 'CPVShape')
tomove = cmds.listRelatives(shapes=True)[0]
cmds.parent(tomove, mesh, shape=True, relative=True)
cmds.delete(todelete)
orig = orig[0] + 'Shape'

# create input graph

cmds.select(orig)
atpc = soup().create('arrayToPointColor')[0]
cmds.connectAttr(atpc + '.outGeometry', cpv + '.inMesh', force=True)
cmds.setAttr(atpc + '.solidAlpha', 1)
cmds.select(orig)
tta = soup().create('textureToArray')[0]
cmds.connectAttr(tta + '.outRgbaPP', atpc + '.inRgbaPP')
cmds.setAttr(tta + '.accurateSampling', 1)
tex = cmds.shadingNode('surfaceShader', asTexture=True, name=mesh + 'CPVcolor')
cmds.connectAttr(tex + '.outColor', tta + '.inColor')
cmds.setAttr(orig + '.intermediateObject', 1)
cmds.setAttr(cpv + '.displayColors', 1)

# create output graph

cmds.select(mesh)
soup().create('pointAttributeToArray')
array = cmds.ls(sl=True)[0]
soup().create('rgbaToColorAndAlpha')
rgba = cmds.ls(sl=True)[0]
soup().create('pointCloudToMesh')
bakemesh = cmds.ls(sl=True)[0]
cmds.polyCube(name=mesh + 'colorBake')
colorBake = cmds.ls(sl=True)[0]

# set nodes attributes
cmds.setAttr(array + '.pointColor', 1)
cmds.setAttr(bakemesh + '.normal', 0)
cmds.setAttr(bakemesh + '.rgba', 0)
cmds.setAttr(bakemesh + '.map', 0)
cmds.setAttr(bakemesh + '.position', 1)
cmds.setAttr(colorBake + '.visibility', 0)

# connect nodes
cmds.connectAttr(array + '.outRgbaPP', rgba + '.inRgbaPP', force=True)
cmds.connectAttr(rgba + '.outRgbPP', bakemesh + '.inPositionPP', force=True)
cmds.connectAttr(bakemesh + '.outMesh', colorBake + '.inMesh', force=True)

# 1 locator per color

vertexNo = [x.replace(x.split('.')[0], colorBake) for x in vertexlist]
cmds.select(vertexNo)
vertexConstraint_SOuP().main()

# 1 locator per light

cmds.select(vertexlist)
vertexConstraint_SOuP().main()
locs = cmds.ls(sl=True, fl=True)

# Controler

ctrl = cmds.spaceLocator(name=mesh + '_Light_CTRL')[0]
cmds.move(0, 5, 0)
cmds.addAttr(longName='lightsDisplay', attributeType='bool', defaultValue=True, hidden=False, writable=True,keyable=True)
cmds.addAttr(longName='lightsScale', attributeType='float', defaultValue=1, hidden=False, writable=True, keyable=True)
cmds.addAttr(longName='targetsDisplay', attributeType='bool', defaultValue=True, hidden=False, writable=True,keyable=True)
cmds.addAttr(longName='targetsScale', attributeType='float', defaultValue=1, hidden=False, writable=True, keyable=True)
cmds.addAttr(longName='locatorsDisplay', attributeType='bool', defaultValue=False, hidden=False, writable=True,keyable=True)
# cmds.addAttr(longName='IESfile', dataType="string", hidden=False, writable=True, keyable=True)
cmds.addAttr(longName='NormalOffset', attributeType='float', hidden=False, writable=True, keyable=True)

cmds.addAttr(longName='Intensity', attributeType='float', defaultValue=1, hidden=False, writable=True, keyable=True)
cmds.addAttr(longName='Exposure', attributeType='float', defaultValue=12, hidden=False, writable=True, keyable=True)

cmds.addAttr(longName='Spread', attributeType='float', defaultValue=1, hidden=False, writable=True, keyable=True)

cmds.addAttr(longName='DiffuseContribution', min=0,max=1,attributeType='float', defaultValue=1, hidden=False, writable=True,keyable=True)
cmds.addAttr(longName='SpecularContribution', min=0,max=1, attributeType='float', defaultValue=1, hidden=False, writable=True,keyable=True)
cmds.addAttr(longName='SSSContribution', min=0,max=1,attributeType='float', defaultValue=1, hidden=False, writable=True,keyable=True)
cmds.addAttr(longName='IndirectContribution', min=0,max=1,attributeType='float', defaultValue=1, hidden=False, writable=True,keyable=True)
cmds.addAttr(longName='VolumeContribution', min=0,max=1,attributeType='float', defaultValue=1, hidden=False, writable=True,keyable=True)

cmds.addAttr(longName='EmitDiffuse', attributeType='bool', defaultValue=True, hidden=False, writable=True, keyable=True)
cmds.addAttr(longName='EmitSpec', attributeType='bool', defaultValue=True, hidden=False, writable=True, keyable=True)
# cmds.setAttr(ctrl+'.IESfile',"IES profile here...",type="string")

for vtx in locs:
    id = vtx.split('_')[3]
    lightShape = cmds.createNode('aiAreaLight', name='AreaLight_' + id)
    light = cmds.listRelatives(lightShape, parent=True)[0]
    cmds.addAttr(light, longName='cpvColor', attributeType='float3')
    cmds.addAttr(light, longName='cpvColorX', attributeType='float', parent='cpvColor')
    cmds.addAttr(light, longName='cpvColorY', attributeType='float', parent='cpvColor')
    cmds.addAttr(light, longName='cpvColorZ', attributeType='float', parent='cpvColor')
    cmds.connectAttr('vertexConstraint*_' + colorBake + '_vtx_' + id + '.translateX', light + '.cpvColorX')
    cmds.connectAttr('vertexConstraint*_' + colorBake + '_vtx_' + id + '.translateY', light + '.cpvColorY')
    cmds.connectAttr('vertexConstraint*_' + colorBake + '_vtx_' + id + '.translateZ', light + '.cpvColorZ')
    cmds.connectAttr(ctrl + '.locatorsDisplay', 'vertexConstraint*_' + mesh + '_vtx_Shape' + id + '.lodVisibility')
    cmds.connectAttr(ctrl + '.lightsDisplay', light + '.lodVisibility')
    #cmds.connectAttr(ctrl + '.IESfile', lightShape + '.aiFilename')
    cmds.connectAttr(ctrl + '.NormalOffset', light + '.translateX')
    cmds.connectAttr(ctrl + '.lightsScale', light + '.scaleX')
    cmds.connectAttr(ctrl + '.lightsScale', light + '.scaleY')
    cmds.connectAttr(ctrl + '.lightsScale', light + '.scaleZ')
    cmds.connectAttr(ctrl + '.Exposure', lightShape + '.aiExposure')
    cmds.connectAttr(ctrl + '.EmitDiffuse', lightShape + '.emitDiffuse')
    cmds.connectAttr(ctrl + '.EmitSpec', lightShape + '.emitSpecular')

    cmds.connectAttr(ctrl + '.Intensity', lightShape + '.intensity')
    cmds.connectAttr(ctrl + '.Spread', lightShape + '.aiSpread')

    cmds.connectAttr(ctrl + '.DiffuseContribution', lightShape + '.aiDiffuse')
    cmds.connectAttr(ctrl + '.SpecularContribution', lightShape + '.aiSpecular')
    cmds.connectAttr(ctrl + '.SSSContribution', lightShape + '.aiSss')
    cmds.connectAttr(ctrl + '.IndirectContribution', lightShape + '.aiIndirect')
    cmds.connectAttr(ctrl + '.VolumeContribution', lightShape + '.aiVolume')

    lightShape = cmds.listRelatives(light, shapes=True)
    cmds.connectAttr(light + '.cpvColor', lightShape[0] + '.color')
    cmds.parent(light, vtx, relative=True)
    target = cmds.spaceLocator(name=mesh + light + id + '_target')[0]
    cmds.parent(target, vtx, relative=True)
    cmds.setAttr(target + '.translateX', 10)
    cmds.aimConstraint(target, light, weight=1, offset=(0, -90, 90), aimVector=(1, 0, 0), upVector=(0, 1, 0),worldUpType='vector', worldUpVector=(0, 1, 0))
    cmds.connectAttr(ctrl + '.lightsScale', target + '.localScaleX')
    cmds.connectAttr(ctrl + '.lightsScale', target + '.localScaleY')
    cmds.connectAttr(ctrl + '.lightsScale', target + '.localScaleZ')
    cmds.connectAttr(ctrl + '.targetsDisplay', target + '.visibility')
    cmds.connectAttr(ctrl + '.targetsScale', target + '.scaleX')
    cmds.connectAttr(ctrl + '.targetsScale', target + '.scaleY')
    cmds.connectAttr(ctrl + '.targetsScale', target + '.scaleZ')

# Sort things

locsCol = cmds.select('vertexConstraint*_' + colorBake + '_vtx_*')
cmds.group(name=mesh + '_colorHisto')
colGrp = cmds.ls(sl=True)[0]
locsPos = cmds.select('vertexConstraint*_' + mesh + '_vtx_*')
cmds.group(name=mesh + '_posHisto')
posGrp = cmds.ls(sl=True)[0]
cmds.parent(colorBake, colGrp)
cmds.setAttr(colGrp + '.visibility', 0)
cmds.group(name=mesh + '_targetsPos', empty=True, world=True)
targetGrp = cmds.ls(sl=True)[0]
cmds.select(mesh + '*_target')
targets = cmds.ls(sl=True)
cmds.parent(targets, targetGrp, absolute=True)

anno = cmds.annotate(ctrl, text='Light controls for ' + mesh, point=(0, 7, 0))
annoTransform = cmds.listRelatives(anno, parent=True)[0]
cmds.parent(anno, ctrl, shape=True, relative=True)
cmds.delete(annoTransform)
cmds.select(ctrl)
