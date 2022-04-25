import sys
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.Qt3DCore import Qt3DCore
from PySide2.Qt3DExtras import Qt3DExtras
from PySide2.Qt3DRender import Qt3DRender
from PySide2.Qt3DInput import Qt3DInput

# SOURCES: Anything besides QT documentation listed here 
# https://stackoverflow.com/questions/60585973/pyside2-qt3d-mesh-does-not-show-up
# https://wiki.qt.io/Qt_for_Python_Tutorial_ClickableButton
# https://stackoverflow.com/questions/38923978/object-going-out-of-scope-and-being-garbage-collected-in-pyside-pyqt
# https://stackoverflow.com/questions/49385525/adding-items-to-qlistview
# https://zetcode.com/gui/pysidetutorial/

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

class ObjectEditor(QtCore.QObject):
    def __init__(self, root_entity=None, cameraEntity=None, objectListWidget=None):
        super().__init__()
        self.m_rootEntity = root_entity
        self.m_cameraEntity = cameraEntity
        self.m_objectListWidget = objectListWidget
        self.m_objectDict = {}

    def createCube(self):
        cube = Cube(self.m_rootEntity, self.m_cameraEntity)
        self.m_objectDict[cube.m_displayName] = cube 
        self.m_objectListWidget.addItem(cube.m_displayName)

    def createSphere(self):
        sphere = Sphere(self.m_rootEntity, self.m_cameraEntity)
        self.m_objectDict[sphere.m_displayName] = sphere
        self.m_objectListWidget.addItem(sphere.m_displayName)

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
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout = layout 
        self.setLayout(layout)

        # name field
        self.name = QtWidgets.QLabel("Object Name")
        layout.addWidget(self.name)
        self.name_edit_box = QtWidgets.QLineEdit()
        layout.addWidget(self.name_edit_box)

        # color field
        self.label = QtWidgets.QLabel("Color")
        self.colorButton = QtWidgets.QPushButton(self)
        self.colorButton.clicked.connect(self.open_color_dialog)

        layout.addWidget(self.label)
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

        self.name_edit_box.textChanged.connect(self.line_edit_text_changed)

        self.show()
    
    def line_edit_text_changed(self, text):
        self.label.setText(text)
    
    def open_color_dialog(self):
        self.color_dialog.open()

    def save_selected_color(self, new_color):
        self.colorButton.setStyleSheet(f"background-color:{new_color.name()}")

class SphereEditor(PrimitiveEditorWidget):
    def __init__(self):
        PrimitiveEditorWidget.__init__(self)

        self.radius_label = QtWidgets.QLabel("Radius")
        self.radius_edit = QtWidgets.QLineEdit()

        self.layout.addWidget(self.radius_label)
        self.layout.addWidget(self.radius_edit)

        self.setLayout(self.layout)
        self.show()


class RectangleEditor(PrimitiveEditorWidget):
    def __init__(self):
        PrimitiveEditorWidget.__init__(self)

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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    view = Qt3DExtras.Qt3DWindow()
    view.defaultFrameGraph().setClearColor(QtGui.QColor("#4d4d4f"))
    container = QtWidgets.QWidget.createWindowContainer(view)
    screenSize = view.screen().size()
    container.setMinimumSize(QtCore.QSize(200, 100))
    container.setMaximumSize(screenSize)

    widget = QtWidgets.QWidget()
    hLayout = QtWidgets.QHBoxLayout(widget)
    
    # leftWindow = PrimitiveEditorWidget()
    leftWindow = SphereEditor()

    rightWindow = QtWidgets.QVBoxLayout()
    rightWindow.setAlignment(QtCore.Qt.AlignTop)

    hLayout.addWidget(leftWindow)
    hLayout.addWidget(container, 1)
    hLayout.addLayout(rightWindow)

    widget.setWindowTitle("3D Editor")

    input_ = Qt3DInput.QInputAspect()
    view.registerAspect(input_)

    rootEntity = Qt3DCore.QEntity()

    cameraEntity = view.camera()
    cameraEntity.lens().setPerspectiveProjection(45.0, 16.0 / 9.0, 0.1, 1000.0)
    cameraEntity.setPosition(QtGui.QVector3D(0, 0, 20.0))
    cameraEntity.setUpVector(QtGui.QVector3D(0, 1, 0))
    cameraEntity.setViewCenter(QtGui.QVector3D(0, 0, 0))

    lightEntity = Qt3DCore.QEntity(rootEntity)
    light = Qt3DRender.QPointLight(lightEntity)
    light.setColor("white")
    light.setIntensity(1)
    lightEntity.addComponent(light)

    lightTransform = Qt3DCore.QTransform(lightEntity)
    lightTransform.setTranslation(cameraEntity.position())
    lightEntity.addComponent(lightTransform)

    camController = Qt3DExtras.QOrbitCameraController(rootEntity)
    camController.setCamera(cameraEntity)
    objectList = QtWidgets.QListWidget(widget)

    modifier = ObjectEditor(rootEntity, cameraEntity, objectList)

    view.setRootEntity(rootEntity)


    info = QtWidgets.QCommandLinkButton()
    info.setText("Objects")
    
    info.setIconSize(QtCore.QSize(0, 0))

    createCubeButton = QtWidgets.QPushButton(widget)
    createCubeButton.setText("Create Cube")

    createSphereButton = QtWidgets.QPushButton(widget)
    createSphereButton.setText("Create Sphere")

    rightWindow.addWidget(info)
    rightWindow.addWidget(createCubeButton)
    rightWindow.addWidget(createSphereButton)
    rightWindow.addWidget(objectList)

    createCubeButton.clicked.connect(modifier.createCube)

    createSphereButton.clicked.connect(modifier.createSphere)

    widget.show()
    widget.resize(1200, 800)

    sys.exit(app.exec_())