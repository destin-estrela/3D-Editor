import sys
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.Qt3DCore import Qt3DCore
from PySide2.Qt3DExtras import Qt3DExtras
from PySide2.Qt3DRender import Qt3DRender
from PySide2.Qt3DInput import Qt3DInput
from pysondb import db


PRIMITIVE_OBJECTS = "primitive_objects.json"
class Primitive(QtCore.QObject):
    def __init__(self, root_entity=None, cameraEntity=None, persist_id=None):
        super().__init__()
        self.m_rootEntity = root_entity
        self.m_cameraEntity = cameraEntity
        self.m_Entity = Qt3DCore.QEntity(self.m_rootEntity)
        self.persist_id = persist_id
        self.m_displayName = 'Primitive Object'

        self.m_material = Qt3DExtras.QPhongMaterial(
            diffuse=QtGui.QColor(QtCore.Qt.gray))
        self.transform = Qt3DCore.QTransform(
            scale=1.3, translation=self.m_cameraEntity.viewCenter(),
        )
        self.m_Entity.addComponent(self.m_material)
        self.m_Entity.addComponent(self.transform)
    
    def remove(self):
        database = db.getDb(PRIMITIVE_OBJECTS)
        if self.persist_id:
            database.deleteById(self.persist_id)

        self.m_Entity.setEnabled(False)
        self.deleteLater()
    
    def toDict(self):
        translation = self.transform.translation()
        rotation = self.transform.rotation().toEulerAngles()
        return {'name': self.m_displayName,
                'position': {'x': translation.x(), 'y': translation.y(), 'z': translation.z()},
                'rotation': {'x': rotation.x(), 'y': rotation.y(), 'z': rotation.z()},
                'color': self.m_material.diffuse().name()}

    def persist(self):
        object_dict = self.toDict()
        database = db.getDb(PRIMITIVE_OBJECTS)

        if self.persist_id == None:
            id = database.add(object_dict)
            self.persist_id = id
        else:
            database.updateById(self.persist_id, object_dict)

class Sphere(Primitive):
    sphereTag = 1

    def __init__(self, root_entity=None, cameraEntity=None):
        super().__init__(root_entity, cameraEntity)

        self.sphereMesh = Qt3DExtras.QSphereMesh(
            rings=20, slices=20, radius=2)

        self.m_Entity.addComponent(self.sphereMesh)
        self.m_displayName = f'Sphere {Sphere.sphereTag}'
        Sphere.sphereTag += 1
    
    def toDict(self):
        object_dict = super().toDict()
        object_dict['type'] = 'sphere'
        object_dict['primitive_specific'] = {'radius': self.sphereMesh.radius()}
        return object_dict



class Cube(Primitive):
    cubeTag = 1

    def __init__(self, root_entity=None, cameraEntity=None):
        super().__init__(root_entity, cameraEntity)
        self.cuboid = Qt3DExtras.QCuboidMesh()

        self.m_Entity.addComponent(self.cuboid)
        self.m_displayName = f'Cube {Cube.cubeTag}'
        self.transform.setScale(4.0)
        Cube.cubeTag += 1


    def toDict(self):
        object_dict = super().toDict()
        object_dict['type'] = 'cube'
        object_dict['primitive_specific'] = {
            'length': self.cuboid.xExtent(),
            'width': self.cuboid.zExtent(),
            'height': self.cuboid.yExtent()}
        return object_dict
