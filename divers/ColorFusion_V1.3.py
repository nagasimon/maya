### ColorFusion V1.1#

import maya.cmds as cmds
import re
import colorsys

#Variable and array creation
selection=[]
clrSelection=[]
attList=[]
attListTmp=[]
attListAffect=[]

#--- Basic Color Operations ---
def meanCol(A,B):
    C=[]  
    for i in range(len(A)):
        C.append(0)
        if A[i] > B[i]:
            C[i]=B[i]+((A[i]-B[i])/2)
        elif A[i] < B[i]:    
            C[i]=A[i]+((B[i]-A[i])/2)
        else:
            C[i]=A[i]
    return(C)

def multCol(A,B):
    C=[]
    for i in range(len(A)):
        C.append(0)
        C[i]=A[i]*B[i]
    return(C)

def addCol(A,B):
    C=[]
    for i in range(len(A)):
        C.append(0)
        C[i]=A[i]+B[i]
    return(C)

def minusCol(A,B):
    C=[]
    for i in range(len(A)):
        C.append(0)
        C[i]=A[i]-B[i]
    return(C)

def linearCol(A,B,C):
    D=[]
    for i in range(len(A)):
        D.append(0)

        D[i]=A[i]+((B[i]-A[i])*C[i])
   
    return(D)

def hueSatCol(A,B):
    hsvA=colorsys.rgb_to_hsv(A[0],A[1],A[2])
    hsvB=colorsys.rgb_to_hsv(B[0],B[1],B[2])    
    
    rgbB=colorsys.hsv_to_rgb(hsvB[0],hsvB[1],hsvA[2])
    
    return(rgbB)

def contrastCol(list):
    R=[]
    G=[]
    B=[]
    
    for col in list:
        R.append(col[0])
        G.append(col[1])
        B.append(col[2])
        
    contrastPointR=sum(R)/float(len(R))
    contrastPointG=sum(G)/float(len(G))
    contrastPointB=sum(B)/float(len(B))
    
    valRGB=[contrastPointR,contrastPointG,contrastPointB]
    return(valRGB)

def brightnessCol(A,b):
    hsvA=colorsys.rgb_to_hsv(A[0],A[1],A[2])
    rgbOut=colorsys.hsv_to_rgb(hsvA[0],hsvA[1],(hsvA[2]+b))
    return(rgbOut)
    
def saturationCol(A,b):
    hsvA=colorsys.rgb_to_hsv(A[0],A[1],A[2])
    rgbOut=colorsys.hsv_to_rgb(hsvA[0],(hsvA[1]+b),hsvA[2])
    return(rgbOut)
    
#--- Function list ---
def splitAtCapital(splitSource):
    splittedSource=re.findall('[A-Z][a-z]*',splitSource)
    return(splittedSource)
    
def listClr(source):
    attListOutput=[]
    attListUnsorted=cmds.listAttr(source,keyable=True)
    
    if attListUnsorted:
        for att in attListUnsorted:
            if att[-1:]=='R' or att[-1:]=='G' or att[-1:]=='B':            
                if (source+'.'+att[:-1]) not in attListOutput:
                    attListOutput.append(source+'.'+att[:-1])  
    else:
        print(source+" Clr has no keyable attribute")
        clrSelection.remove(source)

    return(attListOutput)

def valueFromAdd(Add):
    R=cmds.getAttr(Add + 'R')
    G=cmds.getAttr(Add + 'G')
    B=cmds.getAttr(Add + 'B')  
    value = [R,G,B]
    return (value)
   
def storeAttVal(list):
    del attListTmp[:]
    
    for att in list:
        currentVal=valueFromAdd(att)
        attListTmp.append(currentVal)

def initValueFromAdd(Add):
    idPos=attList.index(Add)
    return(attListTmp[idPos]) 
        
def assignValueToAdd(value,add):
    idPos=attList.index(add)
    '''#Debug
    print(idPos)
    print(attList[2])
    '''
    cmds.setAttr(attList[idPos]+'R',value[0])
    cmds.setAttr(attList[idPos]+'G',value[1])
    cmds.setAttr(attList[idPos]+'B',value[2])

# Return material from selection
def shaderFromObjects(source):
    matArray=[]

    objectRelatives=cmds.listRelatives(source)
    shadingEngineInput=cmds.listConnections(objectRelatives, type='shadingEngine')
    
    for connection in shadingEngineInput:
        shadingInput=cmds.connectionInfo(connection+'.surfaceShader',sfd=1)
        splittedSource=shadingInput.split('.')
        matArray.append(splittedSource[0])

    #matArray = list(set(matArray))

    return matArray

#--- Function of the UI ---

def generateSubList():
    cmds.treeView( clrSublist, edit=True, removeAll = True )
    for clr in clrSelection:
        clrName=clr[:-4]
        clrLay=cmds.treeView( clrSublist, e=True, addItem = (clrName, ""))
        cmds.treeView(clrSublist,e=True,expandItem=(clrName,False),selectItem=(clrName,True))
        for att in (listClr(clr)):
            cmds.treeView( clrSublist, e=True, addItem = (att, clrName))

def selectTreeCallBack(object,action):
    generateAffectList()
               
def generateAffectList():    
    #reset the list
    del attListAffect[:]

    allBaseClr=cmds.treeView(clrSublist,q=True,children='')
    print("All base Clr are:")         
    for clr in allBaseClr:
        if cmds.treeView(clrSublist,q=True,itemSelected=clr)==1:
            if cmds.treeView(clrSublist,q=True,isLeaf=clr)==1:
                attListAffect.append(clr)
                print(clr+' : Selected')
            else :
                print(clr+' : Selected with sub controllers')
                childrens=cmds.treeView(clrSublist,q=True,children=clr)
                for child in range(1,len(childrens)):
                    attListAffect.append(childrens[child])
                    print('    - '+childrens[child])
                
        else:
            print(clr+' : /')
    
    print(attListAffect)
               
def ResetBaseInput():
    for att in attList:
        idPos=attList.index(att)

        cmds.setAttr(attList[idPos]+'R',attListTmp[idPos][0])
        cmds.setAttr(attList[idPos]+'G',attListTmp[idPos][1])
        cmds.setAttr(attList[idPos]+'B',attListTmp[idPos][2])
    
    print("Base Input is reset")

    initSliders()

def StoreBaseInput():
    selection=cmds.ls(sl=1)

    if not selection:
        selection=cmds.ls()
    
    #check if it's opening of the script
    firstTime=True
    if clrSelection:
        firstTime=False
        initSliders()
                
    #emptying the arrays
    del clrSelection[:]
    del attList[:]
    
    for i in selection:
        #check if there's a CLR inside the selection
        if i[-3:]=='CLR':
            clrSelection.append(i)
        '''
        # if there is a set inside the selection, he checks id there's clr inside
        if cmds.nodeType(i)=='objectSet':
            setObjects=cmds.listConnections(i+'.dagSetMembers')            
            for setObj in setObjects:
                if setObj[-3:]=='CLR':
                    print setObj
                    clrSelection.append(setObj)
        
        #if there is objects inside the selection, he finds the materials and clr
        if cmds.nodeType(i)!='objectSet' and i[-3:]!='CLR' :
            shaders=shaderFromObjects(i)
            for shader in shaders:
                clrMatName=str(shader)
                clrTmpName=clrMatName[:-3]+'CLR'
                if clrTmpName not in clrSelection: 
                    clrSelection.append(clrTmpName)
        '''
                
    for i in clrSelection:
        attList.extend(listClr(i))
    
    if len(clrSelection)==0:
        print("No CLR in current selection")
    elif  attList is None:
        print("No color attributes in current CLR selection")
    elif selection is None:
        print("Nothing selected")
    else:
        print("Base Input Loaded correctly for")
        print(clrSelection)
    
    storeAttVal(attList)
    print("Values storred")
    
    if not firstTime:
        generateSubList()

   
def ApplyOutput():
    cmds.select(clrSelection)
    StoreBaseInput()
    print("Ouput is applyed")
    initSliders()

def ColorChange():
    #Recreate the attribute list affected
    generateAffectList()
    
    #Apply the changes
    for att in attListAffect:
        colMix=cmds.colorSliderGrp(ColorMix, query=True,rgb=True)
        colBlend=cmds.colorSliderGrp(ColorBlend, query=True,rgb=True)    
        colorChg=initValueFromAdd(att)
        if cmds.radioButton(blendBtn, q = True, sl = True):
            colorChg=colMix
        elif cmds.radioButton(multiplyBtn, q = True, sl = True):
            colorChg=multCol(initValueFromAdd(att),colMix)
        elif cmds.radioButton(lightenBtn, q = True, sl = True):
            colorChg=addCol(initValueFromAdd(att),colMix)
        elif cmds.radioButton(colorBtn, q = True, sl = True):
            colorChg=hueSatCol(initValueFromAdd(att),colMix)
        colorDef=linearCol(initValueFromAdd(att),colorChg,colBlend)
        assignValueToAdd(colorDef,att)

def initSliders():
    cmds.colorSliderGrp(ColorMix,e=True,rgb=(0.5,0.5,0.5))
    cmds.colorSliderGrp(ColorBlend,e=True,rgb=(0,0,0))
    cmds.floatSliderGrp(Contrast,e=True,value=0)
    cmds.floatSliderGrp(Brightness,e=True, value=0)
    cmds.floatSliderGrp(Saturation,e=True,value=0)

def ContrastChange():
    ColorAdjustments()
        
def BrightnessChange():
    ColorAdjustments()

def SaturationChange():
    ColorAdjustments()

def ColorAdjustments():
    #Recreate the attribute list affected
    generateAffectList()
    colorList=[]
    
    for att in attListAffect:
        colorList.append(initValueFromAdd(att))
    
    mediumVal=contrastCol(colorList)
    
    #Apply the changes
    for att in attListAffect:
        #Contrast
        colBlendVal=cmds.floatSliderGrp(Contrast,query=True,value=1)
        colBlend=[-colBlendVal,-colBlendVal,-colBlendVal]
        colorChg=mediumVal
        colorDef=linearCol(initValueFromAdd(att),colorChg,colBlend)
        #Brightness
        colBrightness=cmds.floatSliderGrp(Brightness,query=True,value=1)
        colorDef=brightnessCol(colorDef,colBrightness)
        #Saturation
        colSaturation=cmds.floatSliderGrp(Saturation,query=True,value=1)
        colorDef=saturationCol(colorDef,colSaturation)
        assignValueToAdd(colorDef,att)       

#- - - BODY OF THE SCRIPT - - -

#--- UI ---

StoreBaseInput()

windowID='ColorFusion'

if cmds.window(windowID, exists=True):
    cmds.deleteUI(windowID)
    
ColorFusion=cmds.window( windowID,title='ColorFusion',resizeToFitChildren=True,sizeable=False)

cmds.columnLayout()
cmds.text( label='ColorFusion',w=250, h=25,bgc=[0.6,0.3,0.15])
cmds.text( label='',w=250, h=5)
ColorMix=cmds.colorSliderGrp(label='ColorMix',rgb=(0.5,0.5,0.5),columnWidth3=[50,50,140],columnAlign3=['left','left','left'],changeCommand='ColorChange()')
ColorBlend=cmds.colorSliderGrp(label='Blending',rgb=(0,0,0),columnWidth3=[50,50,140],columnAlign3=['left','left','left'],changeCommand='ColorChange()')
cmds.text( label='',w=250, h=5)

cmds.text( label='Fusion modes:',w=250, h=15,bgc=[0.8,0.5,0.25] )
cmds.rowLayout(numberOfColumns=4)
cmds.radioCollection()
blendBtn=cmds.radioButton( label='Blend')
multiplyBtn=cmds.radioButton( label='Multiply' )
lightenBtn=cmds.radioButton( label='Lighten' )
colorBtn=cmds.radioButton( label='Color',sl=1 )
cmds.setParent('..')

cmds.text( label='Adjustments:',w=250, h=15,bgc=[0.8,0.5,0.25]  )
Contrast=cmds.floatSliderGrp( label='Contrast', field=True, minValue=-1, maxValue=1, fieldMinValue=-100.0, fieldMaxValue=100.0, value=0 ,step=0.1,precision=2,columnWidth3=[50,50,140],columnAlign3=['left','left','left'],changeCommand='ContrastChange()')
Brightness=cmds.floatSliderGrp( label='Brightness', field=True, minValue=-1, maxValue=1, fieldMinValue=-100.0, fieldMaxValue=100.0, value=0 ,step=0.1,precision=2,columnWidth3=[50,50,140],columnAlign3=['left','left','left'],changeCommand='BrightnessChange()')
Saturation=cmds.floatSliderGrp( label='Saturation', field=True, minValue=-1, maxValue=1, fieldMinValue=-100.0, fieldMaxValue=100.0, value=0 ,step=0.1,precision=2,columnWidth3=[50,50,140],columnAlign3=['left','left','left'],changeCommand='SaturationChange()')

layout = cmds.formLayout(w=250)

clrSublist=cmds.treeView(h=300,allowMultiSelection=True,visible=True)
cmds.formLayout(layout,e=True, attachForm=(clrSublist,'top',5))
cmds.formLayout(layout,e=True, attachForm=(clrSublist,'left', 5))
cmds.formLayout(layout,e=True, attachForm=(clrSublist,'bottom', 5))
cmds.formLayout(layout,e=True, attachForm=(clrSublist,'right', 5))
generateSubList()

cmds.setParent('..')    

cmds.rowLayout(numberOfColumns=3)
cmds.button(label='ResetBaseInput',bgc=[0.2,0.2,0.4],command='ResetBaseInput()')
cmds.button(label='StoreBaseInput',bgc=[0.2,0.4,0.2],command='StoreBaseInput()')
cmds.button(label='ApplyOutput',bgc=[0.4,0.2,0.2],command='ApplyOutput()')

cmds.showWindow()

generateAffectList()
    
