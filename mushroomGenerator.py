import maya.cmds as cmds

#basic mushroom
outline = cmds.curve(bezier=True, d=3, p=[(0.034739, 4.932942, 0), (0.034739, 4.932942, 0), (8.812134, 5.859316, 0), (9.043727, 3.242309, 0), (9.275321, 0.625303, 0), (11.938646, 1.019012, 0), (9.66903, -0.741099, 0), (7.399413, -2.50121, 0), (6.959385, -1.389561, 0), (5.662462, -1.389561, 0), (4.365538, -1.389561, 0), (2.837021, -0.764259, 0), (2.582268, -1.78327, 0), (2.327515, -2.802282, 0), (2.744383, -3.149672, 0), (2.813861, -4.377118, 0), (2.883339, -5.604563, 0), (3.739306, -6.846439, 0), (2.675708, -7.366924, 0), (1.61211, -7.887408, 0), (0.0053979, -7.729, 0), (0.0053979, -7.729, 0)], k=[0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7]) 
mushroom = cmds.revolve(outline, ch=1, po=1, rn=0, ssw=0, esw=360, ut=0, tol=0.01, degree=3, s=12, ulp=1, ax=(0, 1, 0), n="mushroom")
mushroom = cmds.polyNormal(mushroom, normalMode=0, userNormalMode=1, ch=1, n="mushroom")
cmds.delete(outline)

#retopo top of mushroom to get rid of the triangles
#delete faces
faces = ['mushroom.f[99]', 'mushroom.f[101]', 'mushroom.f[102]', 'mushroom.f[117]', 'mushroom.f[118]', 'mushroom.f[126]', 'mushroom.f[128]', 'mushroom.f[129]', 'mushroom.f[386]', 'mushroom.f[389]', 'mushroom.f[387]', 'mushroom.f[390]', 'mushroom.f[406]', 'mushroom.f[405]', 'mushroom.f[414]', 'mushroom.f[417]', 'mushroom.f[416]', 'mushroom.f[475]', 'mushroom.f[476]', 'mushroom.f[478]', 'mushroom.f[478]', 'mushroom.f[479]', 'mushroom.f[478]', 'mushroom.f[494]', 'mushroom.f[495]', 'mushroom.f[503]', 'mushroom.f[505]', 'mushroom.f[506]', 'mushroom.f[9]', 'mushroom.f[10]', 'mushroom.f[12]', 'mushroom.f[13]', 'mushroom.f[28]',  'mushroom.f[29]', 'mushroom.f[37]', 'mushroom.f[39]', 'mushroom.f[40]', 'mushroom.f[98]']
cmds.polyDelFacet(*faces)
#create new faces
cmds.polyBridgeEdge('mushroom.e[86]', 'mushroom.e[209]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[84]', 'mushroom.e[207]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[65]', 'mushroom.e[211]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[69]', 'mushroom.e[203]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[26]', 'mushroom.e[241]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[36]', 'mushroom.e[239]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[30]', 'mushroom.e[256]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[34]', 'mushroom.e[258]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[251]', 'mushroom.e[992]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[785]', 'mushroom.e[999]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[783]', 'mushroom.e[997]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[787]', 'mushroom.e[981]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[779]', 'mushroom.e[983]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[817]', 'mushroom.e[945]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[815]', 'mushroom.e[953]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[832]', 'mushroom.e[949]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[834]', 'mushroom.e[951]', dv = 0)

#retopo bottom of mushroom to get rid of triangles
#delete faces
faces = ['mushroom.f[358]', 'mushroom.f[353]', 'mushroom.f[347]', 'mushroom.f[350]', 'mushroom.f[308]', 'mushroom.f[329]', 'mushroom.f[321]', 'mushroom.f[324]', 'mushroom.f[164]', 'mushroom.f[260]', 'mushroom.f[255]', 'mushroom.f[252]', 'mushroom.f[249]', 'mushroom.f[210]', 'mushroom.f[210]', 'mushroom.f[249]', 'mushroom.f[252]', 'mushroom.f[231]', 'mushroom.f[223]', 'mushroom.f[226]', 'mushroom.f[0]', 'mushroom.f[712]', 'mushroom.f[717]', 'mushroom.f[706]', 'mushroom.f[709]', 'mushroom.f[667]', 'mushroom.f[688]', 'mushroom.f[680]', 'mushroom.f[683]', 'mushroom.f[523]', 'mushroom.f[619]', 'mushroom.f[614]', 'mushroom.f[608]', 'mushroom.f[611]', 'mushroom.f[569]', 'mushroom.f[590]', 'mushroom.f[582]', 'mushroom.f[585]', 'mushroom.f[1]']
cmds.polyDelFacet(*faces)

#create faces
cmds.polyBridgeEdge('mushroom.e[540]', 'mushroom.e[663]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[532]', 'mushroom.e[658]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[524]', 'mushroom.e[670]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[529]', 'mushroom.e[633]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[449]', 'mushroom.e[708]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[491]', 'mushroom.e[703]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[477]', 'mushroom.e[711]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[483]', 'mushroom.e[719]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[0]', 'mushroom.e[1]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[1176]', 'mushroom.e[1402]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[1171]', 'mushroom.e[1395]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[1183]', 'mushroom.e[1387]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[1146]', 'mushroom.e[1392]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[1221]', 'mushroom.e[1320]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[1216]', 'mushroom.e[1357]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[1224]', 'mushroom.e[1345]', dv = 0)
cmds.polyBridgeEdge('mushroom.e[1232]', 'mushroom.e[1350]', dv = 0)

#scale down top faces
cmds.scaleComponents(0.8, 1, 0.8, 'mushroom.e[20]', 'mushroom.e[24]', 'mushroom.e[28]', 'mushroom.e[30]', 'mushroom.e[59]', 'mushroom.e[63]', 'mushroom.e[73]', 'mushroom.e[78]', 'mushroom.e[80]', 'mushroom.e[197]', 'mushroom.e[201]', 'mushroom.e[203]', 'mushroom.e[205]', 'mushroom.e[233]', 'mushroom.e[235]', 'mushroom.e[245]', 'mushroom.e[250]', 'mushroom.e[252]', 'mushroom.e[740]', 'mushroom.e[744]', 'mushroom.e[746]', 'mushroom.e[748]', 'mushroom.e[776]', 'mushroom.e[778]', 'mushroom.e[790]', 'mushroom.e[793]', 'mushroom.e[795]', 'mushroom.e[906]', 'mushroom.e[910]', 'mushroom.e[912]', 'mushroom.e[914]', 'mushroom.e[942]', 'mushroom.e[944]', 'mushroom.e[953]', 'mushroom.e[958]', 'mushroom.e[960]')

#soften
cmds.polySoftEdge(a = 180)

#smooth
#mushroom = cmds.polySmooth(mth=0, sdt=2, ovb=1, ofb=3, ofc=0, ost=0, ocr=0, dv=2, bnr=1, c=1, kb=1, ksb=1, khe=0, kt=1, kmb=1, suv=1, peh=0, sl=1, dpe=1, ps=0.1, ro=1, ch=1)