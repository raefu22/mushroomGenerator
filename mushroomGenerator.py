import maya.cmds as cmds
import random

#UI
window = cmds.window(title="Mushroom Generator", menuBar = True, width=200)
cmds.columnLayout("Block")
cmds.intSliderGrp("num", label="Number of Mushrooms", field = True, min = 1, max = 20, v = 4)
cmds.intSliderGrp("height", label="Average Height", field = True, min = 1, max = 15, v = 4)
cmds.floatSliderGrp("heightstd", label="Height Standard Deviation", field = True, min = 0.5, max = 8, v = 1)
cmds.intSliderGrp("bend", label="Average Bend", field = True, min = 0, max = 10, v = 2)
cmds.floatSliderGrp("bendstd", label="Bend Standard Deviation", field = True, min = 0.1, max = 10, v = 0.5)

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
        coordinates.append(random.uniform(-10, 25))
    return coordinates
    
def createMushroom():
    
    num = cmds.intSliderGrp("num", q = True, v=True)
    height = cmds.intSliderGrp("height", q = True, v=True)
    heightstd = cmds.floatSliderGrp("heightstd", q = True, v=True)
    
    bend = cmds.intSliderGrp("bend", q = True, v=True)
    bendstd = cmds.floatSliderGrp("bendstd", q = True, v=True)
    bend = bend * 10
    bendstd = bendstd*10
    
    #random
    heightlist = normalDistrib(height, heightstd, num)  
    bendlist = normalDistrib(bend, bendstd, num)  
    
    for x in range(1, num+1):
        #obj name
        name = "mushroom" + str(x)

        addheight = heightlist[x - 1]

        #basic mushroom
        outline = cmds.curve(bezier=True, d=3, p=[(0.034739, 4.932942+addheight, 0), (0.034739, 4.932942+addheight, 0), (8.812134, 5.859316+addheight, 0), (9.043727, 3.242309+addheight, 0), (9.275321, 0.625303+addheight, 0), (11.938646, 1.019012+addheight, 0), (9.66903, -0.741099+addheight, 0), (7.399413, -2.50121+addheight, 0), (6.959385, -1.389561+addheight, 0), (5.662462, -1.389561+addheight, 0), (4.365538, -1.389561+addheight, 0), (2.837021, -0.764259+addheight, 0), (2.582268, -1.78327+addheight, 0), (2.327515, -2.802282+addheight, 0), (2.744383, -3.149672+addheight, 0), (2.813861, -4.377118+addheight, 0), (2.883339, -5.604563, 0), (3.739306, -6.846439, 0), (2.675708, -7.366924, 0), (1.61211, -7.887408, 0), (0.0053979, -7.729, 0), (0.0053979, -7.729, 0)], k=[0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7]) 
        mushroom = cmds.revolve(outline, ch=1, po=1, rn=0, ssw=0, esw=360, ut=0, tol=0.01, degree=3, s=12, ulp=1, ax=(0, 1, 0), n=name)
        
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
        
        cmds.scaleComponents(0.8, 1, 0.8, edges)
        
        #soften
        cmds.polySoftEdge(a = 180)
        
        #bend
        
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
     
     
        #smooth
        cmds.select(name)
        mushroom = cmds.polySmooth(mth=0, sdt=2, ovb=1, ofb=3, ofc=0, ost=0, ocr=0, dv=2, bnr=1, c=1, kb=1, ksb=1, khe=0, kt=1, kmb=1, suv=1, peh=0, sl=1, dpe=1, ps=0.1, ro=1, ch=1)
        
        #move
        coordinates = randomLocation()
        
        cmds.move(coordinates[0], relative = True, moveX = True)
        cmds.move(coordinates[1], relative = True, moveZ = True)