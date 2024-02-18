import gmsh
import sys

gmsh.initialize()

gmsh.model.add("t2")

lc = 1e-2
gmsh.model.geo.addPoint(0, 0, 0, lc, 1)
gmsh.model.geo.addPoint(.1, 0, 0, lc, 2)
gmsh.model.geo.addPoint(0, .1, 0, lc, 4)
gmsh.model.geo.addPoint(0, 0, .1, lc, 5)
gmsh.model.geo.addPoint(.1, .1, 0, lc, 3)
gmsh.model.geo.addPoint(0, .1, .1, lc, 8)
gmsh.model.geo.addPoint(.1, 0, .1, lc, 6)
gmsh.model.geo.addPoint(.1, .1, .1, lc, 7)

u = 1
for i in range(1, 5):
    if (i!= 4):
        gmsh.model.geo.addLine(i, (i+1), u)
        u += 1
        gmsh.model.geo.addLine((i+4), (i+5), u)
        u += 1
    else:
        gmsh.model.geo.addLine(i, (i-3), u)
        u += 1
        gmsh.model.geo.addLine((i+4), (i+1), u)
        u += 1
    gmsh.model.geo.addLine(i, i+4, u)
    u += 1


gmsh.model.geo.addCurveLoop([1, 6, -2, -3], 1)
gmsh.model.geo.addPlaneSurface([1], 1)

gmsh.model.geo.addCurveLoop([5, -9, -4, 6], 2)
gmsh.model.geo.addPlaneSurface([2], 2)

gmsh.model.geo.addCurveLoop([9, 8, -12, -7], 3)
gmsh.model.geo.addPlaneSurface([3], 3)

gmsh.model.geo.addCurveLoop([12, 11, -3, -10], 4)
gmsh.model.geo.addPlaneSurface([4], 4)

gmsh.model.geo.addCurveLoop([2, 5, 8, 11], 5)
gmsh.model.geo.addPlaneSurface([5], 5)

gmsh.model.geo.addCurveLoop([1, 4, 7, 10], 6)
gmsh.model.geo.addPlaneSurface([6], 6)

l = gmsh.model.geo.addSurfaceLoop([i + 1 for i in range(6)])
gmsh.model.geo.addVolume([l])

gmsh.model.geo.synchronize()

gmsh.model.mesh.generate(3)

gmsh.fltk.run()

gmsh.finalize()

