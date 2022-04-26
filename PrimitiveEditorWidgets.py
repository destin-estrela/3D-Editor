from multiprocessing.sharedctypes import Value
import sys
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.Qt3DCore import Qt3DCore
from PySide2.Qt3DExtras import Qt3DExtras
from PySide2.Qt3DRender import Qt3DRender
from PySide2.Qt3DInput import Qt3DInput

"""
 Returns string as a float only if it can be properly converted.
 Otherwise, returns None without erroring.
"""
def validate_float(text):
        try:
            res = float(text)
            return res
        except ValueError:
            return None

"""
A reusable widget that allows the user to edit a 3D vector
"""
class XYZEditorWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        layout = QtWidgets.QHBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)

        self.X_label = QtWidgets.QLabel("X")
        self.Y_label = QtWidgets.QLabel("Y")
        self.Z_label = QtWidgets.QLabel("Z")

        self.onlyDouble = QtGui.QDoubleValidator(self)

        self.X_edit = QtWidgets.QLineEdit()
        self.Y_edit = QtWidgets.QLineEdit()
        self.Z_edit = QtWidgets.QLineEdit()

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
    
    def populate_fields(self, vector, setVector):
        self.vector = vector
        self.setVector = setVector
        self.X_edit.setText(str(round(self.vector.x(), 5))) 
        self.Y_edit.setText(str(round(self.vector.y(), 5)))
        self.Z_edit.setText(str(round(self.vector.z(), 5)))

    def x_changed(self, text):
        number = validate_float(text)
        if number is not None:
            self.vector.setX(number)
            self.setVector(self.vector)

    def y_changed(self, text):
        number = validate_float(text)
        if number is not None:
            self.vector.setY(number)
            self.setVector(self.vector)

    def z_changed(self, text):
        number = validate_float(text)
        if number is not None:
            self.vector.setZ(number)
            self.setVector(self.vector)

"""
The UI for editing a primitive objects fields
"""
class PrimitiveEditorWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
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
        self.name_label = QtWidgets.QLabel("Name")
        layout.addWidget(self.name_label)
        self.name_edit_box = QtWidgets.QLineEdit()
        layout.addWidget(self.name_edit_box)
        self.name_edit_box.textChanged.connect(self.name_changed)

        # color field
        self.color_label = QtWidgets.QLabel("Color")
        self.colorButton = QtWidgets.QPushButton(self)
        self.colorButton.clicked.connect(self.open_color_dialog)
        layout.addWidget(self.color_label)
        layout.addWidget(self.colorButton)
        self.color_dialog = QtWidgets.QColorDialog()
        self.color_dialog.currentColorChanged.connect(self.save_selected_color)

        # transform field
        self.transform_label = QtWidgets.QLabel("Position")
        layout.addWidget(self.transform_label)

        self.transform_widget = XYZEditorWidget()
        layout.addWidget(self.transform_widget)

        # quaternion field
        self.quaternion_label = QtWidgets.QLabel("Rotation")
        layout.addWidget(self.quaternion_label)

        self.rotation_widget = XYZEditorWidget()
        layout.addWidget(self.rotation_widget)

        self.listItem = None
        self.primitiveObject = None

    def populate_fields(self, listItem, primitive):
        self.listItem = listItem
        self.primitiveObject = primitive

        self.name_edit_box.setText(primitive.name())
        self.colorButton.setStyleSheet(
            f"background-color:{ primitive.color().name()}")
        
        self.transform_widget.populate_fields(primitive.position(), primitive.setPosition)
        self.rotation_widget.populate_fields(primitive.rotation(), primitive.setRotation)


    def delete_primitive(self):
        
        # TODO: if this is last primitive object, 
        # app freezes until creating a new one 

        # delete from list widget
        listView = self.listItem.listWidget()
        item = listView.takeItem(listView.row(self.listItem))
        item.sceneObject().remove()

        # hide this dialog until it is garbage collected
        self.listItem = None
        self.primitiveObject = None
        self.hide()

    def name_changed(self, text):
        self.primitiveObject.setName(text)
        self.listItem.setName(text)

    def open_color_dialog(self):
        self.color_dialog.open()

    def save_selected_color(self, new_color):
        self.colorButton.setStyleSheet(f"background-color:{new_color.name()}")
        self.primitiveObject.setColor(new_color)

class SphereEditorWidget(PrimitiveEditorWidget):
    def __init__(self):
        PrimitiveEditorWidget.__init__(self)

        self.radius_label = QtWidgets.QLabel("Radius")
        self.radius_edit = QtWidgets.QLineEdit()
        self.radius_edit.textChanged.connect(self.radius_changed)

        self.layout.addWidget(self.radius_label)
        self.layout.addWidget(self.radius_edit)

        self.setLayout(self.layout)
    
    def radius_changed(self, text):
        num = validate_float(text)
        if num is not None:
            self.primitiveObject.setRadius(num)
    
    def populate_fields(self, listItem, primitive):
        super().populate_fields(listItem, primitive)
        self.radius_edit.setText(str(round(self.primitiveObject.radius(), 5)))
        self.show()


class CubeEditorWidget(PrimitiveEditorWidget):
    def __init__(self):
        PrimitiveEditorWidget.__init__(self)

        self.length_label = QtWidgets.QLabel("Length")
        self.width_label = QtWidgets.QLabel("Width")
        self.height_label = QtWidgets.QLabel("Height")

        self.length_edit = QtWidgets.QLineEdit()
        self.width_edit = QtWidgets.QLineEdit()
        self.height_edit = QtWidgets.QLineEdit()

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
    
    def populate_fields(self, listItem, primitive):
        super().populate_fields(listItem, primitive)
        self.length_edit.setText(str(round(self.primitiveObject.length(), 5)))
        self.width_edit.setText(str(round(self.primitiveObject.width(), 5)))
        self.height_edit.setText(str(round(self.primitiveObject.height(), 5)))
        self.show()
    
    def length_changed(self, text):
        num = validate_float(text)
        if num is not None:
            self.primitiveObject.setLength(num)

    def width_changed(self, text):
        num = validate_float(text)
        if num is not None:
            self.primitiveObject.setWidth(num)

    def height_changed(self, text):
        num = validate_float(text)
        if num is not None:
            self.primitiveObject.setHeight(num)
