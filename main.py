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

class Sphere(QtCore.QObject):
    sphereTag = 1
    def __init__(self, root_entity=None, cameraEntity=None):
        super().__init__()
        self.m_rootEntity = root_entity
        self.m_cameraEntity = cameraEntity
        self.m_defaultMaterial = Qt3DExtras.QPhongMaterial(
            diffuse=QtGui.QColor("#665423"))
       
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
        

class Cube(QtCore.QObject):
    cubeTag = 1
    def __init__(self, root_entity=None, cameraEntity=None):
        super().__init__()
        self.m_rootEntity = root_entity
        self.m_cameraEntity = cameraEntity
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

class SceneModifier(QtCore.QObject):
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
    vLayout = QtWidgets.QVBoxLayout()
    vLayout.setAlignment(QtCore.Qt.AlignTop)
    hLayout.addWidget(container, 1)
    hLayout.addLayout(vLayout)

    widget.setWindowTitle("Basic shapes")

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

    modifier = SceneModifier(rootEntity, cameraEntity, objectList)
    print(cameraEntity.position)

    view.setRootEntity(rootEntity)

    info = QtWidgets.QCommandLinkButton()
    info.setText("3D Editor")
    
    info.setIconSize(QtCore.QSize(0, 0))

    createCubeButton = QtWidgets.QPushButton(widget)
    createCubeButton.setText("Create Cube")

    createSphereButton = QtWidgets.QPushButton(widget)
    createSphereButton.setText("Create Sphere")


    vLayout.addWidget(info)
    vLayout.addWidget(createCubeButton)
    vLayout.addWidget(createSphereButton)
    vLayout.addWidget(objectList)

    createCubeButton.clicked.connect(modifier.createCube)

    createSphereButton.clicked.connect(modifier.createSphere)

    widget.show()
    widget.resize(1200, 800)

    sys.exit(app.exec_())