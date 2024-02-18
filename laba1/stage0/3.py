import gmsh
import sys

gmsh.initialize()
gmsh.model.add("t1")
lc = 1e-2

'''
1st circlewith area
'''
gmsh.model.geo.addPoint(0, 0, 0, lc, 1)
gmsh.model.geo.addPoint(.1, 0, 0, lc, 2)
gmsh.model.geo.addPoint(0.2, 0, 0, lc, 3)

c1 = gmsh.model.geo.addCircleArc(1, 2, 3)
c2 = gmsh.model.geo.addCircleArc(3, 2, 1)

# gmsh.model.geo.addCurveLoop([c1,c2], 1)
# gmsh.model.geo.addPlaneSurface([1], 1)


'''
2nd circlewith area
'''
gmsh.model.geo.addPoint(0, 0, 0.4, lc, 4)
gmsh.model.geo.addPoint(.1, 0, 0.4, lc, 5)
gmsh.model.geo.addPoint(0.2, 0, 0.4, lc, 6)

c3 = gmsh.model.geo.addCircleArc(4, 5, 6)
c4 = gmsh.model.geo.addCircleArc(6, 5, 4)

# gmsh.model.geo.addCurveLoop([c3,c4], 2)
# gmsh.model.geo.addPlaneSurface([2], 2)

'''
2 lines
'''

l1 = gmsh.model.geo.addLine(1, 4)
l2 = gmsh.model.geo.addLine(3, 6)

"""
areas and volume
"""

gmsh.model.geo.addCurveLoop([c1,l2,-c3,-l1], 3)
gmsh.model.geo.addSurfaceFilling([3],3)

# gmsh.model.geo.addCurveLoop([-c2,l2,c4,-l1], 4)
# gmsh.model.geo.addSurfaceFilling([4], 4)
# l = gmsh.model.geo.addSurfaceLoop([i + 1 for i in range(4)])
# gmsh.model.geo.addVolume([l])

gmsh.model.geo.synchronize()

gmsh.model.mesh.generate(3)

gmsh.write("t1.msh")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()