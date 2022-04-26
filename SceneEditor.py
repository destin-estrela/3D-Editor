import sys
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.Qt3DCore import Qt3DCore
from PySide2.Qt3DExtras import Qt3DExtras
from PySide2.Qt3DRender import Qt3DRender
from PySide2.Qt3DInput import Qt3DInput
from Primitives import * 
from PrimitiveEditorWidgets import * 

# SOURCES: Anything besides QT documentation listed here 
# https://stackoverflow.com/questions/60585973/pyside2-qt3d-mesh-does-not-show-up
# https://wiki.qt.io/Qt_for_Python_Tutorial_ClickableButton
# https://stackoverflow.com/questions/38923978/object-going-out-of-scope-and-being-garbage-collected-in-pyside-pyqt
# https://stackoverflow.com/questions/49385525/adding-items-to-qlistview
# https://zetcode.com/gui/pysidetutorial/
# https://stackoverflow.com/questions/4625102/how-to-replace-a-widget-with-another-using-qt
# https://stackoverflow.com/questions/33793315/how-to-use-spacers-in-qt

class PrimitiveListItem(QtWidgets.QListWidgetItem):
      def __init__(self, name, sceneObject):
        super().__init__(name)
        self.sceneObject = sceneObject
        self.name = name

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


class SceneEditor(QtCore.QObject):
    def __init__(self, root_entity=None, cameraEntity=None, objectListWidget=None, mainLayout=None):
        super().__init__()
        self.mainLayout = mainLayout
        self.m_rootEntity = root_entity
        self.m_cameraEntity = cameraEntity
        self.m_objectListWidget = objectListWidget
        self.m_currentPrimitiveObjectEditor = None

        # connect list widget to functionality
        self.m_objectListWidget.itemClicked.connect(self.activate_primitive_editor)

    def createCube(self):
        cube = Cube(self.m_rootEntity, self.m_cameraEntity)
        cube.persist()
        cubeListItem = CubeListItem(cube.m_displayName, cube)
        self.activate_primitive_editor(cubeListItem)
        self.m_objectListWidget.addItem(cubeListItem)

    def createSphere(self):
        sphere = Sphere(self.m_rootEntity, self.m_cameraEntity)
        sphere.persist()
        sphereListItem = SphereListItem(sphere.m_displayName, sphere)
        self.activate_primitive_editor(sphereListItem)
        self.m_objectListWidget.addItem(sphereListItem)
    
    def activate_primitive_editor(self, item):
        newWidget = item.activate_primitive_editor()
        if self.m_currentPrimitiveObjectEditor:
            self.m_currentPrimitiveObjectEditor.deleteLater()

        self.mainLayout.addWidget(newWidget)
        self.m_currentPrimitiveObjectEditor = newWidget

       
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
    
    ##
    rightWindow = QtWidgets.QVBoxLayout()
    rightWindow.setAlignment(QtCore.Qt.AlignTop)

    hLayout.addLayout(rightWindow)
    hLayout.addWidget(container, 1)

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

    modifier = SceneEditor(rootEntity, cameraEntity, objectList, hLayout)

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