import maya.cmds as cmds

''' Base reflexion of the projects:

-Base of the tool-
.need to be able to copy paste attribute values/animations
.with matching/non matching names
.onto multiple targets
.with an UI
.every element bein located on an external library as a .txt or .xml file
.with a snapshot of the element

-Advanced of the tool-
.recreate node chains
.import custom tools from mb files


-Function need-
.export function
.import function

-Interface need-

-object need-
.object analyser for export
    analyse all the selected object and identify the tracks he may evaluate
.valuesTrackAssigner for import
    analyse all the target objects to idenmtify the needs and the logical taget for assignement

'''

def getAttValueList(target):
    attList=cmds.listAttr(target,keyable=True)
    for att in attList:
        try:
            attCoumpound=[att]
            attCoumpound.append(cmds.getAttr(target+'.'+str(o)))
        except:
            print 'Cannot retrieve atribut "'+str(att)+'"from object "'+str(target)+'"'
    return attList

def valueListToAttList(attValueList):
    attList=(for att in attValueList:attList.append(att[0]))

def setAttValueList(attValueList,target):
    for att in attValueList:
        try:
            cmds.setAttr(target+'.'+str(att[0]),att[1])
        except:
            print 'Cannot assign value "'+str(att[1])'" to target "'+str(att[0])+'"'

def findMatchingAtt(source,target):
    matchList=[]
    for attSrc in source:
        for attTgt in cmds.listAttr(target,keyable=True):
            if attTgt == attSrc: matchList.append(attSrc)
    return matchList