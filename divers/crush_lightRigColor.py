import maya.cmds as cmds

sel = cmds.ls(sl=1)
print sel

for i in sel:
    cmds.select(i)
    iShp = cmds.pickWalk(d='down')
    source = cmds.connectionInfo(iShp[0] + '.color', sourceFromDestination=True)
    try:
        cmds.disconnectAttr(str(source), iShp[0] + '.color.')
    except:
        'no connection'

cmds.select(sel)

