import maya.cmds as cmds

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
        if str(connA[B+1])==str(objA):
            conn=returnConnection(str(connB[B]))
            print conn
            if conn != "": commonConnections.append(conn)
    if infoControlSwitch==True : 
        print "------ Common Connections for "+objA+" and "+objB+" -------"
        for conn in commonConnections: print conn
    return commonConnections
        
sel=cmds.ls(sl=1)
listConn(sel[0],sel[1],True)