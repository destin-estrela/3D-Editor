import sys
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.Qt3DCore import Qt3DCore
from PySide2.Qt3DExtras import Qt3DExtras
from PySide2.Qt3DRender import Qt3DRender
from PySide2.Qt3DInput import Qt3DInput
from Primitives import *
from PrimitiveEditorWidgets import *

class PrimitiveListItem(QtWidgets.QListWidgetItem):
    def __init__(self, name, sceneObject):
        super().__init__(name)
        self.m_sceneObject = sceneObject
        self.name = name

    def sceneObject(self):
        return self.m_sceneObject

    def setName(self, name):
        self.name = name
        self.setText(name)

class CubeListItem(PrimitiveListItem):
    def __init__(self, name, sceneObject):
        super().__init__(name, sceneObject)

    def activate_primitive_editor(self):
        new_widget = CubeEditorWidget(self)
        return new_widget

class SphereListItem(PrimitiveListItem):
    def __init__(self, name, sceneObject):
        super().__init__(name, sceneObject)

    def activate_primitive_editor(self):
        new_widget = SphereEditorWidget(self)
        return new_widget
