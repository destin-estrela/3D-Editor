from multiprocessing.sharedctypes import Value
import sys
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.Qt3DCore import Qt3DCore
from PySide2.Qt3DExtras import Qt3DExtras
from PySide2.Qt3DRender import Qt3DRender
from PySide2.Qt3DInput import Qt3DInput

# Returns string as a float only if it can be properly converted
# else None
def validate(text):
        try:
            res = float(text)
            return res
        except ValueError:
            return None

class XYZEditorWidget(QtWidgets.QWidget):
    def __init__(self, transform, vector, set_vector):
        QtWidgets.QWidget.__init__(self)
        layout = QtWidgets.QHBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        self.transform = transform
        self.vector = vector
        self.set_vector = set_vector

        self.X_label = QtWidgets.QLabel("X")
        self.Y_label = QtWidgets.QLabel("Y")
        self.Z_label = QtWidgets.QLabel("Z")

        self.onlyDouble = QtGui.QDoubleValidator(self)

        self.X_edit = QtWidgets.QLineEdit(str(round(self.vector.x(), 5)))
        self.Y_edit = QtWidgets.QLineEdit(str(round(self.vector.y(), 5)))
        self.Z_edit = QtWidgets.QLineEdit(str(round(self.vector.z(), 5)))

        self.X_edit.textChanged.connect(self.x_changed)
        self.Y_edit.textChanged.connect(self.y_changed)
        self.Z_edit.textChanged.connect(self.z_changed)

        self.X_edit.setValidator(self.onlyDouble)
        self.Y_edit.setValidator(self.onlyDouble)
        self.Z_edit.setValidator(self.onlyDouble)

        layout.addWidget(self.X_label)
        layout.addWidget(self.X_edit)

        layout.addWidget(self.Y_label)
        layout.addWidget(self.Y_edit)

        layout.addWidget(self.Z_label)
        layout.addWidget(self.Z_edit)

        self.setLayout(layout)
        self.show()
    
    

    def x_changed(self, text):
        number = validate(text)
        if number:
            self.vector.setX(float(text))
            self.set_vector(self.vector)

    def y_changed(self, text):
        number = validate(text)
        if number:
            self.vector.setY(float(text))
            self.set_vector(self.vector)

    def z_changed(self, text):
        number = validate(text)
        if number:
            self.vector.setZ(float(text))
            self.set_vector(self.vector)

class PrimitiveEditorWidget(QtWidgets.QWidget):
    def __init__(self, listItem):
        QtWidgets.QWidget.__init__(self)

        self.listItem = listItem

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout = layout
        self.setLayout(layout)

        # delete button
        self.deleteButton = QtWidgets.QPushButton(self, "Delete")
        self.deleteButton.setText("Delete")
        self.deleteButton.clicked.connect(self.delete_primitive)
        layout.addWidget(self.deleteButton)


        # name field
        self.name = QtWidgets.QLabel("Name")
        layout.addWidget(self.name)
        self.name_edit_box = QtWidgets.QLineEdit(listItem.sceneObject.m_displayName)
        layout.addWidget(self.name_edit_box)
        self.name_edit_box.textChanged.connect(self.name_changed)

        # color field
        self.color_label = QtWidgets.QLabel("Color")
        self.colorButton = QtWidgets.QPushButton(self)
        self.colorButton.clicked.connect(self.open_color_dialog)
        self.colorButton.setStyleSheet(
            f"background-color:{ self.listItem.sceneObject.m_material.diffuse().name()}")


        layout.addWidget(self.color_label)
        layout.addWidget(self.colorButton)

        self.color_dialog = QtWidgets.QColorDialog()
        self.color_dialog.currentColorChanged.connect(self.save_selected_color)

        # transform field
        self.transform_label = QtWidgets.QLabel("Position")
        layout.addWidget(self.transform_label)

        self.transform_widget = XYZEditorWidget(
            self.listItem.sceneObject.transform, self.listItem.sceneObject.transform.translation(), self.listItem.sceneObject.transform.setTranslation)
        layout.addWidget(self.transform_widget)

        # quaternion field
        self.quaternion_label = QtWidgets.QLabel("Rotation")
        layout.addWidget(self.quaternion_label)

        self.rotation_widget = XYZEditorWidget(
            self.listItem.sceneObject.transform, self.listItem.sceneObject.transform.rotation().toEulerAngles(), self.set_rotation)
        layout.addWidget(self.rotation_widget)
        

        self.show()
    
    def set_rotation(self, vector):
        quat = QtGui.QQuaternion.fromEulerAngles(vector)
        self.listItem.sceneObject.transform.setRotation(quat)

    def delete_primitive(self):
        listView = self.listItem.listWidget()
        self.listItem.sceneObject.m_Entity.setEnabled(False)
        self.listItem.sceneObject.deleteLater()
        listView.takeItem(listView.row(self.listItem))
        self.hide()

    def name_changed(self, text):
        self.listItem.sceneObject.m_displayName = text
        self.listItem.setText(text)

    def open_color_dialog(self):
        self.color_dialog.open()

    def save_selected_color(self, new_color):
        self.colorButton.setStyleSheet(f"background-color:{new_color.name()}")
        self.listItem.sceneObject.m_material.setDiffuse(new_color)

class SphereEditorWidget(PrimitiveEditorWidget):
    def __init__(self, listItem):
        PrimitiveEditorWidget.__init__(self, listItem)

        self.radius_label = QtWidgets.QLabel("Radius")
        self.radius_edit = QtWidgets.QLineEdit(str(round(listItem.sceneObject.sphereMesh.radius(), 5)))
        self.radius_edit.textChanged.connect(self.radius_changed)

        self.layout.addWidget(self.radius_label)
        self.layout.addWidget(self.radius_edit)

        self.setLayout(self.layout)
        self.show()
    
    def radius_changed(self, text):
        num = validate(text)
        if num:
            self.listItem.sceneObject.sphereMesh.setRadius(num)


class CubeEditorWidget(PrimitiveEditorWidget):
    def __init__(self, listItem):
        PrimitiveEditorWidget.__init__(self, listItem)

        self.length_label = QtWidgets.QLabel("Length")
        self.width_label = QtWidgets.QLabel("Width")
        self.height_label = QtWidgets.QLabel("Height")

        self.length_edit = QtWidgets.QLineEdit(str(round(self.listItem.sceneObject.cuboid.xExtent(), 5)))
        self.width_edit = QtWidgets.QLineEdit(str(round(self.listItem.sceneObject.cuboid.zExtent(), 5)))
        self.height_edit = QtWidgets.QLineEdit(
            str(round(self.listItem.sceneObject.cuboid.yExtent(), 5)))

        self.length_edit.textChanged.connect(self.length_changed)
        self.width_edit.textChanged.connect(self.width_changed)
        self.height_edit.textChanged.connect(self.height_changed)

        self.layout.addWidget(self.length_label)
        self.layout.addWidget(self.length_edit)

        self.layout.addWidget(self.width_label)
        self.layout.addWidget(self.width_edit)

        self.layout.addWidget(self.height_label)
        self.layout.addWidget(self.height_edit)

        self.setLayout(self.layout)
        self.show()
    
    def length_changed(self, text):
        num = validate(text)
        if num:
            self.listItem.sceneObject.cuboid.setXExtent(num)

    def width_changed(self, text):
        num = validate(text)
        if num:
            self.listItem.sceneObject.cuboid.setZExtent(num)

    def height_changed(self, text):
        num = validate(text)
        if num:
            self.listItem.sceneObject.cuboid.setYExtent(num)
