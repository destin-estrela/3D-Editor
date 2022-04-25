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
        self.m_defaultMaterial = Qt3DExtras.QPhongMaterial(
            diffuse=QtGui.QColor("#665423"))


class Sphere(Primitive):
    sphereTag = 1

    def __init__(self, root_entity=None, cameraEntity=None):
        super().__init__(root_entity, cameraEntity)

        self.sphereMesh = Qt3DExtras.QSphereMesh(
            rings=20, slices=20, radius=2)

        self.sphereTransform = Qt3DCore.QTransform(
            scale=1.3, translation=self.m_cameraEntity.viewCenter(),
        )

        self.m_sphereEntity = Qt3DCore.QEntity(self.m_rootEntity)
        self.m_sphereEntity.addComponent(self.sphereMesh)
        self.m_sphereEntity.addComponent(self.m_defaultMaterial)
        self.m_sphereEntity.addComponent(self.sphereTransform)
        self.m_displayName = f'Sphere {Sphere.sphereTag}'
        Sphere.sphereTag += 1


class Cube(Primitive):
    cubeTag = 1

    def __init__(self, root_entity=None, cameraEntity=None):
        super().__init__(root_entity, cameraEntity)
        self.cuboid = Qt3DExtras.QCuboidMesh()
        self.cuboidTransform = Qt3DCore.QTransform(
            scale=4.0, translation=self.m_cameraEntity.viewCenter(),
        )
        self.cuboidMaterial = Qt3DExtras.QPhongMaterial(
            diffuse=QtGui.QColor("#665423"))

        self.m_cuboidEntity = Qt3DCore.QEntity(self.m_rootEntity)
        self.m_cuboidEntity.addComponent(self.cuboid)
        self.m_cuboidEntity.addComponent(self.cuboidMaterial)
        self.m_cuboidEntity.addComponent(self.cuboidTransform)
        self.m_displayName = f'Cube {Cube.cubeTag}'
        Cube.cubeTag += 1
