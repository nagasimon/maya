import maya.cmds as cmds

import maya.app.renderSetup.model.override as override
import maya.app.renderSetup.model.selector as selector
import maya.app.renderSetup.model.collection as collection
import maya.app.renderSetup.model.renderLayer as renderLayer
import maya.app.renderSetup.model.renderSetup as renderSetup

rs = renderSetup.instance()

baseName='splitControlRoot_'
counter=0

"""
### ----------------------------------Functions ------------------------------------###
#######################################################################################
"""

# --- Connections Functions ---

# - Try to disconnect a plug
def disconnectAbs(connectionPlug):
    dest=''
    source=''
    isDest=cmds.connectionInfo(connectionPlug,isDestination=True)
    if isDest==True:
        source=cmds.connectionInfo(connectionPlug,ges=True)
        dest=connectionPlug
    else:
        dest=cmds.connectionInfo(connectionPlug,ged=True)
        source=connectionPlug
    
    if dest!='' and source !='':
        print source
        print dest
        cmds.disconnectAttr(source,dest)
    else:
        print "disconnection failed"
        
# - return a formated connection        
def returnConnection(connectionPlug):
    dest=''
    source=''
    isDest=cmds.connectionInfo(connectionPlug,isDestination=True)
    if isDest==True:
        source=cmds.connectionInfo(connectionPlug,sfd=True)
        dest=connectionPlug
    else:
        dest=cmds.connectionInfo(connectionPlug,dfs=True)
        source=connectionPlug
    if dest!='' and source !='':
        return [source,dest]
    else:
        return ""
        
# - list connection between two objects
def listConn(objA,objB,infoControlSwitch):
    connA=cmds.listConnections(objA,connections=True)
    connB=cmds.listConnections(objB,connections=True)
    commonConnections=[]
    if infoControlSwitch==True : print "------ Connections for "+objA+" -------"
    for A in range(0,len(connA)-1,2):
        if infoControlSwitch==True : print (str(connA[A]) + " --- Connected To --- " + str(connA[A+1]))
        if str(connA[A+1])==str(objB):
            conn=returnConnection(str(connA[A]))
            print conn
            if conn != "": commonConnections.append(conn)
    if infoControlSwitch==True : print "------ Connections for "+objB+" -------"
    for B in range(0,len(connB)-1,2):
        if infoControlSwitch==True : print (str(connB[B]) + " --- Connected To --- " + str(connB[B+1]))
        if str(connB[B+1])==str(objA):
            conn=returnConnection(str(connB[B]))
            if infoControlSwitch==True : print conn
            if conn != "": commonConnections.append(conn)
    if infoControlSwitch==True : 
        print "------ Common Connections for "+objA+" and "+objB+" -------"
        for conn in commonConnections: print conn
    return commonConnections

# - duplicate the connection pattern of two object onto two others 
def dupConnectionSys(objSA,objSB,objDA,objDB):
    connList=listConn(objSA,objSB,False)
    for conn in connList:
        #reformulate A for dest Object
        connOut=objDA+"."+('.'.join(conn[0].split('.')[1:]))
        #initialise connIn by security
        connIn=''
        #If is a string reformulate and connect
        if type(conn[1])==str:
            connIn=objDB+"."+('.'.join(conn[1].split('.')[1:]))
            cmds.connectAttr(connOut,connIn,force=True)
        #If is a list of multiple output reformulate and connect
        elif conn[1] is list:
            connIn=[]
            for l in range(0,len(conn[1])-1):
                connInPart=objDB+"."+('.'.join(conn[1][l].split('.')[1:]))
                cmds.connectAttr(connOut,connInPart,force=True)
                connIn.append(connInPart)
        #### the conn In contain all output connections if a verification is needed
        # print connOut 
        # print connIn

def findFirstOf(rootNode,typeNode):
  objOut=cmds.listRelatives(rootNode,children=True,type=str(typeNode))
  objOut=objOut[0]
  return objOut

def nodeFromConnection(connection):
  nodeOut=cmds.connectionInfo(connection,sfd=1)
  nodeOut=nodeOut.split(".")[0]
  return nodeOut

"""
### ----------------------------------    UI    ------------------------------------###
#######################################################################################
"""

# Transfer Brightness from B to A
def brightnessCol(A,b):
	import colorsys

	hsvA=colorsys.rgb_to_hsv(A[0],A[1],A[2])
	rgbOut=colorsys.hsv_to_rgb(hsvA[0],hsvA[1],(hsvA[2]+b))
	return(rgbOut)

# Add b in saturation to A color    
def saturationCol(A,b):
	import colorsys

	hsvA=colorsys.rgb_to_hsv(A[0],A[1],A[2])
	rgbOut=colorsys.hsv_to_rgb(hsvA[0],(hsvA[1]+b),hsvA[2])
	return(rgbOut)

#Setup the basis of a batchCacheSetup
def batchCacheSetup():
  visibleFluids=cmds.ls(sl=0,type='fluidShape',visible=True)
  #generate the fluids groups
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

#Start Variables for Auto Rename Split Sessions
def duplicateFluidGroup():
  global counter
  sel=cmds.ls(sl=1)
  dup=cmds.duplicate(sel,rr=True,renameChildren=True,instanceLeaf=True,ic=True)

  #----- Finding targets
  #Find the emitter
  dupEmitter=findFirstOf(dup,'fluidEmitter')
  #Find the source emitter
  emitterSrc=findFirstOf(sel,'fluidEmitter')
  #Search for the input anim and mult
  animNode=nodeFromConnection(dupEmitter+".fluidDensityEmission")
  multNode=nodeFromConnection(dupEmitter+".directionalSpeed")
  fluidShapeNode=nodeFromConnection(emitterSrc+".deltaTime[0]")


  #----- Clean the duplication nodes and connections
  #Duplicate the node giving him a proper new name, as the dupMultnode Return nothing
  #Naming Section
  newAnimRoot=baseName+str(counter)
  newMultNode=baseName+"mult_"+str(counter)
  newFluidShapeNode=baseName+"fluidSh_"+str(counter)
  

  cmds.duplicate(animNode,n=newAnimRoot)
  cmds.createNode('multiplyDivide',n=newMultNode)

  cmds.connectAttr(multNode+".input2.input2X",newMultNode+".input2X")
  #cmds.setAttr(newMultNode+".input2X",cmds.getAttr(multNode+".input2.input2X"))
  cmds.connectAttr(newAnimRoot+".output",newMultNode+".input1X")

  disconnectAbs(dupEmitter+".fluidDensityEmission")
  disconnectAbs(dupEmitter+".directionalSpeed")

  cmds.connectAttr(newAnimRoot+".output",dupEmitter+".fluidDensityEmission",force=True)
  cmds.connectAttr(newMultNode+".outputX",dupEmitter+".directionalSpeed",force=True)

  cmds.duplicate(fluidShapeNode,n=newFluidShapeNode)
  dupConnectionSys(emitterSrc,fluidShapeNode,dupEmitter,newFluidShapeNode)

  #cleanup, because I'm a dirty morron obviously
  #Find the old container
  flShapeDup=cmds.listRelatives(dup,type='transform')
  for i in flShapeDup:
      #print i
      #print cmds.nodeType(i)
      if cmds.nodeType(i)=='transform':
	  cmds.delete(i)
  cmds.parent(newFluidShapeNode,dup)
  nowTime=int(cmds.currentTime(query=True))
  cmds.selectKey(newAnimRoot,time=(-300,nowTime),k=True)
  cmds.cutKey(animation='keys',clear=True )
  cmds.setAttr(newFluidShapeNode+'.startFrame',nowTime)
  
  renderSetupName='renderSplit_'+str(counter)
  rsl = rs.createRenderLayer(renderSetupName)
  c1 = rsl.createCollection("coll_"+renderSetupName)
  c1.getSelector().setPattern(str(dup[0])+'|*')
  
  
  counter=counter+1
  
def enableAllEval():
  visibleFluids=cmds.ls(sl=0,type='fluidShape',visible=True)
  for fluidB in visibleFluids:
    cmds.setAttr(fluidB+'.disableInteractiveEval',0)
    

def disableAllEval():
  visibleFluids=cmds.ls(sl=0,type='fluidShape',visible=True)
  for fluidB in visibleFluids:
    cmds.setAttr(fluidB+'.disableInteractiveEval',1)
    
"""
# ---- UiStartingPoint 
"""

windowID='FluidSeaMonkey'
windowW=150
colorBase=[0.15,0.3,0.6]
contrastVal=-0.2
colorLevelA=brightnessCol(saturationCol(colorBase,contrastVal),contrastVal)
colorLevelB=brightnessCol(saturationCol(colorLevelA,contrastVal),contrastVal)
colorLevelC=brightnessCol(saturationCol(colorLevelB,contrastVal),contrastVal)

if cmds.window(windowID, exists=True):
    cmds.deleteUI(windowID)
    
FluidSeaMonkey=cmds.window( windowID,title='FluidSeaMonkey',resizeToFitChildren=True,sizeable=True,w=windowW)

cmds.columnLayout()
cmds.text( label='FluidSeaMonkey',w=windowW, h=25,bgc=colorBase)
cmds.text( label='',w=windowW, h=5)

cmds.text( label='FluidGestion:',w=windowW, h=15,bgc=colorLevelA)
cmds.text( label='',w=windowW, h=5)
cmds.button(label='Disable all evaluation',bgc=colorLevelB,command='disableAllEval()',w=windowW)
cmds.button(label='Enable all evaluation',bgc=colorLevelB,command='enableAllEval()',w=windowW)
cmds.text( label='',w=windowW, h=5)

cmds.text( label='FluidSplit:',w=windowW, h=15,bgc=colorLevelA)
cmds.text( label='',w=windowW, h=5)
cmds.button(label='SplitFluid',bgc=colorLevelB,command='duplicateFluidGroup()',w=windowW)
cmds.text( label='',w=windowW, h=5)


cmds.text( label='FluidCaches:',w=windowW, h=15,bgc=colorLevelA)
cmds.text( label='',w=windowW, h=5)
cmds.button(label='Batch Cache Setup',bgc=colorLevelB,command='batchCacheSetup()',w=windowW)
cmds.text( label='',w=windowW, h=5)

cmds.setParent('..') 
cmds.setParent('..')
 
cmds.showWindow()
