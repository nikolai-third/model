import gmsh
import math
import numpy as np

a = 1e+6               # ширина и длина
g = 9.81               # ускорение свободного падения
H = 100                # глубина резервуара

gmsh.initialize()


# Create a new model
gmsh.model.add('sphere')

# Parameters for sphere
radius = 5e+4
v2 = np.pi*4/3*radius**3
num_points = 20
lc = 1e+4

# Create points on the sphere surface
points = []
for i in range(num_points):
    theta = (math.pi * i) / (num_points - 1)
    if (i == 0 or i == num_points-1):
        phi = 0
        x = a/2 + radius * math.sin(theta) * math.cos(phi)
        y = a/2 + radius * math.sin(theta) * math.sin(phi)
        z = a/6 + radius * math.cos(theta)
        points.append(gmsh.model.geo.addPoint(x, y, z, lc))
    else:
        for j in range(num_points-1):
            phi = (2 * math.pi * j) / (num_points - 1)
            x = a/2 + radius * math.sin(theta) * math.cos(phi)
            y = a/2 + radius * math.sin(theta) * math.sin(phi)
            z = a/6 + radius * math.cos(theta)
            points.append(gmsh.model.geo.addPoint(x, y, z, lc))

# Create lines connecting points
lines = []
for i in range(num_points-2):
    for j in range(1, num_points):
        if j != num_points-1:
            lines.append(gmsh.model.geo.addLine(points[i * (num_points-1) + j], points[i * (num_points-1) + j + 1]))
        else:
            lines.append(gmsh.model.geo.addLine(points[i * (num_points-1) + j], points[i * (num_points-1) + 1]))
        
for i in range(num_points-2):
    if (i == 0):
        for u in range(2):
            for k in range(1, num_points):
                if u == 0:
                    lines.append(gmsh.model.geo.addLine(points[0], points[k]))
                else:
                    lines.append(gmsh.model.geo.addLine(points[k], points[(num_points-1)+k]))
    else:
        for j in range(1, num_points):
            if (i == num_points-3):
                lines.append(gmsh.model.geo.addLine(points[i * (num_points-1)+j], points[len(points)-1]))
            else:
                lines.append(gmsh.model.geo.addLine(points[i * (num_points-1)+j], points[(i+1) * (num_points-1)+j]))


num_of_paralel = (num_points-1)*(num_points-2)

surfaces = []
for i in range(num_points-1):
    for j in range(1, num_points):
        if (i == 0):
            if (j!=num_points-1):
                surfaces.append(gmsh.model.geo.addCurveLoop([j, -1*(num_of_paralel+j+1), num_of_paralel+j]))
            else:
                surfaces.append(gmsh.model.geo.addCurveLoop([j, -1*(num_of_paralel+1), num_of_paralel+j]))
        elif(i != num_points-2):
            if (j!=num_points-1):
                surfaces.append(gmsh.model.geo.addCurveLoop([i*(num_points-1) + j, -1*(i*(num_points-1) + num_of_paralel+j+1), 
                                             -1*((i-1)*(num_points-1) + j), i*(num_points-1) + num_of_paralel+j]))
            else:
                surfaces.append(gmsh.model.geo.addCurveLoop([i*(num_points-1) + j, -1*(i*(num_points-1) + num_of_paralel+1), 
                                             -1*((i-1)*(num_points-1) + j), i*(num_points-1) + num_of_paralel+j]))
        else:
            if (j!=num_points-1):
                surfaces.append(gmsh.model.geo.addCurveLoop([(i-1)*(num_points-1) + j, -1*(i*(num_points-1) + num_of_paralel+j), 
                                             i*(num_points-1) + num_of_paralel+j+1]))
            else:
                surfaces.append(gmsh.model.geo.addCurveLoop([(i-1)*(num_points-1) + j, (i-1)*(num_points-1) + num_of_paralel+j+1,
                                             -1*(i*(num_points-1) + num_of_paralel+j)]))


plane_surfaces = [gmsh.model.geo.addPlaneSurface([curve_loop]) for curve_loop in surfaces]

l2 = gmsh.model.geo.addSurfaceLoop(plane_surfaces)
gmsh.model.geo.addVolume([l2])

h = 0.001
v1 = h*a*a
v = v1 + v2
p1 = gmsh.model.geo.addPoint(0, 0, 0, lc)
p2 = gmsh.model.geo.addPoint(a, 0, 0, lc)
p4 = gmsh.model.geo.addPoint(0, a, 0, lc)
p5 = gmsh.model.geo.addPoint(0, 0, h, lc)
p3 = gmsh.model.geo.addPoint(a, a, 0, lc)
p8 = gmsh.model.geo.addPoint(0, a, h, lc)
p6 = gmsh.model.geo.addPoint(a, 0, h, lc)
p7 = gmsh.model.geo.addPoint(a, a, h, lc)

l1 = gmsh.model.geo.addLine(p1, p2)
l2 = gmsh.model.geo.addLine(p2, p3)
l3 = gmsh.model.geo.addLine(p3, p4)
l4 = gmsh.model.geo.addLine(p4, p1)
l5 = gmsh.model.geo.addLine(p5, p6)
l6 = gmsh.model.geo.addLine(p6, p7)
l7 = gmsh.model.geo.addLine(p7, p8)
l8 = gmsh.model.geo.addLine(p8, p5)
l9 = gmsh.model.geo.addLine(p1, p5)
l10 = gmsh.model.geo.addLine(p2, p6)
l11 = gmsh.model.geo.addLine(p3, p7)
l12 = gmsh.model.geo.addLine(p4, p8)


c1 = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4])
p1 = gmsh.model.geo.addPlaneSurface([c1])

c2 = gmsh.model.geo.addCurveLoop([l5, l6, l7, l8])
p2 = gmsh.model.geo.addPlaneSurface([c2])

c3 = gmsh.model.geo.addCurveLoop([l3, l12, -l7, -l11])
p3 = gmsh.model.geo.addPlaneSurface([c3])

c4 = gmsh.model.geo.addCurveLoop([l4, l9, -l8, -l12])
p4 = gmsh.model.geo.addPlaneSurface([c4])

c5 = gmsh.model.geo.addCurveLoop([l1, l10, -l5, -l9])
p5 = gmsh.model.geo.addPlaneSurface([c5])

c6 = gmsh.model.geo.addCurveLoop([l2, l11, -l6, -l10])
p6 = gmsh.model.geo.addPlaneSurface([c6])

l1 = gmsh.model.geo.addSurfaceLoop([i for i in [p1, p2 , p3, p4, p5, p6]])
gmsh.model.geo.addVolume([l1])

# # Generate mesh
gmsh.model.geo.synchronize()
gmsh.model.mesh.generate(3)

# Run Gmsh GUI
gmsh.fltk.run()

# Finalize Gmsh
gmsh.finalize()
