import sys
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.Qt3DCore import Qt3DCore
from PySide2.Qt3DExtras import Qt3DExtras
from PySide2.Qt3DRender import Qt3DRender
from PySide2.Qt3DInput import Qt3DInput

class QuaternionEditorWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        layout = QtWidgets.QHBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)

        self.W_label = QtWidgets.QLabel("W")
        self.X_label = QtWidgets.QLabel("X")
        self.Y_label = QtWidgets.QLabel("Y")
        self.Z_label = QtWidgets.QLabel("Z")

        self.W_edit = QtWidgets.QLineEdit()
        self.X_edit = QtWidgets.QLineEdit()
        self.Y_edit = QtWidgets.QLineEdit()
        self.Z_edit = QtWidgets.QLineEdit()

        layout.addWidget(self.W_label)
        layout.addWidget(self.W_edit)

        layout.addWidget(self.X_label)
        layout.addWidget(self.X_edit)

        layout.addWidget(self.Y_label)
        layout.addWidget(self.Y_edit)

        layout.addWidget(self.Z_label)
        layout.addWidget(self.Z_edit)

        self.setLayout(layout)
        self.show()


class TransformEditorWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        layout = QtWidgets.QHBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)

        self.X_label = QtWidgets.QLabel("X")
        self.Y_label = QtWidgets.QLabel("Y")
        self.Z_label = QtWidgets.QLabel("Z")

        self.X_edit = QtWidgets.QLineEdit()
        self.Y_edit = QtWidgets.QLineEdit()
        self.Z_edit = QtWidgets.QLineEdit()

        layout.addWidget(self.X_label)
        layout.addWidget(self.X_edit)

        layout.addWidget(self.Y_label)
        layout.addWidget(self.Y_edit)

        layout.addWidget(self.Z_label)
        layout.addWidget(self.Z_edit)

        self.setLayout(layout)
        self.show()


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
        self.transform_label = QtWidgets.QLabel("Transform")
        layout.addWidget(self.transform_label)

        self.transform_widget = TransformEditorWidget()
        layout.addWidget(self.transform_widget)

        # quaternion field
        self.quaternion_label = QtWidgets.QLabel("Quaternion")
        layout.addWidget(self.quaternion_label)
        self.quaternion_widget = QuaternionEditorWidget()
        layout.addWidget(self.quaternion_widget)

        self.show()

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
        self.radius_edit = QtWidgets.QLineEdit()

        self.layout.addWidget(self.radius_label)
        self.layout.addWidget(self.radius_edit)

        self.setLayout(self.layout)
        self.show()


class RectangleEditorWidget(PrimitiveEditorWidget):
    def __init__(self, listItem):
        PrimitiveEditorWidget.__init__(self, listItem)

        self.length_label = QtWidgets.QLabel("Length")
        self.width_label = QtWidgets.QLabel("Width")
        self.height_label = QtWidgets.QLabel("Height")

        self.length_edit = QtWidgets.QLineEdit()
        self.width_edit = QtWidgets.QLineEdit()
        self.height_edit = QtWidgets.QLineEdit()

        self.layout.addWidget(self.length_label)
        self.layout.addWidget(self.length_edit)

        self.layout.addWidget(self.width_label)
        self.layout.addWidget(self.width_edit)

        self.layout.addWidget(self.height_label)
        self.layout.addWidget(self.height_edit)

        self.setLayout(self.layout)
        self.show()
