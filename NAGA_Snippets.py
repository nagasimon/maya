path="/uvfx/Homes/slegrand/PycharmProjects/Maya/SplitFluidSession/splitFluidSession.py"
execfile(path)

###Maya Snippets:

### great ressources:
'''
Scripts and blogs:

http://www.serge-scherbakov.com/search/label/Python
http://www.fundza.com/

Documentation:


'''

#--- Color Operations --------------------------------------

# Return the median between A and B
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

# Return A*B
def multCol(A,B):
	C=[]
	for i in range(len(A)):
		C.append(0)
		C[i]=A[i]*B[i]
	return(C)

# Return A+B
def addCol(A,B):
	C=[]
	for i in range(len(A)):
		C.append(0)
		C[i]=A[i]+B[i]
	return(C)

# Return A minus B
def minusCol(A,B):
	C=[]
	for i in range(len(A)):
		C.append(0)
		C[i]=A[i]-B[i]
	return(C)

# Return a color value blend from A to B
# C is the percentage of the blending, 1=100%
def linearCol(A,B,C):
	D=[]
	for i in range(len(A)):
		D.append(0)

		D[i]=A[i]+((B[i]-A[i])*C[i])
   
	return(D)

# Transfer hue and saturation from B to A
def hueSatCol(A,B):
	import colorsys

	hsvA=colorsys.rgb_to_hsv(A[0],A[1],A[2])
	hsvB=colorsys.rgb_to_hsv(B[0],B[1],B[2])    
	
	rgbB=colorsys.hsv_to_rgb(hsvB[0],hsvB[1],hsvA[2])
	
	return(rgbB)

# Return the median color of a list of colors (only works in RGB)
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

#--- Point Operations --------------------------------------

#get the distance between two points
def distance2Points(pointA,pointB):
	distance=(abs( pointA[0]-pointB[0] + pointA[1]-pointB[1] + pointA[2]-pointB[2]))** 0.5
	return distance

#--- Vector Operations ---------------------------------------

#normalize a vector
def normalize(v):
    norm=np.linalg.norm(v)
    if norm==0:
        return v
    return v/norm

#find the longest vector possible inside the volume of a mesh
def findLongestVector(obj):
	allVtx=getAllVtxPos([obj])
	maxDist=0
	vtxMax=['none','none']
	for vtx in allVtx:
		for vtxB in allVtx:
			distance=distance2Points(vtx,vtxB)
			if distance>maxDist:
				maxDist=distance
				vtxMax[0]=vtx
				vtxMax[1]=vtxB
	
	# Trace the vector in space		
	#cmds.curve(p=[vtxMax[0],vtxMax[1]])

	vtr=[vtxMax[0][0]-vtxMax[1][0],vtxMax[0][1]-vtxMax[1][1],vtxMax[0][2]-vtxMax[1][2]]
	return vtr

#--- Simple Operations ---------------------------------------

# Split a string at every capital letter and output a list of the words
def splitAtCapital(splitSource):
	import re
	splittedSource=re.findall('[A-Z][a-z]*',splitSource)
	return(splittedSource)

# Split a string at occuring provided symbol
def splitAtSymbol(splitSource,symbol):
	import re
	splittedSource=re.findall(str(symbol)+'*',splitSource)
	return(splittedSource)

# Send True if the provided variable is a list
def isList(object):
	listTmp=[]
	listTmp.append(object)
	if len(listTmp[0]) >1:
		return True
	else:
		return False
		
#--- Simple maya operations ---------------------------------------

### Shader Operations ---------------------------

# Return all shaders from source objects
def shadersFromObjects(source):
	matArray=[]

	objectRelatives=cmds.listRelatives(source)
	shadingEngineInput=cmds.listConnections(objectRelatives, type='shadingEngine')
	
	for connection in shadingEngineInput:
		shadingInput=cmds.connectionInfo(connection+'.surfaceShader',sfd=1)
		splittedSource=shadingInput.split('.')
		matArray.append(splittedSource[0])

	matArray = list(set(matArray))

	return matArray

# Return object with provided Shader
'''def objectsFromShader(shaderInput):
	objectArray=[]

	shadingGroup = cmds.listConnections(shaderInput)
	objectArray.append(cmds.sets(shadingGroup, q=True))

	objectArray = list(set(objectArray))

	return(objectArray)
'''

def shadersFromObjects(source):

	# get shapes of selection:
	shapesInSel = cmds.ls(dag=1,o=1,s=1,sl=1)
	# get shading groups from shapes:
	shadingGrps = cmds.listConnections(shapesInSel,type='shadingEngine')
	# get the shaders:
	shaders = cmds.ls(cmds.listConnections(shadingGrps),materials=1) 

	return shaders

# Return object with provided Shader
def objectsFromShader(shaderInput):

	shadingGroup = cmds.listConnections(shaderInput)
	objectArray=cmds.sets(shadingGroup, q=True)

	return(objectArray)


### Pivot Operations ---------------------------

# Align pivots by Serge Scherbakov.
def copyPivot (sel):
	sourceObj = sel[-1]
	targetObj = sel[0:-1]
	parentList = []
	
	for obj in targetObj:
		if cmds.listRelatives( obj, parent = True):
			parentList.append(cmds.listRelatives( obj, parent = True)[0])
		else:
			parentList.append('')
			
	if len(sel)<2:
		cmds.error('select 2 or more objects.')
		
	pivotTranslate = cmds.xform (sourceObj, q = True, ws = True, rotatePivot = True)
	cmds.parent(targetObj, sourceObj)
	cmds.makeIdentity(targetObj, a = True, t = True, r = True, s = True)
	cmds.xform (targetObj, ws = True, pivots = pivotTranslate)
	
	for ind in range(len(targetObj)):
		if parentList[ind] != '' : 
			cmds.parent(targetObj[ind], parentList[ind])
		else:
			cmds.parent(targetObj[ind], world = True)

#center the pivot of an object base on his bounding box:
#require nBBcenter()
def centerPivot(obj):
	objCenter=BBCenter(obj)
	cmds.move(objCenter[0],objCenter[1],objCenter[2], obj[0]+".scalePivot",obj[0]+".rotatePivot", absolute=True)


### Object Operations ---------------------------

#align two objects
def transferRotTrans(objA,objB):
	tA=(cmds.getAttr(objA+'.tx'),cmds.getAttr(objA+'.ty'),cmds.getAttr(objA+'.tz')) 
	rA=(cmds.getAttr(objA+'.rx'),cmds.getAttr(objA+'.ry'),cmds.getAttr(objA+'.rz'))
	cmds.setAttr(objB+'.tx',tA[0])
	cmds.setAttr(objB+'.ty',tA[1])
	cmds.setAttr(objB+'.tz',tA[2])
	cmds.setAttr(objB+'.rx',rA[0])
	cmds.setAttr(objB+'.ry',rA[1])  
	cmds.setAttr(objB+'.rz',rA[2])  

#Align only rotations
def transferRot(objA,objB):
	rA=(cmds.getAttr(objA+'.rx'),cmds.getAttr(objA+'.ry'),cmds.getAttr(objA+'.rz'))
	cmds.setAttr(objB+'.rx',rA[0])
	cmds.setAttr(objB+'.ry',rA[1])  
	cmds.setAttr(objB+'.rz',rA[2])


### Bounding Box Operations ---------------------------

#Find boundingBox center
def BBCenter(obj):
	objBB=cmds.xform(obj, query=True,worldSpace=True,boundingBox=True)
	bbCenter=[((objBB[3]-objBB[0])/2)+objBB[0],((objBB[4]-objBB[1])/2)+objBB[1],((objBB[5]-objBB[2])/2)+objBB[2]]
	return bbCenter

#Get Bb Size in localSpace
def BBSize(obj):
	objlocalBB=cmds.xform(obj, query=True,objectSpace=True,boundingBox=True)
	objBBSize=[objlocalBB[3]-objlocalBB[0],objlocalBB[4]-objlocalBB[1],objlocalBB[5]-objlocalBB[2]]
	return objBBSize

#Align by bounding boxes
def alignByBB(objList):
	selConformList=objList[:-1]
	selRef=objList[-1]
	
	for selConform in selConformList:
	
		cmds.setAttr(selConform[0]+'.tx',0)
		cmds.setAttr(selConform[0]+'.ty',0)
		cmds.setAttr(selConform[0]+'.tz',0)
		
		refBB=BBCenter(selRef)
		confBB=BBCenter(selConform)
		
		posDiff=[refBB[0]-confBB[0],refBB[1]-confBB[1],refBB[2]-confBB[2]]
		
		cmds.move(refBB[0]-confBB[0],refBB[1]-confBB[1],refBB[2]-confBB[2],selConform)
		
#Match Bounding box Sizes
def matchBBSize(objList):
	selConformList=objList[:-1]
	selRef=objList[-1]
	
	refBBSize=BBSize(selRef)

	for selConform in selConformList:	
		confBBSize=BBSize(selConform)
		factor=[(refBBSize[0]-confBBSize[0])/confBBSize[0],(refBBSize[1]-confBBSize[1])/confBBSize[1],(refBBSize[2]-confBBSize[2])/confBBSize[2]]
		cmds.setAttr(selConform[0]+'.sx',factor[0])
		cmds.setAttr(selConform[0]+'.sy',factor[1])
		cmds.setAttr(selConform[0]+'.sz',factor[2])
		
#GetClosestBB (by pshipkov, https://soup-dev.websitetoolbox.com/post/finding-minimum-bounding-box-6280318 )		
def getClosestBB():
	# obtain mesh data
	dp = om.MDagPath()
	sl = om.MSelectionList()
	sl.add(n)
	sl.getDagPath(0, dp)
	iterF = om.MItMeshPolygon(dp)
	
	# buffers
	v = 999999999.9
	p1 = om.MPoint()
	p2 = om.MPoint()
	p3 = om.MPoint()
	c = [0.0,0.0,0.0]
	s = [0.0,0.0,0.0]
	n3 = ""
	t1 = mc.createNode("transform", n="t#")
	t2 = mc.createNode("transform", n="t#")
	t3 = mc.createNode("transform", n="t#")
	mc.aimConstraint(t1, t2, wuo=t3, wut=1)
	
	# loop through the triangles of the convex hull
	while not iterF.isDone():
		pp = om.MPointArray()
		ids = om.MIntArray()
		iterF.getTriangles(pp, ids, om.MSpace.kWorld)
		for i in range(pp.length()/3):
			# define local space
			mc.setAttr(t1+".t", pp[i*3].x, pp[i*3].y, pp[i*3].z)
			mc.setAttr(t2+".t", pp[i*3+1].x, pp[i*3+1].y, pp[i*3+1].z)
			mc.setAttr(t3+".t", pp[i*3+2].x, pp[i*3+2].y, pp[i*3+2].z)
			# duplicate the convex hull and move it to the origin
			n2 = mc.duplicate(n)[0]
			mc.parent(n2, t2)
			mc.setAttr(t1+".t", 1,0,0)
			mc.setAttr(t2+".t", 0,0,0)
			mc.setAttr(t3+".t", 0,0,1)
			mc.parent(n2, w=True)
			mc.makeIdentity(n2, a=True)
			mc.move(0,0,0, n2+".scalePivot")
			mc.move(0,0,0, n2+".rotatePivot")
			# bounding box volume
			c2 = mc.getAttr(n2+".center")[0]
			s2 = mc.getAttr(n2+".boundingBoxSize")[0]
			v2 = s2[0]*s2[1]*s2[2]
			# skip if the current bbox volume
			# is bigger than the previous one
			if v2 >= v:
				mc.delete(n2)
				continue
			# cleanup
			try: mc.delete(n3)
			except: pass
			# remember some values
			n3 = n2
			v = v2
			p1.x = pp[i*3].x
			p1.y = pp[i*3].y
			p1.z = pp[i*3].z
			p2.x = pp[i*3+1].x
			p2.y = pp[i*3+1].y
			p2.z = pp[i*3+1].z
			p3.x = pp[i*3+2].x
			p3.y = pp[i*3+2].y
			p3.z = pp[i*3+2].z
			c = [c2[0],c2[1],c2[2]]
			s = [s2[0],s2[1],s2[2]]
		iterF.next()
	
	# create bounding box and move it in place
	n4 = mc.polyCube(ch=False)[0]
	n4 = mc.rename(n4, n4+"_minbbox")
	mc.setAttr(n4+".t", c[0],c[1],c[2])
	mc.setAttr(n4+".s", s[0],s[1],s[2])
	n4 = mc.parent(n4, t2)[0]
	mc.setAttr(t1+".t", p1.x, p1.y, p1.z)
	mc.setAttr(t2+".t", p2.x, p2.y, p2.z)
	mc.setAttr(t3+".t", p3.x, p3.y, p3.z)
	mc.parent(n4, w=True)
	
	# cleanup
	mc.delete(t1,t2,t3,n3)
	return n4


### OpenMaya -------------------------------------------
import maya.OpenMaya as OpenMaya

#get Soft selection informations, script by -Brian Escribano (www.meljunky.com)
def softSelection():
    #Grab the soft selection
    selection = OpenMaya.MSelectionList()
    softSelection = OpenMaya.MRichSelection()
    OpenMaya.MGlobal.getRichSelection(softSelection)
    softSelection.getSelection(selection)
   
    dagPath = OpenMaya.MDagPath()
    component = OpenMaya.MObject()
   
    # Filter Defeats the purpose of the else statement
    iter = OpenMaya.MItSelectionList( selection,OpenMaya.MFn.kMeshVertComponent )
    elements, weights = [], []
    while not iter.isDone():
        iter.getDagPath( dagPath, component )
        dagPath.pop() #Grab the parent of the shape node
        node = dagPath.fullPathName()
        fnComp = OpenMaya.MFnSingleIndexedComponent(component)   
        getWeight = lambda i: fnComp.weight(i).influence() if fnComp.hasWeights() else 1.0
       
        for i in range(fnComp.elementCount()):
            elements.append('%s.vtx[%i]' % (node, fnComp.element(i)))
            weights.append(getWeight(i)) 
        iter.next()
       
    return elements, weights
elements,weights = softSelection() 
 
 


#--- Vray ---------------------------------------

cmds.vray("addAttributesFromGroup", obj, "vray_objectID", 1)