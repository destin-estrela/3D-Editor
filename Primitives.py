import json
import sys
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.Qt3DCore import Qt3DCore
from PySide2.Qt3DExtras import Qt3DExtras
from PySide2.Qt3DRender import Qt3DRender
from PySide2.Qt3DInput import Qt3DInput
from pysondb import db


PRIMITIVE_OBJECTS = "primitive_objects.json"

"""
Represents a generic namable, colorable three-dimensional primitive object
"""
class Primitive(QtCore.QObject):
    def __init__(self, root_entity, cameraEntity, shapeEditor, persist_id=None):
        super().__init__()
        self.m_rootEntity = root_entity
        self.m_cameraEntity = cameraEntity
        self.m_Entity = Qt3DCore.QEntity(self.m_rootEntity)
        self.persist_id = persist_id
        self.m_displayName = 'Primitive Object'
        self.shapeEditor = shapeEditor

        self.m_material = Qt3DExtras.QPhongMaterial(
            diffuse=QtGui.QColor(QtCore.Qt.gray))
        self.transform = Qt3DCore.QTransform(
            scale=1.3, translation=self.m_cameraEntity.viewCenter(),
        )
        self.m_Entity.addComponent(self.m_material)
        self.m_Entity.addComponent(self.transform)

        self.picker = Qt3DRender.QObjectPicker()
        self.picker.setHoverEnabled(True)
        self.picker.setDragEnabled(True)
        self.picker.clicked.connect(self.primitiveClicked)
        self.m_Entity.addComponent(self.picker)
    
    def primitiveClicked(self):
        print(f"{self.m_displayName} clicked!")
        self.shapeEditor.handleClickedPrimitive(self)

    """
    Deletes 3D object and removes from the databased 
    """
    def remove(self):
        database = db.getDb(PRIMITIVE_OBJECTS)
        if self.persist_id:
            database.deleteById(self.persist_id)

        self.m_Entity.setEnabled(False)
        self.deleteLater()
 
    """
    Setters
    """
    def setRotation(self, vector, doPersist=True):
        quat = QtGui.QQuaternion.fromEulerAngles(vector)
        self.transform.setRotation(quat)
        self.persist(doPersist)
    
    def setPosition(self, vector, doPersist=True):
        self.transform.setTranslation(vector)
        self.persist(doPersist)

    def setColor(self, color, doPersist=True):
        self.m_material.setDiffuse(color)
        self.persist(doPersist)

    def setName(self, name, doPersist=True):
        self.m_displayName = name
        self.persist(doPersist)
    
    """
    Getters
    """
    def color(self):
        return self.m_material.diffuse()
    
    def name(self):
        return self.m_displayName

    def position(self):
        return self.transform.translation()
    
    def rotation(self):
        return self.transform.rotation().toEulerAngles()

    """
    Restore object from a serialized representation
    """
    def restore(self, json_dict):
        # restore position
        xyz_dict = json_dict['position']
        vector = QtGui.QVector3D(xyz_dict['x'], xyz_dict['y'], xyz_dict['z'])
        self.setPosition(vector, False)

        # restore rotation
        xyz_dict = json_dict['rotation']
        vector = QtGui.QVector3D(xyz_dict['x'], xyz_dict['y'], xyz_dict['z'])
        self.setRotation(vector, False)

        # restore color
        color_str = json_dict['color']
        self.setColor(QtGui.QColor(color_str), False)

        self.setName(json_dict['name'], False)
    
    """
    Persist object fields and save to local storage
    """
    def persist(self, doPersist):
        if not doPersist:
            return 

        object_dict = self.toDict()
        database = db.getDb(PRIMITIVE_OBJECTS)

        if self.persist_id == None:
            id = database.add(object_dict)
            self.persist_id = id
        else:
            database.updateById(self.persist_id, object_dict)
    
    """
    Serialized representation of object
    """ 
    def toDict(self):
        translation = self.transform.translation()
        rotation = self.transform.rotation().toEulerAngles()
        return {'name': self.m_displayName,
                'position': {'x': translation.x(), 'y': translation.y(), 'z': translation.z()},
                'rotation': {'x': rotation.x(), 'y': rotation.y(), 'z': rotation.z()},
                'color': self.m_material.diffuse().name()}

"""
Represents a spherical 3D object
"""
class Sphere(Primitive):
    sphereTag = 1

    def __init__(self, root_entity, cameraEntity, shapeEditor, persist_id=None):
        super().__init__(root_entity, cameraEntity, shapeEditor, persist_id)

        self.sphereMesh = Qt3DExtras.QSphereMesh(
            rings=20, slices=20, radius=2)

        self.m_Entity.addComponent(self.sphereMesh)
        self.m_displayName = f'Sphere {Sphere.sphereTag}'

        if persist_id is None:
            self.persist(True)

        Sphere.sphereTag += 1
    
    def toDict(self):
        object_dict = super().toDict()
        object_dict['type'] = 'sphere'
        object_dict['primitive_specific'] = {'radius': self.sphereMesh.radius()}
        return object_dict
    
    def radius(self):
        return self.sphereMesh.radius()

    def primitiveType(self):
        return 'sphere'
    
    def setRadius(self, radius, doPersist=True):
        self.sphereMesh.setRadius(radius)
        self.persist(doPersist)
    
    def restore(self, json_dict):
        super().restore(json_dict)
        cubeInfo = json_dict['primitive_specific']
        self.setRadius(cubeInfo['radius'], False)
     

"""
Represents a cubical 3D object
"""
class Cube(Primitive):
    cubeTag = 1

    def __init__(self, root_entity, cameraEntity, shapeEditor, persist_id=None):
        super().__init__(root_entity, cameraEntity, shapeEditor, persist_id)
        self.cuboid = Qt3DExtras.QCuboidMesh()

        self.m_Entity.addComponent(self.cuboid)
        self.m_displayName = f'Cube {Cube.cubeTag}'
        self.transform.setScale(4.0)

        if persist_id is None:
            self.persist(True)

        Cube.cubeTag += 1

    def toDict(self):
        object_dict = super().toDict()
        object_dict['type'] = 'cube'
        object_dict['primitive_specific'] = {
            'length': self.cuboid.xExtent(),
            'width': self.cuboid.zExtent(),
            'height': self.cuboid.yExtent()}
        return object_dict
    
    def restore(self, json_dict):
        super().restore(json_dict)
        cubeInfo = json_dict['primitive_specific']
        self.setLength(cubeInfo['length'], False)
        self.setWidth(cubeInfo['width'], False)
        self.setHeight(cubeInfo['height'], False)

    def primitiveType(self):
        return 'cube'

    def length(self):
        return self.cuboid.xExtent()
    
    def width(self):
        return self.cuboid.zExtent()
    
    def height(self):
        return self.cuboid.yExtent()
    
    def setLength(self, length, doPersist=True):
        self.cuboid.setXExtent(length)
        self.persist(doPersist)

    def setWidth(self, length, doPersist=True):
        self.cuboid.setZExtent(length)
        self.persist(doPersist)

    def setHeight(self, length, doPersist=True):
        self.cuboid.setYExtent(length)
        self.persist(doPersist)