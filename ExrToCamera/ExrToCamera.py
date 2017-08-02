## this script was assembled by j.hezer for studiorakete 2012 all input comes from frank rueter, ivan busquet and Michael Garrett 
## still wip with worldToNDC and worldToCamera only

import nuke
import os
import math
    
def getMetadataMatrix(meta_list):
    m = nuke.math.Matrix4()
    try:
        for i in range (0,16) :
            m[i] = meta_list[i]   
    except:
        m.makeIdentity()
    return m    

def ExrToCamera():
    try:
        selectedNode = nuke.selectedNode()
        nodeName = selectedNode.name()
        node = nuke.toNode(nodeName)
        if nuke.getNodeClassName(node) != 'Read':
            nuke.message('Please select a read Node')
            print 'Please select a read Node'
            return
        metaData = node.metadata()
        reqFields = ['exr/%s' % i for i in ('worldToCamera', 'worldToNDC')]
        if not set( reqFields ).issubset( metaData ):
            nuke.message('no basic matrices for camera found')
            print 'no basic matrices for camera found'
            return
        else:
            print 'found needed data'
        imageWidth = metaData['input/width']
        imageHeight = metaData['input/height']
        aspectRatio = float(imageWidth)/float(imageHeight)
        hAperture = 20.72640038
        vAperture = hAperture/aspectRatio
        
        # get additional stuff
        first = node.firstFrame()
        last = node.lastFrame()
        ret = nuke.getFramesAndViews( 'Create Camera from Metadata', '%s-%s' %( first, last )  )
        frameRange = nuke.FrameRange( ret[0] )
        camViews = (ret[1])
        
        
        for act in camViews:
            cam = nuke.nodes.Camera (name="Camera %s" % act)
            #enable animated parameters
            cam['useMatrix'].setValue( True )
            cam['haperture'].setValue ( hAperture )
            cam['vaperture'].setValue ( vAperture )
        
            for k in ( 'focal', 'matrix', 'win_translate'):
                cam[k].setAnimated()
            
            task = nuke.ProgressTask( 'Baking camera from meta data in %s' % node.name() )
    
            for curTask, frame in enumerate( frameRange ):
                if task.isCancelled():
                    break
                task.setMessage( 'processing frame %s' % frame )
            #get the data out of the exr header
                wTC = node.metadata('exr/worldToCamera',frame, act)
                wTN = node.metadata('exr/worldToNDC',frame, act)
                
            #set the lenshiift if additional metadata is available or manage to calculate it from the toNDC matrix    
                #cam['win_translate'].setValue( lensShift, 0 , frame )
                
            # get the focal length out of the worldToNDC Matrix
            # thats the wip part any ideas ??
                errCor = 0.99916081857
                # use maximum of abs wTC[0,4,8]
                iMax = 0
                if abs( wTC[ 4 ] ) > abs( wTC[ iMax ] ): iMax = 4
                if abs( wTC[ 8 ] ) > abs( wTC[ iMax ] ): iMax = 8
                focal = errCor * ( hAperture * 0.5 ) / ( wTC[ iMax ] / wTN[ iMax ] )
                cam['focal'].setValueAt(  float( focal ), frame )
            
            # do the matrix math for rotation and translation
        
                matrixList = wTC
                camMatrix = getMetadataMatrix(wTC)
                
                flipZ=nuke.math.Matrix4()
                flipZ.makeIdentity()
                flipZ.scale(1,1,-1)
             
                transposedMatrix = nuke.math.Matrix4(camMatrix)
                transposedMatrix.transpose()
                transposedMatrix=transposedMatrix*flipZ
                invMatrix=transposedMatrix.inverse()
                scale = math.sqrt( wTC[0]*wTC[0] + wTC[1]*wTC[1] + wTC[2]*wTC[2] )
                invMatrix[0] *= scale
                invMatrix[1] *= scale
                invMatrix[2] *= scale
                invMatrix[4] *= scale
                invMatrix[5] *= scale
                invMatrix[6] *= scale
                invMatrix[8] *= scale
                invMatrix[9] *= scale
                invMatrix[10] *= scale

                for i in range(0,16):
                    matrixList[i]=invMatrix[i]
                
                for i, v in enumerate( matrixList ):
                    cam[ 'matrix' ].setValueAt( v, frame, i)
            # UPDATE PROGRESS BAR
                task.setProgress( int( float(curTask) / frameRange.frames() *100) )
    except:
        print 'select at least one read node'