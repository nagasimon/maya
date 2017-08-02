import maya.cmds as cmds

"""
### ----------------------------    Function List    -------------------------------###
#######################################################################################
"""
def listConnectionsClean(targetNode,inOut,debugMode):
    connectionsClean=[]
    connectionsSorted=[]
    connections=cmds.listConnections(targetNode,plugs=True,connections=True)
    for i in range(0,len(connections)-1,2):
        iConn=[connections[i+1],connections[i]]
        connectionsSorted.append(iConn)
    
    for i in connectionsSorted:
        if inOut=='in':
            if cmds.connectionInfo(i[1],isDestination=True)==True:
                connectionsClean.append(i[1].split('.')[1])
            
        if inOut=='out':
            if cmds.connectionInfo(i[1],isSource=True)==True:
                connectionsClean.append(i[1].split('.')[1])
                
    if debugMode==True:
        print '--- Raw Connections :'
        print connections
        print '--- Connections Sorted :'
        for i in connectionsSorted:
            print i
        print '--- Connections Clean Plugs :'
        for i in connectionsClean:
            print i
    
    return connectionsClean


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

def getConnectedInput():
    sel=cmds.ls(sl=1)
    inputPlugList=listConnectionsClean(sel[0],'in',debugMode=0)     
    cmds.textScrollList(plugList,e=True,removeAll=True)
    cmds.textScrollList(plugList,e=True,append=inputPlugList)

'''
def getFromList():
    selectedPlugs=cmds.textScrollList(plugList,query=True,si=True))
    spString=''
    for sp in selectedPlugs:
        if spString=='':
            spString=str(sp)
        else :
            spString=spString+'&'+str(sp)
    cmds.textFieldButtonGrp(plugField,edit=True,text=spString)
'''        
    
"""
# ---- UiStartingPoint 
"""

windowID='Arnold_AOV_Manager'
windowW=350
colorBase=[0.3,0.6,0.15]
contrastVal=-0.2
colorLevelA=brightnessCol(saturationCol(colorBase,contrastVal),contrastVal)
colorLevelB=brightnessCol(saturationCol(colorLevelA,contrastVal),contrastVal)
colorLevelC=brightnessCol(saturationCol(colorLevelB,contrastVal),contrastVal)

if cmds.window(windowID, exists=True):
    cmds.deleteUI(windowID)

    
FluidSeaMonkey=cmds.window( windowID,title=windowID,resizeToFitChildren=True,sizeable=True,w=windowW,h=150)

cmds.columnLayout()
cmds.text( label=windowID,w=windowW, h=25,bgc=colorBase)
cmds.text( label='',w=windowW, h=5)

cmds.rowLayout(nc=3)
cmds.columnLayout()
cmds.text( label='Inputs', h=25,w=80,bgc=colorLevelA)
collInput = cmds.radioCollection()
rbBeauty = cmds.radioButton( label='Beauty' )
rbRSource = cmds.radioButton( label='B Source' )
rbGSource = cmds.radioButton( label='G Source' )
rbBSource = cmds.radioButton( label='B Source' )
rbRFill = cmds.radioButton( label='R Fill' )
rbGFill = cmds.radioButton( label='G Fill' )
rbBFill = cmds.radioButton( label='B Fill' )
cmds.radioCollection( collInput, edit=True, select=rbBeauty )
cmds.text( label='', h=25)

cmds.setParent('..')
cmds.separator( style='single',height=160 )

cmds.columnLayout()
inOutAffect=cmds.radioButtonGrp(label='Affect object:',labelArray2=['Input', 'Output'], numberOfRadioButtons=2,cw3=[85,60,60],cl3=['left','left','left'],select=1 )

cmds.text( label='', h=5)
plugField=cmds.textFieldButtonGrp( label='Plug', text='', buttonLabel='GetFromList',cl3=['left','left','left'],cw3=[30,140,50],ct3=['left','left','left'],bc='getFromList()')
cmds.text( label='', h=5)
cmds.separator(w=250)
cmds.text( label='', h=5)
cmds.button(label='List Plugs',w=250,c='getConnectedInput()')
cmds.text( label='', h=5)
plugList=cmds.textScrollList(h=80,w=250,allowMultiSelection=True)
cmds.setParent('..') 
cmds.setParent('..')
cmds.text( label='', h=5)
cmds.button("Let's do this!",w=windowW,h=30)
 
cmds.showWindow(windowID)
