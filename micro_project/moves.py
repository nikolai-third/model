import numpy as np
import gmsh
import vtk
import math
import os
import sys


# Класс расчётной сетки
class CalcMesh:

    # Конструктор сетки, полученной из stl-файла
    def __init__(self, nodes_coords, tetrs_points):
        # 3D-сетка из расчётных точек
        # Пройдём по узлам в модели gmsh и заберём из них координаты 
        self.nodes = np.array([nodes_coords[0::3],nodes_coords[1::3],nodes_coords[2::3]])

        # Модельная скалярная величина распределена как-то вот такç
        self.smth = np.log10(abs(self.nodes[0, :]*np.exp(self.nodes[1, :])*np.cos(self.nodes[2, :])))

        self.velocity = np.zeros(shape=(3, len(self.nodes[0, :])), dtype=np.double)
        

        # Пройдём по элементам в модели gmsh
        self.tetrs = np.array([tetrs_points[0::4],tetrs_points[1::4],tetrs_points[2::4],tetrs_points[3::4]])
        self.tetrs -= 1

    # Метод отвечает за выполнение для всей сетки шага по времени величиной tau
    def move(self, tau, time):    
        self.velocity[1] = 10*np.cos(0.5*self.nodes[1]-10*(time-50*tau))
        self.velocity[2] = 10*np.sin(0.5*self.nodes[2]-10*(time-50*tau))


        # По сути метод просто двигает все точки c их текущими скоростями
        self.nodes += self.velocity * tau

        self.smth = np.log10(abs(self.nodes[0, :]*np.exp(self.nodes[1, :])*np.cos(self.nodes[2, :])))

    # Метод отвечает за запись текущего состояния сетки в снапшот в формате VTK
    def snapshot(self, snap_number):
        # Сетка в терминах VTK
        unstructuredGrid = vtk.vtkUnstructuredGrid()
        # Точки сетки в терминах VTK
        points = vtk.vtkPoints()

        # Скалярное поле на точках сетки
        smth = vtk.vtkDoubleArray()
        smth.SetName("smth")

        # Векторное поле на точках сетки
        vel = vtk.vtkDoubleArray()
        vel.SetNumberOfComponents(3)
        vel.SetName("vel")

        # Обходим все точки нашей расчётной сетки
        # Делаем это максимально неэффективным, зато наглядным образом
        for i in range(0, len(self.nodes[0])):
            # Вставляем новую точку в сетку VTK-снапшота
            points.InsertNextPoint(self.nodes[0,i], self.nodes[1,i], self.nodes[2,i])
            # Добавляем значение скалярного поля в этой точке
            smth.InsertNextValue(self.smth[i])
            # Добавляем значение векторного поля в этой точке
            vel.InsertNextTuple((self.velocity[0,i], self.velocity[1,i], self.velocity[2,i]))

        # Грузим точки в сетку
        unstructuredGrid.SetPoints(points)

        # Присоединяем векторное и скалярное поля к точкам
        unstructuredGrid.GetPointData().AddArray(smth)
        unstructuredGrid.GetPointData().AddArray(vel)

        # А теперь пишем, как наши точки объединены в тетраэдры
        # Делаем это максимально неэффективным, зато наглядным образом
        for i in range(0, len(self.tetrs[0])):
            tetr = vtk.vtkTetra()
            for j in range(0, 4):
                tetr.GetPointIds().SetId(j, self.tetrs[j,i])
            unstructuredGrid.InsertNextCell(tetr.GetCellType(), tetr.GetPointIds())

        # Создаём снапшот в файле с заданным именем
        writer = vtk.vtkXMLUnstructuredGridWriter()
        writer.SetInputDataObject(unstructuredGrid)
        writer.SetFileName("Wood-step-" + str(snap_number) + ".vtu")
        writer.Write()


# Теперь придётся немного упороться:
# (а) построением сетки средствами gmsh,
# (б) извлечением данных этой сетки в свой код.
gmsh.initialize()


# Create a new model
gmsh.model.add('sphere')

# Parameters for sphere
radius = 0.007
num_points = 20
lc = 1e-3

# Create points on the sphere surface
points = []
for i in range(num_points):
    theta = (math.pi * i) / (num_points - 1)
    if (i == 0 or i == num_points-1):
        phi = 0
        x = 0.05 + radius * math.sin(theta) * math.cos(phi)
        y = 0.05 + radius * math.sin(theta) * math.sin(phi)
        z = 0.03 + radius * math.cos(theta)
        points.append(gmsh.model.geo.addPoint(x, y, z, lc))
    else:
        for j in range(num_points-1):
            phi = (2 * math.pi * j) / (num_points - 1)
            x = 0.05 + radius * math.sin(theta) * math.cos(phi)
            y = 0.05 + radius * math.sin(theta) * math.sin(phi)
            z = 0.03 + radius * math.cos(theta)
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



p1 = gmsh.model.geo.addPoint(0, 0, 0, lc)
p2 = gmsh.model.geo.addPoint(.1, 0, 0, lc)
p4 = gmsh.model.geo.addPoint(0, .1, 0, lc)
p5 = gmsh.model.geo.addPoint(0, 0, .001, lc)
p3 = gmsh.model.geo.addPoint(.1, .1, 0, lc)
p8 = gmsh.model.geo.addPoint(0, .1, .001, lc)
p6 = gmsh.model.geo.addPoint(.1, 0, .001, lc)
p7 = gmsh.model.geo.addPoint(.1, .1, .001, lc)

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




# Теперь извлечём из gmsh данные об узлах сетки
nodeTags, nodesCoord, parametricCoord = gmsh.model.mesh.getNodes()

# И данные об элементах сетки тоже извлечём, нам среди них нужны только тетраэдры, которыми залит объём
GMSH_TETR_CODE = 4
tetrsNodesTags = None
elementTypes, elementTags, elementNodeTags = gmsh.model.mesh.getElements()
for i in range(0, len(elementTypes)):
    if elementTypes[i] != GMSH_TETR_CODE:
        continue
    tetrsNodesTags = elementNodeTags[i]

if tetrsNodesTags is None:
    print("Can not find tetra data. Exiting.")
    gmsh.finalize()
    exit(-2)

print("The model has %d nodes and %d tetrs" % (len(nodeTags), len(tetrsNodesTags) / 4))

# На всякий случай проверим, что номера узлов идут подряд и без пробелов
for i in range(0, len(nodeTags)):
    # Индексация в gmsh начинается с 1, а не с нуля. Ну штош, значит так.
    assert (i == nodeTags[i] - 1)
# И ещё проверим, что в тетраэдрах что-то похожее на правду лежит.
assert(len(tetrsNodesTags) % 4 == 0)

# TODO: неплохо бы полноценно данные сетки проверять, да

mesh = CalcMesh(nodesCoord, tetrsNodesTags)
mesh.snapshot(0)
tau = 0.01

# Делаем шаги по времени,
# на каждом шаге считаем новое состояние и пишем его в VTK
for i in range(1, 500):
    mesh.move(tau, i*tau)
    mesh.snapshot(i)


gmsh.finalize()