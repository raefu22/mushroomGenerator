import maya.cmds as cmds
import random
import colorsys

def showColorOp(*args):
    showCheckbox = cmds.checkBoxGrp(applyMaterials, q = True)
    cmds.colorSliderGrp(pickColor, edit=True, enable=True)
    cmds.floatSliderGrp(colorSpread, edit=True, enable=True)
    cmds.checkBoxGrp(addMoss, edit=True, enable=True)
   
def hideColorOp(*args):
    showCheckbox = cmds.checkBoxGrp(applyMaterials, q = True, vis = False, v1 = False)
    cmds.colorSliderGrp(pickColor, edit=True, enable=False)
    cmds.floatSliderGrp(colorSpread, edit=True, enable=False)
    cmds.checkBoxGrp(addMoss, edit=True, enable=False)
    
def showScatter(*args):
    showCheckbox = cmds.checkBoxGrp(useCurve, q = True)
    cmds.floatSliderGrp(locationScatter, edit=True, enable=True)
   
def hideScatter(*args):
    showCheckbox = cmds.checkBoxGrp(useCurve, q = True, vis = False, v1 = False)
    cmds.floatSliderGrp(locationScatter, edit=True, enable=False)

def showMossOp(*args):
    showCheckbox = cmds.checkBoxGrp(addMoss, q = True)
    cmds.floatSliderGrp(mossAmount, edit=True, enable=True)
   
def hideMossOp(*args):
    showCheckbox = cmds.checkBoxGrp(addMoss, q = True, vis = False, v1 = False)
    cmds.floatSliderGrp(mossAmount, edit=True, enable=False)

#UI
window = cmds.window(title='Rock Generator', menuBar = True, width=250)
container = cmds.columnLayout()
cols = cmds.rowLayout(numberOfColumns=3, p=container)

leftmar = cmds.columnLayout(p=cols)
cmds.text('       ', p =leftmar)

maincol = cmds.columnLayout('Block', p=cols)
cmds.text('            ')

cmds.separator(height = 10)
nameparam = cmds.textFieldGrp(label = 'Name ')
cmds.separator(height = 10)
cmds.intSliderGrp("num", label="Number of Rocks ", field = True, min = 1, max = 40, v = 15)
cmds.separator(height = 10)

curveInstructions = cmds.text('                Select an EP Curve or Bezier Curve to place the rocks along?')
cmds.separator(height = 5)
useCurve = cmds.checkBoxGrp('useCurve', numberOfCheckBoxes=1, label='Use Curve ', v1=False, onc = hideScatter, ofc = showScatter)

locationScatter = cmds.floatSliderGrp("spread", label="Location Scatter ", field = True, min = 1, max = 50, v = 20)

cmds.separator(height = 10)
applyMaterials = cmds.checkBoxGrp("applyMaterials", numberOfCheckBoxes=1, label='Apply Materials ', v1=False, onc = showColorOp, ofc = hideColorOp)

cmds.separator(height = 5)
pickColor = cmds.colorSliderGrp('colorpicked', label= 'Color', rgb=(0.272, 0.240, 0.237))
cmds.separator(height = 5)
colorSpread = cmds.floatSliderGrp('colorvariation', label="Color Variation ", field = True, min = 0, max = 10, v = 0.5)

cmds.colorSliderGrp(pickColor, edit=True, enable=False)
cmds.floatSliderGrp(colorSpread, edit=True, enable=False)

cmds.separator(height = 10)
addMoss = cmds.checkBoxGrp("addMoss", numberOfCheckBoxes=1, label='Add Moss ', v1=False, onc = showMossOp, ofc = hideMossOp)
cmds.checkBoxGrp(addMoss, edit=True, enable=False)
cmds.separator(height = 5)
mossAmount = cmds.floatSliderGrp('mossAmount', label="Moss Amount ", field = True, min = 0, max = 10, v = 0.5)

cmds.floatSliderGrp(mossAmount, edit=True, enable=False)

cmds.separator(height = 10)

submitrow = cmds.rowLayout(numberOfColumns=2, p=maincol)
cmds.text(label='                                                                                                    ')
cmds.button(label="Create Rock(s)", c="createRock()", p = submitrow)

cmds.separator(height = 10, p = maincol)
rightmar = cmds.columnLayout(p=cols)
cmds.text('         ', p =rightmar)

cmds.showWindow(window)

def appendName(name, textstring):
    textstring = name + textstring
    return textstring
    
def normalDistrib(mean, std, size):
    numlist = []
    upperlim = mean + std
    otherupperlim = mean - std
    controlnum = int(size*0.341)
    for i in range(controlnum):
        numlist.append(random.uniform(mean, upperlim))
        numlist.append(random.uniform(otherupperlim, mean))
    lowerlim = upperlim
    upperlim = upperlim + std
    otherlowerlim = otherupperlim
    otherupperlim = otherupperlim - std
    if (otherupperlim < 0):
        otherupperlim = 0
    
    controlnum = int(size*0.136)
    for i in range(controlnum):
        numlist.append(random.uniform(lowerlim, upperlim))
        numlist.append(random.uniform(otherupperlim, otherlowerlim))
    lowerlim = upperlim
    upperlim = upperlim + std
    otherlowerlim = otherupperlim
    otherupperlim = otherupperlim - std
    if (otherupperlim < 0):
        otherupperlim = 0
    
    controlnum = int(size*0.021)
    for i in range(controlnum):
        numlist.append(random.uniform(lowerlim, upperlim))
        numlist.append(random.uniform(otherupperlim, otherlowerlim))
    
    while (len(numlist) < size):
        if (len(heightlist) == (size - 1)):
            sum = 0
            for h in range(len(numlist)):
                sum = sum + numlist[h]
            numlist.append((mean * size) - sum)
        else:
            upperlim = upperlim + std
            numlist.append(random.uniform(mean, upperlim))
            
    return numlist
    
def randomfloat():
    return 1
    
def locations(curvename, level):
    position = cmds.pointOnCurve(curvename, pr = level, turnOnPercentage = True)
    return position
    
def randomLocation(size, spread):
    singleCoordinates = normalDistrib(200, spread, size)
    for i in range(len(singleCoordinates)):
        singleCoordinates[i] = singleCoordinates[i] - 200
    random.shuffle(singleCoordinates)
    return singleCoordinates
    
#main function    
def createRock():
    inputname = cmds.textFieldGrp(nameparam, query = True, text = True)
   
    num = cmds.intSliderGrp("num", q = True, v=True)
    spread = cmds.floatSliderGrp("spread", q = True, v = True)
    
    applyMaterials = cmds.checkBoxGrp('applyMaterials', q = True, v1=True)
    maincolor = cmds.colorSliderGrp('colorpicked', q = True, rgbValue = True)
    colorvariation = cmds.floatSliderGrp('colorvariation', q = True, v = True)
    colorvariation = colorvariation/20
    curvename = cmds.ls(selection = True)
    
    addMossMaterial= cmds.checkBoxGrp('addMoss', q = True, v1=True)
    mossSpread = cmds.floatSliderGrp('mossAmount', q = True, v = True)
    for x in range(1, num+1):
        #obj name
        name = inputname + str(x)
        
        #basic rock shape
        width = random.randint(1,3)
        depth = random.randint(1,3)
        cmds.polyCube(w = width, d = depth, cuv=4, sd = 3, sh = 3, sw = 3, n = name)
        
        cmds.select(appendName(name, '.f[4]'), appendName(name, '.f[1]'))
        cmds.move(0, 0, random.uniform(0,1), r=True)
        cmds.select(appendName(name, '.f[22]'), appendName(name, '.f[25]'))
        cmds.move(0, 0, -random.uniform(0,1), r=True)
        
        cmds.select(appendName(name, '.f[37]'), appendName(name, '.f[40]'))
        if (width == 1 and depth == 1):
            cmds.move(random.uniform(0,0.04), 0, 0, r=True)
            cmds.select(appendName(name, '.f[49]'), appendName(name, '.f[46]'))
            cmds.move(-random.uniform(0,0.03), 0, 0, r=True)
            cmds.select(appendName(name, '.f[13]'))
            cmds.move(random.uniform(-0.2,0.2), random.uniform(0,0.03), random.uniform(-0.2,.2), r=True)
        else:
            cmds.move(random.uniform(0,0.5), 0, 0, r=True)
            cmds.select(appendName(name, '.f[49]'), appendName(name, '.f[46]'))
            cmds.move(-random.uniform(0,1), 0, 0, r=True)
            cmds.select(appendName(name, '.f[13]'))
            cmds.move(random.uniform(-0.2,0.2), random.uniform(0,1), random.uniform(-0.2,.2), r=True)
       
        #tweaks
        cmds.select(appendName(name, '.vtx[15]'))
        cmds.move(random.uniform(-.2,-0.01), 0, random.uniform(-0.2,-0.01), r=True)
        cmds.select(appendName(name, '.vtx[12]'))
        cmds.move(random.uniform(0.01, 0.2), 0, random.uniform(-0.2,-0.01), r=True)
        cmds.select(appendName(name, '.vtx[27]'))
        cmds.move(random.uniform(-0.2, -0.01), 0, random.uniform(0.01,0.2), r=True)
        cmds.select(appendName(name, '.vtx[24]'))
        cmds.move(random.uniform(0.01, 0.2), 0, random.uniform(0.01,0.2), r=True)
        
        #rotate
        cmds.select(name)
        degrees = str(random.uniform(0, 360)) + 'deg'
        cmds.rotate(0, degrees, 0, r=True)
        
        #location
        cmds.select(name)
        position = locations(curvename, (x-0.0)/num)
        cmds.move(position[0], position[1], position[2], relative = True)
        
        #UVs
        cmds.polyProjection(name+".f[0:53]", md = 'y')
        
        edgenums = ['.e[0:2]', '.e[27:29]', '.e[72]', '.e[75:76]', '.e[79:80]', '.e[83]', '.e[37]', '.e[41]', '.e[45]']   
        edges = []
        for edge in edgenums:
            edges.append(appendName(name,edge))
        
        cmds.polyMapCut(edges)
        cmds.select(name + '.f[0:53]')
        cmds.u3dUnfold(name + '.f[0:53]', ite=1, p=0, bi=1, tf=1, ms=1024, rs=0)
        cmds.u3dLayout(name+'.f[0:53]', res=256, scl=1, box=[0, 1, 0, 1])
        
        #material
        if (applyMaterials == True):
            
            shader = cmds.shadingNode('aiStandardSurface', asShader = True, n=name + 'shader')
            
            cmds.sets(renderable=True, noSurfaceShader= True, empty=True, n= 'aiSurfaceShader' + name + 'SG')
            cmds.select(name)
            cmds.hyperShade(assign = 'aiSurfaceShader' + name + 'SG')
            cmds.connectAttr(name + 'shader.outColor', 'aiSurfaceShader' + name +'SG.surfaceShader', f=True)
            
            #initial noise
            cmds.shadingNode('noise', asTexture=True, n = name + 'noise1')
            
            cmds.shadingNode('place2dTexture', asUtility = True, n = name + 'place2dTexture1')
            cmds.connectAttr (name + 'place2dTexture1.outUV', name + 'noise1.uv')
            cmds.connectAttr(name + 'place2dTexture1.outUvFilterSize', name + 'noise1.uvFilterSize')
            
            cmds.shadingNode('simplexNoise', asTexture=True, n = name + 'simplexNoise1')
            cmds.shadingNode('place2dTexture', asUtility=True, n = name + 'place2dTexture2')
            cmds.connectAttr(name + 'place2dTexture2.outUV', name + 'simplexNoise1.uv')
            cmds.connectAttr(name +'place2dTexture2.outUvFilterSize', name + 'simplexNoise1.uvFilterSize')
            cmds.connectAttr(name + 'simplexNoise1.outColor', name + 'noise1.colorOffset', force=True)
            
            cmds.shadingNode('aiMultiply', asUtility=True, n = name + 'aiMultiply1')
            cmds.connectAttr(name + 'noise1.outColor', name + 'aiMultiply1.input1', force = True)
            
            cmds.shadingNode('noise', asTexture=True, n = name + 'noiseColor')
            cmds.shadingNode('place2dTexture', asUtility = True, n = name + 'place2dTexture3')
            cmds.connectAttr (name + 'place2dTexture3.outUV', name + 'noiseColor.uv')
            cmds.connectAttr(name + 'place2dTexture3.outUvFilterSize', name + 'noiseColor.uvFilterSize')
            cmds.connectAttr(name + 'noiseColor.outColor', name + 'aiMultiply1.input2', force = True)
            
            #mountain texture
            cmds.shadingNode('mountain', asTexture=True, n = name + 'mountain1')
            cmds.shadingNode('place2dTexture', asUtility=True, n = name + 'place2dTexture4')
            cmds.connectAttr(name + 'place2dTexture4.outUV', name + 'mountain1.uv')
            cmds.connectAttr(name + 'place2dTexture4.outUvFilterSize', name + 'mountain1.uvFilterSize')
            
            cmds.shadingNode('fractal', asTexture=True, n = name + 'fractal1') 
            cmds.shadingNode('place2dTexture', asUtility=True, n=name + 'place2dTexture5')
            cmds.connectAttr(name + 'place2dTexture5.outUV', name + 'fractal1.uv')
            cmds.connectAttr(name + 'place2dTexture5.outUvFilterSize', name + 'fractal1.uvFilterSize')
            cmds.shadingNode('aiAdd', asUtility=True, n = name + 'aiAdd1')
            cmds.connectAttr(name + 'mountain1.outColor', name + 'aiAdd1.input1', force = True)
            cmds.connectAttr(name + 'fractal1.outColor', name + 'aiAdd1.input2', force = True)
            
            cmds.shadingNode('aiMultiply', asUtility=True, n = name + 'aiMultiply2')
            cmds.connectAttr(name + 'aiMultiply1.outColor', name + 'aiMultiply2.input1', force = True)
            cmds.connectAttr(name + 'aiAdd1.outColor', name + 'aiMultiply2.input2', force = True)
            cmds.connectAttr(name + 'aiMultiply2.outColor', name + 'shader.baseColor', force = True)
            
            cmds.shadingNode('layeredTexture', asTexture=True, n = name + 'layeredTextureMaster') 
            cmds.connectAttr(name + 'aiMultiply2.outColor', name + 'layeredTextureMaster.inputs[0].color', force = True)
            cmds.shadingNode('luminance', asUtility=True, n = name + 'luminance1')
            cmds.connectAttr(name + 'layeredTextureMaster.outColor', name + 'luminance1.value', force = True)
            
            cmds.shadingNode('bump2d', asUtility=True, n = name + 'bump2d1')
            cmds.connectAttr(name + 'luminance1.outValue', name + 'bump2d1.bumpValue', f = True)
            cmds.connectAttr(name + 'bump2d1.outNormal', name + 'shader.normalCamera')
            
            cmds.shadingNode('contrast', asUtility=True, n = name + 'roughnessContrast')
            cmds.connectAttr(name + 'luminance1.outValue', name + 'roughnessContrast.valueX', f = True)
            cmds.connectAttr(name + 'luminance1.outValue', name + 'roughnessContrast.valueY', f = True)
            cmds.connectAttr(name + 'luminance1.outValue', name + 'roughnessContrast.valueZ', f = True)
            cmds.connectAttr(name + 'roughnessContrast.outValueX', name + 'shader.diffuseRoughness', force = True)
            cmds.connectAttr(name + 'roughnessContrast.outValueX', name + 'shader.specularRoughness', force = True)
            
            cmds.connectAttr(name + 'layeredTextureMaster.outColor', name + 'shader.baseColor', force = True)
            
            #adjustments
            cmds.setAttr(name + 'noise1.amplitude', 0.42)
            cmds.setAttr(name + 'noise1.ratio', 1.0)
            cmds.setAttr(name + 'noise1.frequencyRatio', random.uniform(29.636, 96))
            cmds.setAttr(name + 'noise1.frequency', random.uniform(88, 99))
            cmds.setAttr(name + 'noise1.density', 1.0)
            cmds.setAttr(name + 'noise1.spottyness', 0)
            cmds.setAttr(name + 'noise1.sizeRand', random.uniform(0,1))
            cmds.setAttr(name + 'noise1.randomness', 1.0)
            cmds.setAttr(name + 'noise1.colorGain',  0.804, 0.771, 0.763, type='double3')
            cmds.setAttr(name + 'noise1.alphaGain', 0.392)
            
            cmds.setAttr(name + 'simplexNoise1.amplitude', random.uniform(0.01, 0.7))
            cmds.setAttr(name + 'simplexNoise1.threshold', 0.0)
            cmds.setAttr(name + 'simplexNoise1.ratio', 0.707)
            cmds.setAttr(name + 'simplexNoise1.frequency', 6.853)
            cmds.setAttr(name + 'simplexNoise1.frequencyRatio', 1.0)
            cmds.setAttr(name + 'simplexNoise1.gamma', .455)
            if (random.uniform(0,1) < 0.2):
                cmds.setAttr(name + 'simplexNoise1.noiseType', 2)
                cmds.setAttr(name + 'simplexNoise1.scale', random.uniform(0,6.3))
            else:
                cmds.setAttr(name + 'simplexNoise1.scale', random.uniform(0,10))
                
            cmds.setAttr(name + 'noiseColor.amplitude', random.uniform(0.182, 1))
            cmds.setAttr(name + 'noiseColor.ratio', 0.643)
            cmds.setAttr(name + 'noiseColor.frequencyRatio', 1.566)
            cmds.setAttr(name + 'noiseColor.frequency', 9.091)
            cmds.setAttr(name + 'noiseColor.noiseType', 4)
            cmds.setAttr(name + 'noiseColor.colorGain', 0.712, 0.712, 0.712, type='double3')
            
            hsv = colorsys.rgb_to_hsv(maincolor[0], maincolor[1], maincolor[2])
            hue = hsv[0] + random.uniform(-colorvariation/2, colorvariation/2)
            rgb = colorsys.hsv_to_rgb(hue, hsv[1], hsv[2])
            
            cmds.setAttr(name + 'noiseColor.colorOffset', rgb[0], rgb[1], rgb[2], type='double3')
            cmds.setAttr(name + 'noiseColor.alphaGain', 1.0)
            
            cmds.setAttr(name + 'mountain1.snowColor', 1, 1, 1, type='double3')
            cmds.setAttr(name + 'mountain1.rockColor', 0.503, 0.503, 0.503, type='double3')
            cmds.setAttr(name + 'mountain1.amplitude', 1.0)
            cmds.setAttr(name + 'mountain1.snowRoughness', 0.4)
            cmds.setAttr(name + 'mountain1.rockRoughness', 0.707)
            cmds.setAttr(name + 'mountain1.boundary', random.uniform(0.874,1))
            cmds.setAttr(name + 'mountain1.snowAltitude', random.uniform(0, 0.5))
            cmds.setAttr(name + 'mountain1.snowDropoff', random.uniform(0, 2.0))
            cmds.setAttr(name + 'mountain1.snowSlope', random.uniform(0, 3.0))
            cmds.setAttr(name + 'mountain1.colorOffset', 0.041958, 0.041958, 0.041958, type='double3')
            
            cmds.setAttr(name + 'fractal1.amplitude', 1.0)
            cmds.setAttr(name + 'fractal1.threshold', 0.0)
            cmds.setAttr(name + 'fractal1.ratio', 0.972)
            cmds.setAttr(name + 'fractal1.frequencyRatio', random.uniform(2.0, 3.4))
            cmds.setAttr(name + 'fractal1.bias', 0.636)
            cmds.setAttr(name + 'fractal1.colorOffset', 0.13986, 0.13986, 0.13986, type='double3')
            
            '''
            #for normal map
            cmds.shadingNode('layeredTexture', asTexture=True, n = name + 'layeredTexture1') 
            cmds.setAttr(name + 'layeredTexture1.inputs[0].color', 0.523, 0.523, 0.523, type="double3")
            cmds.setAttr(name + 'layeredTexture1.inputs[0].alpha', 1)
            cmds.setAttr(name + 'layeredTexture1.inputs[0].blendMode', 6)
            cmds.connectAttr(name + 'mountain1.outAlpha', name + 'layeredTexture1.inputs[0].alpha', force = True)
            cmds.setAttr(name + 'mountain1.alphaIsLuminance', 1)
            cmds.setAttr(name + 'layeredTexture1.alphaIsLuminance', 1)
            cmds.setAttr(name + 'layeredTexture1.inputs[1].color', 0.242, 0.242, 0.242, type="double3")
            cmds.setAttr(name + 'layeredTexture1.inputs[1].alpha', 1)
            cmds.setAttr(name + 'layeredTexture1.inputs[1].blendMode', 4)
            
            cmds.connectAttr(name + 'fractal1.outAlpha', name + 'layeredTexture1.inputs[1].alpha', force = True)
            cmds.setAttr(name + 'fractal1.alphaIsLuminance', 1)
           
            cmds.shadingNode('bump2d', asUtility=True, n = name + 'bump2d1')
            cmds.connectAttr(name + 'layeredTexture1.outAlpha', name + 'bump2d1.bumpValue', f = True)
            cmds.connectAttr(name + 'bump2d1.outNormal', name + 'shader.normalCamera')
            '''        
     
            #moss
            if (addMossMaterial == True):
                cmds.shadingNode('fractal', asTexture=True, n = name + 'mossFractal1') 
                cmds.shadingNode('place2dTexture', asUtility=True, n=name + 'place2dTexture6')
                cmds.connectAttr(name + 'place2dTexture6.outUV', name + 'mossFractal1.uv')
                cmds.connectAttr(name + 'place2dTexture6.outUvFilterSize', name + 'mossFractal1.uvFilterSize')
                
                cmds.shadingNode('aiMultiply', asUtility=True, n = name + 'aiMultiply3')
                cmds.connectAttr(name + 'mossFractal1.outColor', name + 'aiMultiply3.input1', force = True)
                
                cmds.shadingNode('noise', asTexture=True, n = name + 'mossColor')
                cmds.shadingNode('place2dTexture', asUtility = True, n = name + 'place2dTexture7')
                cmds.connectAttr (name + 'place2dTexture7.outUV', name + 'mossColor.uv')
                cmds.connectAttr(name + 'place2dTexture7.outUvFilterSize', name + 'mossColor.uvFilterSize')
                cmds.connectAttr(name + 'mossColor.outColor', name + 'aiMultiply3.input2', force = True)
                
                cmds.shadingNode('aiMultiply', asUtility=True, n = name + 'aiMultiply4')
                cmds.connectAttr(name + 'aiMultiply3.outColor', name + 'aiMultiply4.input1', force = True)
                
                cmds.shadingNode('simplexNoise', asTexture=True, n = name + 'mossSimplexNoise1')
                cmds.shadingNode('place2dTexture', asUtility=True, n = name + 'place2dTexture8')
                cmds.connectAttr(name + 'place2dTexture8.outUV', name + 'mossSimplexNoise1.uv')
                cmds.connectAttr(name +'place2dTexture8.outUvFilterSize', name + 'mossSimplexNoise1.uvFilterSize')
                
                cmds.shadingNode('reverse', asUtility=True, n = name + 'reverse1')
                cmds.connectAttr(name + 'mossSimplexNoise1.outColor', name + 'reverse1.input')
                cmds.shadingNode('contrast', asUtility=True, n = name + 'contrast1')
                cmds.connectAttr(name + 'reverse1.output', name + 'contrast1.value')
                cmds.shadingNode('aiAdd', asUtility=True, n = name + 'aiAdd2')
                cmds.connectAttr(name + 'contrast1.outValue', name + 'aiAdd2.input1')
                
                cmds.shadingNode('simplexNoise', asTexture=True, n = name + 'mossSimplexNoise2')
                cmds.shadingNode('place2dTexture', asUtility=True, n = name + 'place2dTexture9')
                cmds.connectAttr(name + 'place2dTexture9.outUV', name + 'mossSimplexNoise2.uv')
                cmds.connectAttr(name +'place2dTexture9.outUvFilterSize', name + 'mossSimplexNoise2.uvFilterSize')
                
                cmds.shadingNode('reverse', asUtility=True, n = name + 'reverse2')
                cmds.connectAttr(name + 'mossSimplexNoise2.outColor', name + 'reverse2.input')
                cmds.shadingNode('contrast', asUtility=True, n = name + 'contrast2')
                cmds.connectAttr(name + 'reverse2.output', name + 'contrast2.value')
                cmds.connectAttr(name + 'contrast2.outValue', name + 'aiAdd2.input2')
                
                cmds.shadingNode('fractal', asTexture=True, n = name + 'mossFractal2') 
                cmds.shadingNode('place2dTexture', asUtility=True, n=name + 'place2dTexture10')
                cmds.connectAttr(name + 'place2dTexture10.outUV', name + 'mossFractal2.uv')
                cmds.connectAttr(name + 'place2dTexture10.outUvFilterSize', name + 'mossFractal2.uvFilterSize')
                cmds.shadingNode('contrast', asUtility=True, n = name + 'contrast3')
                cmds.connectAttr(name + 'mossFractal2.outColor', name + 'contrast3.value')
                cmds.shadingNode('aiMax', asUtility=True, n = name + 'aiMax1')
                cmds.connectAttr(name + 'aiAdd2.outColor', name + 'aiMax1.input1')
                cmds.connectAttr(name + 'contrast3.outValue', name + 'aiMax1.input2')
                cmds.connectAttr(name + 'aiMax1.outColor', name + 'aiMultiply4.input2', force = True)
                
                cmds.connectAttr(name + 'aiMultiply2.outColor', name + 'layeredTextureMaster.inputs[1].color', force = True)
                cmds.shadingNode('noise', asTexture=True, n = name + 'mossMask')
                cmds.shadingNode('place2dTexture', asUtility = True, n = name + 'place2dTexture11')
                cmds.connectAttr (name + 'place2dTexture11.outUV', name + 'mossMask.uv')
                cmds.connectAttr(name + 'place2dTexture11.outUvFilterSize', name + 'mossMask.uvFilterSize')
                cmds.connectAttr(name + 'mossMask.outColor.outColorR', name + 'layeredTextureMaster.inputs[0].alpha', force = True)
                cmds.connectAttr(name + 'aiMultiply4.outColor', name + 'layeredTextureMaster.inputs[0].color', force = True)
                
                '''
                cmds.setAttr(name + 'layeredTextureMaster.inputs[0].color', 0.523, 0.523, 0.523, type="double3")
                cmds.setAttr(name + 'layeredTextureMaster.inputs[0].alpha', 1)
                cmds.setAttr(name + 'layeredTextureMaster.inputs[0].blendMode', 6)
                cmds.connectAttr(name + 'bump2d1.outNormal', name + 'shader.normalCamera')
                '''
                
                #adjustments
                
                cmds.setAttr(name + 'mossFractal1.amplitude', 1)
                cmds.setAttr(name + 'mossFractal1.ratio', 0.707)
                cmds.setAttr(name + 'mossFractal1.frequencyRatio', 3.077)
                cmds.setAttr(name + 'mossFractal1.colorGain', 0.75, 0.8, 0.7, type='double3') #strange values when looking , 
                cmds.setAttr(name + 'mossFractal1.colorOffset', 0.156, 0.174, 0.133, type='double3')
                
                cmds.setAttr(name + 'mossColor.amplitude', 1)
                cmds.setAttr(name + 'mossColor.ratio', 0.923)
                cmds.setAttr(name + 'mossColor.frequencyRatio', 0.923)
                cmds.setAttr(name + 'mossColor.frequency', 8)
                cmds.setAttr(name + 'mossColor.noiseType', 4)
                cmds.setAttr(name + 'mossColor.numWaves', 5)
                cmds.setAttr(name + 'mossColor.colorGain', 0.172, 0.199, 0.062, type='double3')
                cmds.setAttr(name + 'mossColor.colorOffset', 0.046, 0.049, 0.044, type='double3')
                 
                cmds.setAttr(name + 'mossSimplexNoise1.scale', 39.434) 
                cmds.setAttr(name + 'mossSimplexNoise1.amplitude', 0.806)
                cmds.setAttr(name + 'mossSimplexNoise1.ratio', 0.707)
                cmds.setAttr(name + 'mossSimplexNoise1.octaves', 3)
                cmds.setAttr(name + 'mossSimplexNoise1.frequency', 9.606)
                cmds.setAttr(name + 'mossSimplexNoise1.frequencyRatio', 1)
                cmds.setAttr(name + 'mossSimplexNoise1.noiseType', 1)
                
                cmds.setAttr(name + 'contrast1.contrastX', 3)
                cmds.setAttr(name + 'contrast1.contrastY', 3)
                cmds.setAttr(name + 'contrast1.contrastZ', 3)
                cmds.setAttr(name + 'contrast1.biasX', 0.5)
                cmds.setAttr(name + 'contrast1.biasY', 0.5)
                cmds.setAttr(name + 'contrast1.biasZ', 0.5)
                
                cmds.setAttr(name + 'mossSimplexNoise2.scale', 67.158) 
                cmds.setAttr(name + 'mossSimplexNoise2.amplitude', 0.806)
                cmds.setAttr(name + 'mossSimplexNoise2.ratio', 0.707)
                cmds.setAttr(name + 'mossSimplexNoise2.octaves', 1)
                cmds.setAttr(name + 'mossSimplexNoise2.frequency', 9.606)
                cmds.setAttr(name + 'mossSimplexNoise2.frequencyRatio', 1)
                cmds.setAttr(name + 'mossSimplexNoise2.noiseType', 1)
                
                cmds.setAttr(name + 'contrast2.contrastX', 4)
                cmds.setAttr(name + 'contrast2.contrastY', 4)
                cmds.setAttr(name + 'contrast2.contrastZ', 4)
                cmds.setAttr(name + 'contrast2.biasX', 0.5)
                cmds.setAttr(name + 'contrast2.biasY', 0.5)
                cmds.setAttr(name + 'contrast2.biasZ', 0.5)
                
                cmds.setAttr(name + 'mossFractal2.amplitude', 1)
                cmds.setAttr(name + 'mossFractal2.ratio', 0.776)
                cmds.setAttr(name + 'mossFractal2.frequencyRatio', 7.545)
                cmds.setAttr(name + 'mossFractal2.levelMin', 25)
                cmds.setAttr(name + 'mossFractal2.levelMax', 8.939)
                cmds.setAttr(name + 'mossFractal2.bias', -0.139)
                cmds.setAttr(name + 'mossFractal2.alphaIsLuminance', 1)
                
                cmds.setAttr(name + 'contrast3.contrastX', 5)
                cmds.setAttr(name + 'contrast3.contrastY', 5)
                cmds.setAttr(name + 'contrast3.contrastZ', 5)
                cmds.setAttr(name + 'contrast3.biasX', 0.5)
                cmds.setAttr(name + 'contrast3.biasY', 0.5)
                cmds.setAttr(name + 'contrast3.biasZ', 0.5)
                
                cmds.setAttr(name + 'layeredTextureMaster.inputs[0].blendMode', 1)
                
                cmds.setAttr(name + 'roughnessContrast.contrastX', 0.2)
                cmds.setAttr(name + 'roughnessContrast.contrastY', 0.2)
                cmds.setAttr(name + 'roughnessContrast.contrastZ', 0.2)
                cmds.setAttr(name + 'roughnessContrast.biasX', 0.02)
                cmds.setAttr(name + 'roughnessContrast.biasY', 0.02)
                cmds.setAttr(name + 'roughnessContrast.biasZ', 0.02)
                
        #smooth
        cmds.select(name)
        cmds.polySmooth(mth=0, sdt=2, ovb=1, ofb=3, ofc=0, ost=0, ocr=0, dv=2, bnr=1, c=1, kb=1, ksb=1, khe=0, kt=1, kmb=1, suv=1, peh=0, sl=1, dpe=1, ps=0.1, ro=1, ch=1)
