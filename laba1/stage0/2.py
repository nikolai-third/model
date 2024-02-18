import gmsh
import sys

gmsh.initialize()
gmsh.model.add("t1")
lc = 1e-2
gmsh.model.geo.addPoint(0, 0, 0, lc, 1)

gmsh.model.geo.addPoint(.1, 0, 0, lc, 2)
gmsh.model.geo.addPoint(.2, 0, 0, lc, 3)

c1 = gmsh.model.geo.addCircleArc(1, 2, 3)
c2 = gmsh.model.geo.addCircleArc(3, 2, 1)

gmsh.model.geo.synchronize()

gmsh.model.mesh.generate(2)

gmsh.write("t1.msh")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()