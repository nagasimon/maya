import maya.cmds as cmds
import random as random

curves=cmds.ls(sl=1)
print curves

#Return an array with the cvs id and position in worldSpace
def getCurveCVS(inputCurve):
    cvs = cmds.getAttr(inputCurve + '.spans') + 1
    cvsPosArray=[]
    for cv in range(0,cvs):
        pos=cmds.xform(inputCurve+'.cv['+str(cv)+']',pivots=True,worldSpace=True)
        cvInfo=inputCurve+'.cv['+str(cv)+']'
        cvGrp=[cvInfo,pos]
        cvsPosArray.append(cvGrp)
    return cvsPosArray

def setCvsVal(cvsPosArray,inputCurve):
    for cvArr in cvsPosArray:
        cmds.move(cvArr[1][0],cvArr[1][1],cvArr[1][2],cvArr[0],worldSpace=True,relative=False)

def noiseCvsPosArray(cvsPosArray,noiseSize):
    for cv in cvsPosArray:
        cvPos=cv[1]


for c in curves:
    cvs=cmds.getAttr(c+'.spans')+1
    for cv in range(0,cvs):
        val=float(random.randint(0,cv))*0.01
        cmds.move(val,val,val,c+'.cv['+str(cv)+']',relative=True)
