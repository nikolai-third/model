import pygmsh
import numpy as np

def create_parallelepiped(length, width, height):
    geom = pygmsh.built_in.Geometry()

    # Define the corners of the parallelepiped
    corners = np.array([[0, 0, 0],
                        [length, 0, 0],
                        [length, width, 0],
                        [0, width, 0],
                        [0, 0, height],
                        [length, 0, height],
                        [length, width, height],
                        [0, width, height]])

    # Create points
    points = [geom.add_point(c, lcar=0.1) for c in corners]

    # Create lines
    lines = [geom.add_line(points[i], points[(i + 1) % 4]) for i in range(4)]
    lines += [geom.add_line(points[i], points[i + 4]) for i in range(4)]
    lines += [geom.add_line(points[i + 4], points[(i + 1) % 4 + 4]) for i in range(4)]

    # Create surfaces
    faces = [geom.add_line_loop(lines[i:i + 4]) for i in range(0, 8, 4)]
    geom.add_plane_surface(faces)

    return geom

length = 1.0
width = 0.5
height = 0.3

geom = create_parallelepiped(length, width, height)

# Generate mesh
mesh = pygmsh.generate_mesh(geom)

# Write mesh to file
mesh.write("parallelepiped.msh")
