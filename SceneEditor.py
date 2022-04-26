import sys
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.Qt3DCore import Qt3DCore
from PySide2.Qt3DExtras import Qt3DExtras
from PySide2.Qt3DRender import Qt3DRender
from PySide2.Qt3DInput import Qt3DInput
from Primitives import *
from PrimitiveEditorWidgets import *
from PrimitiveListItems import *

# SOURCES: Anything besides QT documentation listed here
# https://www.tutorialspoint.com/pyqt/pyqt_qstackedwidget.htm
# https://stackoverflow.com/questions/60585973/pyside2-qt3d-mesh-does-not-show-up
# https://wiki.qt.io/Qt_for_Python_Tutorial_ClickableButton
# https://stackoverflow.com/questions/38923978/object-going-out-of-scope-and-being-garbage-collected-in-pyside-pyqt
# https://stackoverflow.com/questions/49385525/adding-items-to-qlistview
# https://zetcode.com/gui/pysidetutorial/
# https://stackoverflow.com/questions/4625102/how-to-replace-a-widget-with-another-using-qt
# https://stackoverflow.com/questions/33793315/how-to-use-spacers-in-qt


class ShapeEditor(QtCore.QObject):
    def __init__(self, rootEntity, cameraEntity, objectListWidget, stackedLayout):
        super().__init__()
        self.stackedLayout = stackedLayout
        self.m_rootEntity = rootEntity
        self.m_cameraEntity = cameraEntity
        self.m_objectListWidget = objectListWidget

        # connect list widget to functionality
        self.m_objectListWidget.itemActivated.connect(
            self.initPrimitiveEditorWidget)
        # connect list widget to functionality
        self.m_objectListWidget.itemClicked.connect(
            self.initPrimitiveEditorWidget)
         # connect list widget to functionality
        self.m_objectListWidget.itemDoubleClicked.connect(
            self.initPrimitiveEditorWidget)
        self.m_objectListWidget.itemEntered.connect(
            self.initPrimitiveEditorWidget)

    def createCube(self):
        cube = Cube(self.m_rootEntity, self.m_cameraEntity)
        cubeListItem = CubeListItem(cube.m_displayName, cube)
        self.initPrimitiveEditorWidget(cubeListItem)
        self.m_objectListWidget.addItem(cubeListItem)
        return cubeListItem

    def createSphere(self):
        sphere = Sphere(self.m_rootEntity, self.m_cameraEntity)
        sphereListItem = SphereListItem(sphere.m_displayName, sphere)
        self.initPrimitiveEditorWidget(sphereListItem)
        self.m_objectListWidget.addItem(sphereListItem)
        return sphereListItem

    def initPrimitiveEditorWidget(self, item):
        self.stackedLayout.openPrimitiveEditor(item)

    """
    Creates and populates editor with persisted primitive objects
    """
    def restoreData(self):
        database = db.getDb(PRIMITIVE_OBJECTS)
        json_data = database.getAll()

        for primitive in json_data:
            if primitive['type'] == 'cube':
                cube = Cube(self.m_rootEntity,
                            self.m_cameraEntity, primitive['id'])
                listItem = CubeListItem(cube.m_displayName, cube)
                cube.restore(primitive)
            elif primitive['type'] == 'sphere':
                sphere = Sphere(self.m_rootEntity,
                                self.m_cameraEntity, primitive['id'])
                listItem = SphereListItem(sphere.m_displayName, sphere)
                sphere.restore(primitive)
            else:
                print("Found invalid object in database")
                continue

            listItem.setName(primitive['name'])
            self.m_objectListWidget.addItem(listItem)


class RightSideMenu(QtWidgets.QWidget):

    PRIMITIVE_MAP = {'sphere': 1, 'cube': 2}

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(layout)
        self.stackWidget = QtWidgets.QStackedWidget(self)
        self.setMinimumSize(300, 300)
        self.setMaximumWidth(300)


        self.sphereEditor = SphereEditorWidget()
        self.boxEditor = CubeEditorWidget()
        self.emptyWidget = QtWidgets.QWidget()

        self.stackWidget.addWidget(self.emptyWidget)
        self.stackWidget.addWidget(self.sphereEditor)
        self.stackWidget.addWidget(self.boxEditor)

        layout.addWidget(self.stackWidget, 1)

    def openPrimitiveEditor(self, listItem):
        primObj = listItem.sceneObject()
        self.stackWidget.setCurrentIndex(self.PRIMITIVE_MAP[primObj.primitiveType()])
        self.stackWidget.currentWidget().populate_fields(listItem, primObj)


class LeftSideMenu(QtWidgets.QWidget):
    def __init__(self, shapeEditor, objectList):
        QtWidgets.QWidget.__init__(self)
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(layout)
        self.setMinimumSize(300, 300)
        self.setMaximumWidth(300)

        # buttons to create primitives
        self.createCubeButton = QtWidgets.QPushButton(self)
        self.createCubeButton.setText("Create Cube")
        self.createSphereButton = QtWidgets.QPushButton(self)
        self.createSphereButton.setText("Create Sphere")

        self.createCubeButton.clicked.connect(shapeEditor.createCube)
        self.createSphereButton.clicked.connect(shapeEditor.createSphere)

        layout.addWidget(self.createCubeButton)
        layout.addWidget(self.createSphereButton)
        layout.addWidget(objectList)



class Application(QtWidgets.QWidget):
    def __init__(self, rootEntity, cameraEntity, container):
        QtWidgets.QWidget.__init__(self)
        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)
        self.rootEntity = rootEntity
        self.container = container
        self.cameraEntity = cameraEntity
        self.rightMenu = RightSideMenu()
        self.objectList = QtWidgets.QListWidget(self)
        self.shapeEditor = ShapeEditor(
            self.rootEntity, self.cameraEntity, self.objectList, self.rightMenu)
        self.leftMenu = LeftSideMenu(self.shapeEditor, self.objectList)

        layout.addWidget(self.leftMenu, 1)
        layout.addWidget(self.container, 1)
        layout.addWidget(self.rightMenu, 1)

        self.shapeEditor.restoreData()

        self.setWindowTitle("3D Editor")
        self.resize(1200, 800)
        self.show()


def initialize_camera(view, rootEntity):
    cameraEntity = view.camera()
    cameraEntity.lens().setPerspectiveProjection(45.0, 16.0 / 9.0, 0.1, 1000.0)
    cameraEntity.setPosition(QtGui.QVector3D(0, 0, 20.0))
    cameraEntity.setUpVector(QtGui.QVector3D(0, 1, 0))
    cameraEntity.setViewCenter(QtGui.QVector3D(0, 0, 0))
    camController = Qt3DExtras.QOrbitCameraController(rootEntity)
    camController.setCamera(cameraEntity)
    return cameraEntity


def initialize_lighting(rootEntity, cameraEntity):
    lightEntity = Qt3DCore.QEntity(rootEntity)
    light = Qt3DRender.QPointLight(lightEntity)
    light.setColor("white")
    light.setIntensity(1)
    lightEntity.addComponent(light)

    lightTransform = Qt3DCore.QTransform(lightEntity)
    lightTransform.setTranslation(cameraEntity.position())
    lightEntity.addComponent(lightTransform)
    return lightEntity


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # init 3D environment
    view = Qt3DExtras.Qt3DWindow()
    view.defaultFrameGraph().setClearColor(QtGui.QColor("#4d4d4f"))
    container = QtWidgets.QWidget.createWindowContainer(view)
    screenSize = view.screen().size()
    container.setMinimumSize(QtCore.QSize(800, 800))
    container.setMaximumSize(screenSize)

    rootEntity = Qt3DCore.QEntity()
    cameraEntity = initialize_camera(view, rootEntity)
    lightEntity = initialize_lighting(rootEntity, cameraEntity)
    view.setRootEntity(rootEntity)

    # init input
    input_ = Qt3DInput.QInputAspect()
    view.registerAspect(input_)

    # init app
    appWidget = Application(rootEntity, cameraEntity, container)

    sys.exit(app.exec_())
