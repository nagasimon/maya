### ------ Macaque Inker ------ ###

import maya.cmds as cmds
import random

grungeList = []
grungeListTmp = []
currentSel = []


# --- Functions ------------------------------------

def findPressureList(strokeObj):
    grungeShp = cmds.listRelatives(strokeObj, path=True)
    grungePressure = grungeShp[0] + '.pressure'
    return grungePressure


def increaseAll(listValues, increment):
    listNewValues = []
    for i in listValues:
        listNewValues.append(listvalues[i] + increment)
    return listNewValues


def addValueToAll(list, value):
    newList = []
    for i in list:
        newVal = i + value
        newList.append(newVal)
    return newList


def multValueToAll(list, value):
    newList = []
    for i in list:
        newVal = i * value
        newList.append(newVal)
    return newList


def smoothValue(listVal, factor):
    centralVal = sum(listVal) / float(len(listVal))
    newList = []

    for i in range(0, len(listVal)):
        newVal = listVal[i] + ((centralVal - listVal[i]) * factor)
        newList.append(newVal)

    return (newList)


def noiseValue(listVal, factor):
    noisyList = []
    for i in listVal:
        noiseValue = random.uniform(0, 1)
        noisyList.append(noiseValue)

    newList = []
    for i in range(0, len(listVal)):
        newVal = listVal[i] + ((noisyList[i] - listVal[i]) * factor)
        newList.append(newVal)

    return (newList)


def smoothInOut(listVal, distance, factor):
    smoothedList = listVal[:]
    for i in range(0, len(listVal)):
        if i <= distance:
            distPct = 1
            smoothValue = 0
            if i != 0:
                distPct = 1.00 / distance * i
                smoothValue = listVal[i] * distPct
            else:
                smoothValue = 0
            smoothedList[i] = smoothValue
        elif len(listVal) - i <= distance:
            distPct = 1
            smoothValue = 0
            if (len(listVal) - i) != 0:
                distPct = 1.00 / distance * (len(listVal) - i)
                smoothValue = listVal[i] * distPct
            else:
                smoothValue = 0
            smoothedList[i] = smoothValue
        else:
            unsmoothedValue = listVal[i]
            smoothedList[i] = unsmoothedValue

    newList = []
    for i in range(0, len(listVal)):
        newVal = listVal[i] + ((smoothedList[i] - listVal[i]) * factor)
        newList.append(newVal)

    return (newList)


def clampValues(listVal, minVal, maxVal):
    newList = []

    for i in listVal:
        if i < minVal:
            newVal = minVal
            newList.append(newVal)
        if i > maxVal:
            newVal = maxVal
            newList.append(newVal)
        else:
            newList.append(i)

    return newList


# --- Interface -------------------------------------

# - Value Modifications

def addSubstractValues():
    addSubSldVal = cmds.floatSliderGrp(addSubSld, query=True, value=True)
    # print addSubSldVal
    for i in range(0, len(grungeList)):
        valueFromTmpList = addValueToAll(grungeList[i][1], addSubSldVal)
        grungeList[i][1] = valueFromTmpList


def multValues():
    multSldVal = cmds.floatSliderGrp(multSld, query=True, value=True)
    # print multSldVal
    for i in range(0, len(grungeList)):
        grungeList[i][1] = multValueToAll(grungeList[i][1], multSldVal)


def smoothValues():
    smoothSldVal = cmds.floatSliderGrp(smoothSld, query=True, value=True)
    # print multSldVal
    for i in range(0, len(grungeList)):
        grungeList[i][1] = smoothValue(grungeList[i][1], smoothSldVal)


def noiseValues():
    noiseSldVal = cmds.floatSliderGrp(noiseSld, query=True, value=True)
    # print multSldVal
    for i in range(0, len(grungeList)):
        grungeList[i][1] = noiseValue(grungeList[i][1], noiseSldVal)


def smoothInOutValues():
    smoothInOutSldVal = cmds.floatSliderGrp(smoothInOutSld, query=True, value=True)
    smoothDistSldVal = cmds.floatSliderGrp(smoothDistSld, query=True, value=True)
    for i in range(0, len(grungeList)):
        grungeList[i][1] = smoothInOut(grungeList[i][1], int(smoothDistSldVal), smoothInOutSldVal)


def clampAllValues():
    minClampSldVal = cmds.floatSliderGrp(minClampSld, query=True, value=True)
    maxClampSldVal = cmds.floatSliderGrp(maxClampSld, query=True, value=True)
    # print multSldVal
    for i in range(0, len(grungeList)):
        grungeList[i][1] = clampValues(grungeList[i][1], minClampSldVal, maxClampSldVal)


# - Curve modifications

def sampleNumberCurve():
    sampleCurveSldVal = cmds.floatSliderGrp(curveSampleSld, query=True, value=True)
    for grunge in grungeList:
        grungeAdd = (str(grunge[0])[:-9]) + '.sampleDensity'
        cmds.setAttr(grungeAdd, sampleCurveSldVal)


def smoothCurve():
    smoothCurveSldVal = cmds.floatSliderGrp(smoothLineSld, query=True, value=True)
    for grunge in grungeList:
        grungeAdd = (str(grunge[0])[:-9]) + '.smoothing'
        cmds.setAttr(grungeAdd, smoothCurveSldVal)


def clipCurve():
    minClipSldVal = cmds.floatSliderGrp(minCurveClipSld, query=True, value=True)
    maxClipSldVal = cmds.floatSliderGrp(maxCurveClipSld, query=True, value=True)
    for grunge in grungeList:
        grungeAddMin = (str(grunge[0])[:-9]) + '.minClip'
        grungeAddMax = (str(grunge[0])[:-9]) + '.maxClip'
        cmds.setAttr(grungeAddMin, minClipSldVal)
        cmds.setAttr(grungeAddMax, maxClipSldVal)


# - Global

def ResetBaseInput():
    for u in range(0, len(grungeListTmp)):
        for v in range(0, len(grungeListTmp[u][1])):
            grungeAdd = str(grungeListTmp[u][0]) + '[' + str(v) + ']'
            grungeVal = grungeListTmp[u][1][v]
            cmds.setAttr(grungeAdd, grungeVal)


def StoreBaseInput():
    del grungeList[:]
    del grungeListTmp[:]
    del currentSel[:]

    sel = cmds.ls(sl=1)
    currentSel.extend(cmds.ls(sl=1))

    for i in sel:
        if 'strokeBrush' in i:
            pressureAddress = findPressureList(i)
            pressureList = (cmds.getAttr(pressureAddress))
            subList = [pressureAddress, pressureList[0]]
            grungeList.append(subList)
    for i in sel:
        if 'strokeBrush' in i:
            pressureAddress = findPressureList(i)
            pressureList = (cmds.getAttr(pressureAddress))
            subList = [pressureAddress, pressureList[0]]
            grungeListTmp.append(subList)


def ApplyOutput():
    grungeListTmp = grungeList[:]


def valueChange():
    selChkVal = cmds.checkBox(selCkBx, query=True, value=True)
    clampChkVal = cmds.checkBox(clampCkBx, query=True, value=True)
    clampEveryChkVal = cmds.checkBox(clampEveryCkBx, query=True, value=True)
    curveModChkVal = cmds.checkBox(curveModCkBx, query=True, value=True)

    if selChkVal == True:
        newSel = cmds.ls(sl=1)
        if newSel != currentSel:
            StoreBaseInput()
        else:
            ResetBaseInput()
            StoreBaseInput()
    else:
        ResetBaseInput()
        StoreBaseInput()

    if clampChkVal == True:
        if clampEveryChkVal == True:
            multValues()
            clampAllValues()
            addSubstractValues()
            clampAllValues()
            noiseValues()
            clampAllValues()
            smoothValues()
            clampAllValues()
            smoothInOutValues()
            clampAllValues()
        else:
            multValues()
            addSubstractValues()
            clampAllValues()
            noiseValues()
            smoothValues()
            smoothInOutValues()
            clampAllValues()
    else:
        multValues()
        addSubstractValues()
        noiseValues()
        smoothValues()
        smoothInOutValues()

    for grunge in grungeList:
        for u in range(0, len(grunge[1])):
            grungeAdd = str(grunge[0]) + '[' + str(u) + ']'
            grungeNewVal = grunge[1][u]
            cmds.setAttr(grungeAdd, grungeNewVal)

    if curveModChkVal == True:
        sampleNumberCurve()
        smoothCurve()
        clipCurve()


def resetUIValues():
    cmds.floatSliderGrp(multSld, edit=True, value=1)
    cmds.floatSliderGrp(addSubSld, edit=True, value=0)
    cmds.floatSliderGrp(smoothSld, edit=True, value=0)
    cmds.floatSliderGrp(noiseSld, edit=True, value=0)
    cmds.floatSliderGrp(smoothInOutSld, edit=True, value=0)
    cmds.floatSliderGrp(curveSampleSld, edit=True, value=1)
    cmds.floatSliderGrp(smoothLineSld, edit=True, value=0)


# --- Body of the script ---------------------------
# --- UI -------------------------------------------
windowID = 'MacaqueInker'
colorUIMain = [0.62, 0.68, 0.24]
colorUISecondary = [0.51, 0.58, 0.4]

if cmds.window(windowID, exists=True):
    cmds.deleteUI(windowID)

ColorFusion = cmds.window(windowID, title='MacaqueInker', resizeToFitChildren=True, sizeable=False)

cmds.columnLayout(adjustableColumn=True)
cmds.text(label='MacaqueInker', w=250, h=25, bgc=colorUIMain)
cmds.text(label='', w=250, h=5)

cmds.rowLayout(numberOfColumns=1, co1=75, ct1='left')
selCkBx = cmds.checkBox(label='work on selection', v=True, cc='valueChange()')
cmds.setParent('..')
cmds.button(label='Reset UI Values', command='resetUIValues()')

cmds.text(label='', w=250, h=5)
cmds.text(label='Thickness twitch', w=250, h=10, bgc=colorUISecondary)
multSld = cmds.floatSliderGrp(label='Multiply', field=True, minValue=0, maxValue=5, value=1, columnWidth3=[80, 50, 140],
                              columnAlign3=['left', 'left', 'left'], changeCommand='valueChange()')
addSubSld = cmds.floatSliderGrp(label='Add/Substract', field=True, minValue=-1.0, maxValue=1.0, value=0,
                                columnWidth3=[80, 50, 140], columnAlign3=['left', 'left', 'left'],
                                changeCommand='valueChange()')
cmds.text(label='', w=250, h=5)

cmds.text(label='Smooth/Noise', w=250, h=10, bgc=colorUISecondary)
cmds.text(label='', w=250, h=5)
smoothSld = cmds.floatSliderGrp(label='Smooth Values', field=True, minValue=0, maxValue=1, value=0,
                                columnWidth3=[80, 50, 140], columnAlign3=['left', 'left', 'left'],
                                changeCommand='valueChange()')
noiseSld = cmds.floatSliderGrp(label='Noise Values', field=True, minValue=0, maxValue=1, value=0,
                               columnWidth3=[80, 50, 140], columnAlign3=['left', 'left', 'left'],
                               changeCommand='valueChange()')
cmds.text(label='', w=250, h=5)

cmds.text(label='Smooth In Out', w=250, h=10, bgc=colorUISecondary)
cmds.text(label='', w=250, h=5)
smoothInOutSld = cmds.floatSliderGrp(label='Smooth In/Out', field=True, minValue=0, maxValue=1, value=0,
                                     columnWidth3=[80, 50, 140], columnAlign3=['left', 'left', 'left'],
                                     changeCommand='valueChange()')
smoothDistSld = cmds.floatSliderGrp(label='Smooth Distance', field=True, minValue=1, maxValue=100, value=1,
                                    columnWidth3=[80, 50, 140], columnAlign3=['left', 'left', 'left'],
                                    changeCommand='valueChange()')
cmds.text(label='', w=250, h=5)

cmds.text(label='Value Clamping', w=250, h=10, bgc=colorUISecondary)
cmds.text(label='', w=250, h=5)
minClampSld = cmds.floatSliderGrp(label='Min Clamp', field=True, minValue=-2.0, maxValue=2.0, value=0,
                                  columnWidth3=[80, 50, 140], columnAlign3=['left', 'left', 'left'],
                                  changeCommand='valueChange()')
maxClampSld = cmds.floatSliderGrp(label='Max Clamp', field=True, minValue=-2.0, maxValue=2.0, value=1,
                                  columnWidth3=[80, 50, 140], columnAlign3=['left', 'left', 'left'],
                                  changeCommand='valueChange()')
cmds.text(label='', w=250, h=5)
cmds.rowLayout(numberOfColumns=2, co2=(55, 15), ct2=('left', 'left'))
clampCkBx = cmds.checkBox(label='Clamp', v=True, cc='valueChange()')
clampEveryCkBx = cmds.checkBox(label='After Each Operation', v=False, cc='valueChange()')
cmds.setParent('..')

cmds.text(label='', w=250, h=5)

cmds.text(label='Line Sampling', w=250, h=10, bgc=colorUISecondary)
cmds.text(label='', w=250, h=5)
curveModCkBx = cmds.checkBox(label='CurveModifications', v=False, cc='valueChange()')
cmds.text(label='', w=250, h=5)
curveSampleSld = cmds.floatSliderGrp(label='Curve Sample', field=True, minValue=-0, maxValue=2.0, value=1,
                                     columnWidth3=[80, 50, 140], columnAlign3=['left', 'left', 'left'],
                                     changeCommand='valueChange()')
smoothLineSld = cmds.floatSliderGrp(label='SmoothLine', field=True, minValue=0, maxValue=10, value=0,
                                    columnWidth3=[80, 50, 140], columnAlign3=['left', 'left', 'left'],
                                    changeCommand='valueChange()')
cmds.text(label='', w=250, h=10)
minCurveClipSld = cmds.floatSliderGrp(label='Min Curve Clip', field=True, minValue=-1.0, maxValue=1.0, value=0,
                                      columnWidth3=[80, 50, 140], columnAlign3=['left', 'left', 'left'],
                                      changeCommand='valueChange()')
maxCurveClipSld = cmds.floatSliderGrp(label='Max Curve Clip', field=True, minValue=-1.0, maxValue=1.0, value=1,
                                      columnWidth3=[80, 50, 140], columnAlign3=['left', 'left', 'left'],
                                      changeCommand='valueChange()')
cmds.text(label='', w=250, h=10)

cmds.rowLayout(numberOfColumns=3, co3=(0, 0, 0), cl3=('center', 'center', 'center'))
cmds.button(label='ResetBaseInput', bgc=[0.2, 0.2, 0.4], command='ResetBaseInput()')
cmds.button(label='StoreBaseInput', bgc=[0.2, 0.4, 0.2], command='StoreBaseInput()')
cmds.button(label='ApplyOutput', bgc=[0.4, 0.2, 0.2], command='ApplyOutput()')
cmds.setParent('..')

cmds.showWindow()

StoreBaseInput()