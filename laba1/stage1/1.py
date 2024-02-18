import gmsh
import sys

gmsh.initialize()

gmsh.model.add("t2")



gmsh.model.geo.synchronize()

gmsh.model.mesh.generate(3)

gmsh.write("t1.msh")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()