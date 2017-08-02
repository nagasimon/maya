import maya.cmds as cmds

scaleF = 1.1

sel = cmds.ls(sl=1)

for o in sel:
    cmds.polyCloseBorder(o + '.e[:]', ch=1)
    faceCount = cmds.polyEvaluate(o, face=True)
    cmds.delete(o + '.f[0:' + str(faceCount - 1) + ']')
    cmds.polyNormal(o + '.f[0]', normalMode=0, userNormalMode=0, ch=1)
    cmds.xform(o + '.f[0]', scale=[scaleF, scaleF, scaleF], centerPivots=True)
    cmds.polyAutoProjection(o + '.f[0]')


