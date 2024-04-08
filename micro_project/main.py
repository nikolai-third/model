import gmsh
import math

# Initialize Gmsh
gmsh.initialize()

# Create a new model
gmsh.model.add('sphere')

lc = 1e-3
gmsh.model.geo.addPoint(0, 0, 0, lc, 1)
gmsh.model.geo.addPoint(.1, 0, 0, lc, 2)
gmsh.model.geo.addPoint(0, .1, 0, lc, 4)
gmsh.model.geo.addPoint(0, 0, .001, lc, 5)
gmsh.model.geo.addPoint(.1, .1, 0, lc, 3)
gmsh.model.geo.addPoint(0, .1, .001, lc, 8)
gmsh.model.geo.addPoint(.1, 0, .001, lc, 6)
gmsh.model.geo.addPoint(.1, .1, .001, lc, 7)

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

#gmsh.model.geo.synchronize()
#gmsh.model.mesh.generate(3)



# Sphere parameters
radius = 0.007
num_points = 20
num_lines = 2 * num_points

# Create points on the surface of the sphere
points = []
for i in range(num_points):
    theta = (math.pi * i) / (num_points - 1)
    for j in range(num_points):
        phi = (2 * math.pi * j) / (num_points - 1)
        x = 0.05 + radius * math.sin(theta) * math.cos(phi)
        y = 0.05 + radius * math.sin(theta) * math.sin(phi)
        z = 0.03 + radius * math.cos(theta)
        points.append(gmsh.model.geo.addPoint(x, y, z, meshSize=0.1))

# Create curves forming squares on the surface of the sphere
curves = []
for i in range(num_points - 1):
    for j in range(num_points - 1):
        curve_points = [
            points[i * num_points + j],
            points[i * num_points + j + 1],
            points[(i + 1) * num_points + j + 1],
            points[(i + 1) * num_points + j],
            points[i * num_points + j]
        ]
        curves.append([gmsh.model.geo.addLine(curve_points[k], curve_points[k + 1]) for k in range(4)])

# Create plane surfaces for each CurveLoop
plane_surfaces = []
for curve_loop in curves:
    curve_loop_id = gmsh.model.geo.addCurveLoop(curve_loop)
    plane_surfaces.append(gmsh.model.geo.addPlaneSurface([curve_loop_id]))

# Create surface loop
surface_loop = gmsh.model.geo.addSurfaceLoop(plane_surfaces)

# Create volume
volume = gmsh.model.geo.addVolume([surface_loop])

# Generate mesh
gmsh.model.geo.synchronize()
gmsh.model.mesh.generate(2)


# Run Gmsh GUI
gmsh.fltk.run()

# Finalize Gmsh
gmsh.finalize()
