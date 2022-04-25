import sys
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.Qt3DCore import Qt3DCore
from PySide2.Qt3DExtras import Qt3DExtras
from PySide2.Qt3DRender import Qt3DRender
from PySide2.Qt3DInput import Qt3DInput

class Primitive(QtCore.QObject):
    def __init__(self, root_entity=None, cameraEntity=None):
        super().__init__()
        self.m_rootEntity = root_entity
        self.m_cameraEntity = cameraEntity
        self.m_Entity = Qt3DCore.QEntity(self.m_rootEntity)

        self.m_material = Qt3DExtras.QPhongMaterial(
            diffuse=QtGui.QColor("#665423"))
        self.transform = Qt3DCore.QTransform(
            scale=1.3, translation=self.m_cameraEntity.viewCenter(),
        )
        self.m_Entity.addComponent(self.m_material)
        self.m_Entity.addComponent(self.transform)

class Sphere(Primitive):
    sphereTag = 1

    def __init__(self, root_entity=None, cameraEntity=None):
        super().__init__(root_entity, cameraEntity)

        self.sphereMesh = Qt3DExtras.QSphereMesh(
            rings=20, slices=20, radius=2)

        self.m_Entity.addComponent(self.sphereMesh)
        self.m_displayName = f'Sphere {Sphere.sphereTag}'
        Sphere.sphereTag += 1


class Cube(Primitive):
    cubeTag = 1

    def __init__(self, root_entity=None, cameraEntity=None):
        super().__init__(root_entity, cameraEntity)
        self.cuboid = Qt3DExtras.QCuboidMesh()
        self.m_Entity.addComponent(self.cuboid)
        self.m_displayName = f'Cube {Cube.cubeTag}'
        self.transform.setScale(4.0)
        Cube.cubeTag += 1
