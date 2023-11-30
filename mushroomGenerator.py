import maya.cmds as cmds
import random

def showParameter(*args):
    showCheckbox = cmds.checkBoxGrp(smooth, q = True)
    cmds.checkBoxGrp(layers, edit=True, enable=True) 
   
def hideParameter(*args):
    showCheckbox = cmds.checkBoxGrp(smooth, q = True, vis = False, v1 = False)
    cmds.checkBoxGrp(layers, edit=True, enable=False)
   
#UI
window = cmds.window(title="Mushroom Generator", menuBar = True, width=200)
cmds.columnLayout("Block")


nameparam = cmds.textFieldGrp(label = 'Name')

cmds.intSliderGrp("num", label="Number of Mushrooms", field = True, min = 1, max = 20, v = 4)
cmds.intSliderGrp("height", label="Average Height", field = True, min = 1, max = 15, v = 4)
cmds.floatSliderGrp("heightstd", label="Height Standard Deviation", field = True, min = 0.5, max = 8, v = 1)
cmds.intSliderGrp("bend", label="Average Bend", field = True, min = 0, max = 10, v = 2)
cmds.floatSliderGrp("bendstd", label="Bend Standard Deviation", field = True, min = 0.1, max = 10, v = 0.5)

smooth = cmds.checkBoxGrp("smooth", numberOfCheckBoxes=1, label='Smooth ', v1=False, onc = showParameter, ofc = hideParameter)

layers = cmds.checkBoxGrp("layers", numberOfCheckBoxes=1, label='    Save a LP Copy ', v1=False)
cmds.checkBoxGrp(layers, edit=True, enable=False)

#NEEDS TO IMPLEMENTED: set layer visiblity HP T, LP F, and make it check for layer with the same name, only create layer if it does not exist

#    if mushroom cap is pointy, it gives off a fantastical vibe
#    NEEDS TO GET DONE: separate out when capheight > 0 adjust the curve for a smooth round cap

cmds.button(label="Create Mushroom", c="createMushroom()")
cmds.showWindow(window)

def appendName(name, textstring):
    textstring = name + textstring
    return textstring

def normalDistrib(mean, std, size):
    heightlist = []
    upperlim = mean + std
    otherupperlim = mean - std
    controlnum = int(size*0.341)
    for i in range(controlnum):
        heightlist.append(random.uniform(mean, upperlim))
        heightlist.append(random.uniform(otherupperlim, mean))
    lowerlim = upperlim
    upperlim = upperlim + std
    otherlowerlim = otherupperlim
    otherupperlim = otherupperlim - std
    if (otherupperlim < 0):
        otherupperlim = 0
    
    controlnum = int(size*0.136)
    for i in range(controlnum):
        heightlist.append(random.uniform(lowerlim, upperlim))
        heightlist.append(random.uniform(otherupperlim, otherlowerlim))
    lowerlim = upperlim
    upperlim = upperlim + std
    otherlowerlim = otherupperlim
    otherupperlim = otherupperlim - std
    if (otherupperlim < 0):
        otherupperlim = 0
    
    controlnum = int(size*0.021)
    for i in range(controlnum):
        heightlist.append(random.uniform(lowerlim, upperlim))
        heightlist.append(random.uniform(otherupperlim, otherlowerlim))
    
    while (len(heightlist) < size):
        if (len(heightlist) == (size - 1)):
            sum = 0
            for h in range(len(heightlist)):
                sum = sum + heightlist[h]
            heightlist.append((mean * size) - sum)
        else:
            upperlim = upperlim + std
            heightlist.append(random.uniform(mean, upperlim))
            
    return heightlist
    
def randomLocation():
    coordinates = []
    for i in range(2):
        coordinates.append(random.uniform(-40, 45))
    return coordinates
    
    
def clusterLocation(size):
    singleCoordinates = normalDistrib(200, 20, size)
    for i in range(len(singleCoordinates)):
        singleCoordinates[i] = singleCoordinates[i] - 200
    random.shuffle(singleCoordinates)
    return singleCoordinates
    
def setDisplayLayerVis(name, visible):
    '''Toggle display layer visibility

    Args:
        name (str): Display layer name
        on (bool): True to enable layer, False to disable
    '''
    
    cmds.setAttr('{}.visibility'.format(name), visible)
    cmds.layerButton(name, edit=True, lv=visible)
    
def findShadingGroup(node): 
    """ Walks the shader graph to find the shading group """ 
    result = None 
 
    connections = cmds.listConnections(node, source=False) 
 
    if connections: 
        for connection in connections: 
            if cmds.nodeType(connection) == 'shadingEngine': 
                result = connection 
            else: 
                result = findShadingGroup(connection) 
                if result is not None: 
                    break 
 
    return result 

    
def createMushroom():
    inputname = cmds.textFieldGrp(nameparam, query = True, text = True)
   
    num = cmds.intSliderGrp("num", q = True, v=True)
    height = cmds.intSliderGrp("height", q = True, v=True)
    heightstd = cmds.floatSliderGrp("heightstd", q = True, v=True)
    
    bend = cmds.intSliderGrp("bend", q = True, v=True)
    bendstd = cmds.floatSliderGrp("bendstd", q = True, v=True)
    bend = bend * 10
    bendstd = bendstd*10
    
    smooth = cmds.checkBoxGrp("smooth", q = True, v1=True)
   
    layers = cmds.checkBoxGrp("layers", q = True, v1=True)
    #random
    heightlist = normalDistrib(height, heightstd, num)  
    bendlist = normalDistrib(bend, bendstd, num)  
    
    
    xCoordinates = clusterLocation(num)
    zCoordinates = clusterLocation(num)
    
    #display layers
    if (smooth == True and layers == True):
        layer1 = cmds.createDisplayLayer(n="LowPoly")
        layer2 = cmds.createDisplayLayer(n="HighPoly")
    
    for x in range(1, num+1):
        #obj name
        name = inputname + str(x)

        addheight = heightlist[x - 1]
        
        addwidth = random.uniform(0,9)
        
        #basic mushroom 
        if x%3 == 0:
            outline = cmds.curve(bezier=True, d=3, p=[(0.0569524, 4.935496+addheight, 0), (0.0569524, 4.935496+addheight, 0), (2.924011, 5.060151+addheight, 0), (4.139394, 4.71735+addheight, 0),(5.354778, 4.37455+addheight, 0), (6.383179, 4.156404+addheight, 0), (6.819471, 3.128003+addheight, 0), (7.255762, 2.099601+addheight, 0), (7.723217, 3.793489-4+addheight, 0), (6.13387, 2.983233-4+addheight, 0), (4.544522, 2.172978-4+addheight, 0), 
              (2.550047, 3.076724-4+addheight, 0), (2.612374, 2.422287-4+addheight, 0), (2.674701,  1.76785-4+addheight, 0), (2.425392, -4.379682+addheight, 0), (2.83052, -7.748121+addheight, 0),
               (2.883339, -5.604563, 0), (3.739306, -6.846439, 0), (2.675708, -7.366924, 0), (1.61211, -7.887408, 0), (0.0053979, -7.729, 0), (0.0053979, -7.729, 0)], k=[0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7])         
        elif x%4==0:
            addwidth = 0.6*addwidth
            outline = cmds.curve(bezier=True, d=3, p=[(0.0105626, 0.878479+addheight, 0), (0.0105626, 0.878479+addheight, 0), (4.283515, 0.684254+addheight, 0), (5.545978, 1.145538+addheight, 0), (6.808441 + addwidth * 0.7, 1.606823+addheight, 0), (7.949513 + addwidth, 2.189498+addheight, 0), (7.925235 + addwidth*0.8, 1.461154+addheight, 0), (7.900957 + addwidth * 0.6, 0.73281+addheight, 0), 
            (7.026944,2.887672-4+addheight, 0), (4.720521, 2.863393-4+addheight, 0),(2.414098, 2.839115-4+addheight, 0), (2.923939, 3.179009-4+addheight, 0), (2.7, 1.843712-4+addheight, 0), (3, 0.508414-4+addheight, 0), (2.584045, 0.508414-4+addheight, 0), (3.1, -4.802605+addheight, 0), 
             (3.3, -6.113625, 0), (3.739306, -6.846439, 0), (2.675708, -7.366924, 0), (1.61211, -7.887408, 0), (0.0053979, -7.729, 0), (0.0053979, -7.729, 0)], k=[0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7]) 

        else:
            outline = cmds.curve(bezier=True, d=3, p=[(0.034739, 4.932942+addheight, 0), (0.034739, 4.932942+addheight, 0), (8.812134, 5.859316+addheight, 0), (9.043727, 3.242309+addheight, 0), (9.275321, 0.625303+addheight, 0), (11.938646 + addwidth, 1.019012+addheight, 0), (9.66903 + 0.7*addwidth, -0.741099+addheight, 0), (7.399413, -2.50121+addheight, 0), (6.959385, -1.389561+addheight, 0), (5.662462, -1.389561+addheight, 0), (4.365538, -1.389561+addheight, 0), (2.837021, -0.764259+addheight, 0), (2.582268, -1.78327+addheight, 0), (2.327515, -2.802282+addheight, 0), (2.744383, -3.149672+addheight, 0), (2.813861, -4.377118+addheight, 0), (2.883339, -5.604563, 0), (3.739306, -6.846439, 0), (2.675708, -7.366924, 0), (1.61211, -7.887408, 0), (0.0053979, -7.729, 0), (0.0053979, -7.729, 0)], k=[0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7]) 
        
        
        
        #adjust curve shape by moving handle
        cmds.select("bezier1.cv[1]")
        
           
        
        mushroom = cmds.revolve(outline, ch=1, po=1, rn=0, ssw=0, esw=360, ut=0, tol=0.01, degree=3, s=12, ulp=1, ax=(0, 1, 0), n=name)
        #fix normals
        mushroom = cmds.polyNormal(mushroom, normalMode=0, userNormalMode=1, ch=1, n=name)
        cmds.delete(outline)
        
        #retopo top of mushroom to get rid of the triangles
        #delete faces
        facenums = ['.f[99]', '.f[101]', '.f[102]', '.f[117]', '.f[118]', '.f[126]', '.f[128]', '.f[129]', '.f[386]', '.f[389]', '.f[387]', '.f[390]', '.f[406]',
         '.f[405]', '.f[414]', '.f[417]', '.f[416]', '.f[475]', '.f[476]', '.f[478]', '.f[478]', '.f[479]', '.f[478]', '.f[494]', '.f[495]', '.f[503]', '.f[505]',
         '.f[506]', '.f[9]', '.f[10]', '.f[12]', '.f[13]', '.f[28]',  '.f[29]', '.f[37]', '.f[39]', '.f[40]', '.f[98]']
        faces = []
        for face in facenums:
            faces.append(appendName(name, face))
            
        cmds.polyDelFacet(*faces)
        #create new faces
        edgenums = ['.e[86]', '.e[209]', '.e[84]', '.e[207]', '.e[65]', '.e[211]', '.e[69]', '.e[203]', '.e[26]', '.e[241]', '.e[36]', '.e[239]', '.e[30]', 
        '.e[256]', '.e[34]', '.e[258]', '.e[251]', '.e[992]', '.e[785]', '.e[999]', '.e[783]', '.e[997]', '.e[787]', '.e[981]', '.e[779]', '.e[983]', '.e[817]',
         '.e[945]', '.e[815]', '.e[953]', '.e[832]', '.e[949]', '.e[834]', '.e[951]']
        edges = []
        for edge in edgenums:
            edges.append(appendName(name,edge))
        
        i = 0
        while i < len(edges):     
            cmds.polyBridgeEdge(edges[i], edges[i+1], dv = 0)
            i = i + 2
        
        #retopo bottom of mushroom to get rid of triangles
        #delete faces
        facenums = ['.f[358]', '.f[353]', '.f[347]', '.f[350]', '.f[308]', '.f[329]', '.f[321]', '.f[324]', '.f[164]', '.f[260]', '.f[255]', '.f[252]', 
        '.f[249]', '.f[210]', '.f[210]', '.f[249]', '.f[252]', '.f[231]', '.f[223]', '.f[226]', '.f[0]', '.f[712]', '.f[717]', '.f[706]', '.f[709]', 
        '.f[667]', '.f[688]', '.f[680]', '.f[683]', '.f[523]', '.f[619]', '.f[614]', '.f[608]', '.f[611]', '.f[569]', '.f[590]', '.f[582]', '.f[585]', '.f[1]']
        faces = []
        for face in facenums:
            faces.append(appendName(name, face))
            
        cmds.polyDelFacet(*faces)
        
        #create faces
        edgenums = ['.e[540]', '.e[663]','.e[532]', '.e[658]', '.e[524]', '.e[670]', '.e[529]', '.e[633]', '.e[449]', '.e[708]', '.e[491]', '.e[703]', 
        '.e[477]', '.e[711]', '.e[483]', '.e[719]', '.e[0]', '.e[1]', '.e[1176]', '.e[1402]', '.e[1171]', '.e[1395]', '.e[1183]', '.e[1387]', '.e[1146]', 
        '.e[1392]', '.e[1221]', '.e[1320]', '.e[1216]', '.e[1357]', '.e[1224]', '.e[1345]', '.e[1232]', '.e[1350]']
        edges = []
        for edge in edgenums:
            edges.append(appendName(name,edge))
        
        i = 0
        while i < len(edges):     
            cmds.polyBridgeEdge(edges[i], edges[i+1], dv = 0)
            i = i + 2
        
        #scale down top faces
        edgenums = ['.e[20]', '.e[24]', '.e[28]', '.e[30]', '.e[59]', '.e[63]', '.e[73]', '.e[78]', '.e[80]', '.e[197]', '.e[201]', '.e[203]', '.e[205]', '.e[233]', 
        '.e[235]', '.e[245]', '.e[250]', '.e[252]', '.e[740]', '.e[744]', '.e[746]', '.e[748]', '.e[776]', '.e[778]', '.e[790]', '.e[793]', '.e[795]', '.e[906]', 
        '.e[910]', '.e[912]', '.e[914]', '.e[942]', '.e[944]', '.e[953]', '.e[958]', '.e[960]']
        edges = []
        for edge in edgenums:
            edges.append(appendName(name,edge))
        
        cmds.scaleComponents(0.03, 1, 0.03, edges)
       
        #soften
        cmds.polySoftEdge(a = 180)
        
        #randomize shape
        
        vertnums = ['.vtx[481]', '.vtx[425]', '.vtx[483]', '.vtx[21]', '.vtx[22]', '.vtx[23]', 
        '.vtx[27]', '.vtx[28]', '.vtx[37]', '.vtx[38]', '.vtx[47]', '.vtx[51]', '.vtx[52]', '.vtx[115]', '.vtx[116]', '.vtx[120]', '.vtx[121]', '.vtx[130]', '.vtx[131]', '.vtx[140]', '.vtx[144]',
        '.vtx[145]', '.vtx[395]', '.vtx[396]', '.vtx[400]', '.vtx[401]', '.vtx[410]', '.vtx[411]', '.vtx[420]', '.vtx[424]', '.vtx[425]', '.vtx[483]', '.vtx[484]', '.vtx[488]', '.vtx[489]', 
        '.vtx[498]', '.vtx[499]', '.vtx[506]', '.vtx[509]', '.vtx[472]', '.vtx[476]', '.vtx[482]',
        '.vtx[381]', '.vtx[3]', '.vtx[4]', '.vtx[5]', '.vtx[16]', '.vtx[20]', '.vtx[26]', '.vtx[29]', '.vtx[36]', '.vtx[45]', '.vtx[50]', '.vtx[101]', '.vtx[102]', '.vtx[111]', '.vtx[114]', 
        '.vtx[119]', '.vtx[122]', '.vtx[129]', '.vtx[138]', '.vtx[143]', '.vtx[381]', '.vtx[382]', '.vtx[391]', '.vtx[394]', '.vtx[399]', '.vtx[402]', '.vtx[409]', '.vtx[418]', '.vtx[423]', 
        '.vtx[470]', '.vtx[479]', '.vtx[482]', '.vtx[487]', '.vtx[490]', '.vtx[497]', '.vtx[504]', '.vtx[508]']
               
        verts = []
        for vert in vertnums:
            verts.append(appendName(name,vert))
        
        for j in range(10):
            point = verts[random.randint(0, len(verts) - 1)]
            value = random.uniform(0, 6)
            cmds.select(point)
           
            value = random.uniform(0, 1)
            cmds.move(value, relative = True, ls = True, moveY = True)


        #bend
        cmds.select(name)
        bendDeformer = cmds.nonLinear(type = 'bend', curvature=bendlist[x-1])
        cmds.select(bendDeformer[1])
        lowbound = bendDeformer[0] + '.lowBound'
        cmds.setAttr(lowbound, -3.66)
     
        highbound = bendDeformer[0] + '.highBound'
        cmds.setAttr(highbound, 0)
        
     
        #clear history
        cmds.select(name)
        cmds.delete(name, constructionHistory = True)
     
        #rotate
        cmds.select(name)
        val = bendlist[x-1] * 1.2
        if val < 0:
            val = 0
        degrees = '-' + str(val) + 'deg'
        cmds.rotate(0, 0, degrees, r=True)
        
        cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn=1)
        deg = random.uniform(0, 360)
        cmds.rotate(0, deg,0, r=True)
     
        #move
        #coordinates = randomLocation()
        
        print(xCoordinates[x-1])
        print(zCoordinates[x-1])
        cmds.move(xCoordinates[x-1], 0, zCoordinates[x-1], relative = True)
        #cmds.move(0, 0, , relative = True, z = True)
        
        
        #UVS
        cmds.polyProjection(name+".f[0:717]", md = 'y')
        
        edgenums = ['.e[723]', '.e[897]', '.e[954]', '.e[967]', '.e[972]', '.e[1034]', '.e[1042]', '.e[1049]', '.e[1054]', '.e[1236]', '.e[1299]', '.e[1307]', '.e[1314]', '.e[1319]', '.e[1361]', '.e[1381]', '.e[1386]', '.e[1399]', '.e[1403]', '.e[1412]', '.e[1428]']
        
        moreedges = ['.e[10]', '.e[14]', '.e[31]', '.e[41]', '.e[50]', '.e[54]', '.e[68]', '.e[81]', '.e[91]', '.e[189:190]', '.e[206]', '.e[214]', '.e[222]', '.e[226]', '.e[240]', '.e[253]', '.e[263]', '.e[364]', '.e[368]', '.e[372]', '.e[377]', '.e[408]', '.e[412]', '.e[424]', '.e[429]', '.e[432]', '.e[452]', '.e[456]', '.e[465]', '.e[474]', '.e[495]', '.e[500]', '.e[507]', '.e[512]', '.e[521]', '.e[554]', '.e[558]', '.e[560]', '.e[564]', '.e[594]', '.e[596]', '.e[608]', '.e[613]', '.e[616]', '.e[635]', '.e[640]', '.e[647]', '.e[655]', '.e[674]', '.e[679]', '.e[686]', '.e[691]', '.e[700]', '.e[729]', '.e[733]', '.e[749]', '.e[757]', '.e[765]', '.e[769]', '.e[783]', '.e[796]', '.e[806]', '.e[898:899]', '.e[915]', '.e[923]', '.e[931]', '.e[935]', '.e[949]', '.e[961]', '.e[970]', '.e[1067]', '.e[1071]', '.e[1073]', '.e[1077]', '.e[1107]', '.e[1109]', '.e[1121]', '.e[1126]', '.e[1129]', '.e[1148]', '.e[1153]', '.e[1160]', '.e[1168]', '.e[1187]', '.e[1192]', '.e[1199]', '.e[1204]', '.e[1213]', '.e[1245]', '.e[1249]', '.e[1251]', '.e[1255]', '.e[1285]', '.e[1287]', '.e[1298]', '.e[1303]', '.e[1306]', '.e[1322]', '.e[1327]', '.e[1334]', '.e[1342]', '.e[1360]', '.e[1365]', '.e[1372]', '.e[1377]', '.e[1385]']
        edgenums.extend(moreedges)
        edges = []
        for edge in edgenums:
            edges.append(appendName(name,edge))
        
        cmds.polyMapCut(edges)
        cmds.select(name + '.f[0:717]')
        cmds.u3dUnfold(name + '.f[0:717]', ite=1, p=0, bi=1, tf=1, ms=1024, rs=0)
        #performPolyLayoutUV(0);
        cmds.u3dLayout(name+'.f[0:717]', res=256, scl=1, box=[0, 1, 0, 1])
        
        #create a shader
        '''
        capshader = cmds.shadingNode('aiStandardSurface', asShader = True, n='capshader'+name)
        cmds.sets(renderable=True, noSurfaceShader= True, empty=True, n= 'aiSurfaceShader' + name + 'SG')
        cmds.connectAttr('capshader' + name + '.outColor', 'aiSurfaceShader' + name +'SG.surfaceShader', f=True)
        
        
        cmds.shadingNode('volumeNoise', asTexture = True, n='volumeNoise' + name)
        cmds.shadingNode('place3dTexture', asUtility = True, n='place3dTexture' + name)
        cmds.connectAttr('place3dTexture' + name + '.wim[0]', 'volumeNoise' + name + '.pm')
        cmds.connectAttr('volumeNoise' + name + '.outColor', 'capshader' + name + '.baseColor', f=True)
        
        cmds.select('capshader' + name)
        cmds.setAttr('volumeNoise' + name + '.defaultColor', 0.945, 0, 0, type='double3')
        cmds.setAttr('volumeNoise' + name + '.colorOffset', 0.084, 0.0452593, 0.035868, type='double3')
        cmds.setAttr('volumeNoise' + name + '.colorGain', 0.665, 0.24605, 0.24605, type='double3') 
        '''
        #cap shader
        #capshader = cmds.shadingNode('aiStandardSurface', asShader = True, n='capshader' + name)
        captexture = cmds.shadingNode('substanceNode', asTexture=True, n='substanceNode' + name)
        cmds.shadingNode('place2dTexture', asUtility=True, n = 'place2dTexture' + name)
        cmds.connectAttr('place2dTexture' + name + '.outUV', 'substanceNode' + name + '.uv')
        cmds.connectAttr('place2dTexture' + name + '.outUvFilterSize', 'substanceNode' + name + '.uvFilterSize')
        #load substance .sbar file
        substanceFilename = 'E:\materials\mushrooomcap.sbsar'
        cmds.substanceNodeLoadSubstance('substanceNode' + name, substanceFilename)
        cmds.substanceNodeApplyWorkflow('substanceNode' + name, workflow = cmds.substanceGetWorkflow())
        shadingGroup = findShadingGroup(captexture)
        cmds.setAttr('substanceNode' + name + '.input_spotsScale', 6)
        cmds.setAttr('substanceNode' + name + '.input_edgeWidth', 10)
        cmds.setAttr('substanceNode' + name + '.input_randomseed', random.randint(1, 10000))
        
        cmds.select(name)
        if x%3 == 0:
            facenums = ['.f[387]', '.f[385]', '.f[42:43]', '.f[45:46]', '.f[61:62]', '.f[70]', '.f[72:73]', '.f[122:123]', '.f[125:126]', '.f[141:142]', '.f[150]', '.f[152:153]', '.f[384:385]', '.f[387:388]', '.f[403:404]', '.f[412]', '.f[414:415]', '.f[464:465]', '.f[467:468]', '.f[483:484]', '.f[492]', '.f[494:495]',
                '.f[353]', '.f[350]', '.f[2:3]', '.f[8]', '.f[11]', '.f[16]', '.f[19]', '.f[24]', '.f[30]', '.f[35]', '.f[82:83]', '.f[88]', '.f[91]', '.f[96]', '.f[99]', '.f[104]', '.f[110]', '.f[115]', '.f[344:345]', '.f[350]', '.f[353]', '.f[358]', '.f[361]', '.f[366]', '.f[372]', '.f[377]', '.f[424:425]', '.f[430]', 
                '.f[433]', '.f[438]', '.f[441]', '.f[446]', '.f[452]', '.f[457]', '.f[355]', '.f[354]', '.f[12:13]', '.f[17:18]', '.f[25:26]', '.f[32]', '.f[36:37]', '.f[92:93]', '.f[97:98]', '.f[105:106]', '.f[112]', '.f[116:117]', '.f[354:355]', '.f[359:360]', '.f[367:368]', '.f[374]', '.f[378:379]', '.f[434:435]', 
                '.f[439:440]', '.f[447:448]', '.f[454]', '.f[458:459]', '.f[352]', '.f[351]', '.f[9:10]', '.f[14:15]', '.f[22:23]', '.f[31]', '.f[33:34]', '.f[89:90]', '.f[94:95]', '.f[102:103]', '.f[111]', '.f[113:114]', '.f[351:352]', '.f[356:357]', '.f[364:365]', '.f[373]', '.f[375:376]', '.f[431:432]', '.f[436:437]', 
                '.f[444:445]', '.f[453]', '.f[455:456]', '.f[348]', '.f[107]', '.f[4:7]', '.f[20:21]', '.f[27:29]', '.f[84:87]', '.f[100:101]', '.f[107:109]', '.f[346:349]', '.f[362:363]', '.f[369:371]', '.f[426:429]', '.f[442:443]', '.f[449:451]', '.f[700]', '.f[684]', '.f[684:700]',
                '.f[381]', '.f[386]', '.f[39:41]', '.f[44]', '.f[59:60]', '.f[68:69]', '.f[71]', '.f[119:121]', '.f[124]', '.f[139:140]', '.f[148:149]', '.f[151]', '.f[381:383]', '.f[386]', '.f[401:402]', '.f[410:411]', '.f[413]', '.f[461:463]', '.f[466]', '.f[481:482]', '.f[490:491]', '.f[493]', '.f[395]', '.f[396]', 
                '.f[48:49]', '.f[53:54]', '.f[63:64]', '.f[75]', '.f[77:78]', '.f[128:129]', '.f[133:134]', '.f[143:144]', '.f[155]', '.f[157:158]', '.f[390:391]', '.f[395:396]', '.f[405:406]', '.f[417]', '.f[419:420]', '.f[470:471]', '.f[475:476]', '.f[485:486]', '.f[497]', '.f[499:500]', '.f[399]', '.f[398]', '.f[51:52]', 
                '.f[56:57]', '.f[66:67]', '.f[76]', '.f[80:81]', '.f[131:132]', '.f[136:137]', '.f[146:147]', '.f[156]', '.f[160:161]', '.f[393:394]', '.f[398:399]', '.f[408:409]', '.f[418]', '.f[422:423]', '.f[473:474]', '.f[478:479]', '.f[488:489]', '.f[498]', '.f[502:503]', '.f[380]', '.f[397]', '.f[0:1]', '.f[38]', 
                '.f[47]', '.f[50]', '.f[55]', '.f[58]', '.f[65]', '.f[74]', '.f[79]', '.f[118]', '.f[127]', '.f[130]', '.f[135]', '.f[138]', '.f[145]', '.f[154]', '.f[159]', '.f[342:343]', '.f[380]', '.f[389]', '.f[392]', '.f[397]', '.f[400]', '.f[407]', '.f[416]', '.f[421]', '.f[460]', '.f[469]', '.f[472]', '.f[477]', 
                '.f[480]', '.f[487]', '.f[496]', '.f[501]', '.f[512]', '.f[513]', '.f[167:168]', '.f[170:171]', '.f[186:187]', '.f[195]', '.f[197:198]', '.f[257:258]', '.f[260:261]', '.f[276:277]', '.f[285]', '.f[287:288]', '.f[509:510]', '.f[512:513]', '.f[528:529]', '.f[537]', '.f[539:540]', '.f[599:600]', '.f[602:603]', 
                '.f[618:619]', '.f[627]', '.f[629:630]']
        else:
            facenums = ['.f[387]', '.f[385]', '.f[42:43]', '.f[45:46]', '.f[61:62]', '.f[70]', '.f[72:73]', '.f[122:123]', '.f[125:126]', '.f[141:142]', '.f[150]', '.f[152:153]', '.f[384:385]', '.f[387:388]', '.f[403:404]', '.f[412]', '.f[414:415]', '.f[464:465]', '.f[467:468]', '.f[483:484]', '.f[492]', '.f[494:495]',
                '.f[353]', '.f[350]', '.f[2:3]', '.f[8]', '.f[11]', '.f[16]', '.f[19]', '.f[24]', '.f[30]', '.f[35]', '.f[82:83]', '.f[88]', '.f[91]', '.f[96]', '.f[99]', '.f[104]', '.f[110]', '.f[115]', '.f[344:345]', '.f[350]', '.f[353]', '.f[358]', '.f[361]', '.f[366]', '.f[372]', '.f[377]', '.f[424:425]', '.f[430]', 
                '.f[433]', '.f[438]', '.f[441]', '.f[446]', '.f[452]', '.f[457]', '.f[355]', '.f[354]', '.f[12:13]', '.f[17:18]', '.f[25:26]', '.f[32]', '.f[36:37]', '.f[92:93]', '.f[97:98]', '.f[105:106]', '.f[112]', '.f[116:117]', '.f[354:355]', '.f[359:360]', '.f[367:368]', '.f[374]', '.f[378:379]', '.f[434:435]', 
                '.f[439:440]', '.f[447:448]', '.f[454]', '.f[458:459]', '.f[352]', '.f[351]', '.f[9:10]', '.f[14:15]', '.f[22:23]', '.f[31]', '.f[33:34]', '.f[89:90]', '.f[94:95]', '.f[102:103]', '.f[111]', '.f[113:114]', '.f[351:352]', '.f[356:357]', '.f[364:365]', '.f[373]', '.f[375:376]', '.f[431:432]', '.f[436:437]', 
                '.f[444:445]', '.f[453]', '.f[455:456]', '.f[348]', '.f[107]', '.f[4:7]', '.f[20:21]', '.f[27:29]', '.f[84:87]', '.f[100:101]', '.f[107:109]', '.f[346:349]', '.f[362:363]', '.f[369:371]', '.f[426:429]', '.f[442:443]', '.f[449:451]', '.f[700]', '.f[684]', '.f[684:700]']
        faces = []
        for face in facenums:
            faces.append(appendName(name, face))
        cmds.select(faces)
        #cmds.sets(forceElement = 'aiSurfaceShader' + name + 'SG')
        cmds.hyperShade(assign = shadingGroup)
        
        #smooth
        cmds.select(name)
        if (smooth == True):
            
            if (layers == True):
                 cmds.duplicate(name, n = inputname + "_HP" + str(x))
                 mushroom = cmds.polySmooth(mth=0, sdt=2, ovb=1, ofb=3, ofc=0, ost=0, ocr=0, dv=2, bnr=1, c=1, kb=1, ksb=1, khe=0, kt=1, kmb=1, suv=1, peh=0, sl=1, dpe=1, ps=0.1, ro=1, ch=1)
                 cmds.editDisplayLayerMembers('LowPoly', name)
                 
                 #setDisplayLayerVis(layer1, False)
                 
                 cmds.editDisplayLayerMembers('HighPoly', inputname + "_HP" + str(x))
                 
                 #setDisplayLayerVis('HighPoly', True)
                 
            else:
                mushroom = cmds.polySmooth(mth=0, sdt=2, ovb=1, ofb=3, ofc=0, ost=0, ocr=0, dv=2, bnr=1, c=1, kb=1, ksb=1, khe=0, kt=1, kmb=1, suv=1, peh=0, sl=1, dpe=1, ps=0.1, ro=1, ch=1)