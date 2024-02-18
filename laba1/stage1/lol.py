import gmsh

# Initialize Gmsh
gmsh.initialize()

# Create a new Gmsh model
gmsh.model.add("circle")

# Define the circle geometry
radius = 1.0
center_x = 0.0
center_y = 0.0
center_z = 0.0  # Center of the circle (z-coordinate)

# Add the center point
center_point = gmsh.model.geo.addPoint(center_x, center_y, center_z)

# Add the two points to define the circle in XY plane
point1 = gmsh.model.geo.addPoint(center_x + radius, center_y, center_z)
point2 = gmsh.model.geo.addPoint(center_x, center_y + radius, center_z)

# Create the circle arc using the two points and the center
circle_arc = gmsh.model.geo.addCircleArc(point1, center_point, point2)

# Create a line loop from the circle arc
circle_loop = gmsh.model.geo.addCurveLoop([circle_arc])

# Create a surface from the line loop
circle_surface = gmsh.model.geo.addPlaneSurface([circle_loop])

# Extrude the circle to make it parallel to OZ plane
extruded_surface = gmsh.model.geo.extrude(circle_surface, 0, 0, 1)

# Synchronize the model to update the internal data structures
gmsh.model.geo.synchronize()

# Generate the mesh
gmsh.model.mesh.generate(3)  # Generate 3D mesh

# Save the mesh to a file
gmsh.write("circle.msh")

# Finalize Gmsh
gmsh.finalize()