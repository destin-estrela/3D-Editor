import sys
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.Qt3DCore import Qt3DCore
from PySide2.Qt3DExtras import Qt3DExtras
from PySide2.Qt3DRender import Qt3DRender
from PySide2.Qt3DInput import Qt3DInput

# SOURCE https://stackoverflow.com/questions/60585973/pyside2-qt3d-mesh-does-not-show-up

class SceneModifier(QtCore.QObject):
    def __init__(self, root_entity=None):
        super().__init__()
        self.m_rootEntity = root_entity

        self.cuboid = Qt3DExtras.QCuboidMesh()

        self.cuboidTransform = Qt3DCore.QTransform(
            scale=4.0, translation=QtGui.QVector3D(5.0, -4.0, 0.0),
        )

        self.cuboidMaterial = Qt3DExtras.QPhongMaterial(diffuse=QtGui.QColor("#665423"))

        self.m_cuboidEntity = Qt3DCore.QEntity(self.m_rootEntity)
        self.m_cuboidEntity.addComponent(self.cuboid)
        self.m_cuboidEntity.addComponent(self.cuboidMaterial)
        self.m_cuboidEntity.addComponent(self.cuboidTransform)

        self.sphereMesh = Qt3DExtras.QSphereMesh(rings=20, slices=20, radius=2)

        self.sphereTransform = Qt3DCore.QTransform(
            scale=1.3, translation=QtGui.QVector3D(-5.0, -4.0, 0.0),
        )

        self.sphereMaterial = Qt3DExtras.QPhongMaterial(diffuse=QtGui.QColor("#a69929"))

        self.m_sphereEntity = Qt3DCore.QEntity(self.m_rootEntity)
        self.m_sphereEntity.addComponent(self.sphereMesh)
        self.m_sphereEntity.addComponent(self.sphereMaterial)
        self.m_sphereEntity.addComponent(self.sphereTransform)

    @QtCore.Slot(bool)
    def enableCuboid(self, enabled):
        self.m_cuboidEntity.setEnabled(enabled)

    @QtCore.Slot(bool)
    def enableSphere(self, enabled):
        self.m_sphereEntity.setEnabled(enabled)


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
    camController

    modifier = SceneModifier(rootEntity)

    view.setRootEntity(rootEntity)

    info = QtWidgets.QCommandLinkButton()
    info.setText("3D Editor")
    
    info.setIconSize(QtCore.QSize(0, 0))


    cuboidCB = QtWidgets.QCheckBox(widget)
    cuboidCB.setChecked(True)
    cuboidCB.setText("Cuboid")

    sphereCB = QtWidgets.QCheckBox(widget)
    sphereCB.setChecked(True)
    sphereCB.setText("Sphere")

    vLayout.addWidget(info)
    vLayout.addWidget(cuboidCB)
    vLayout.addWidget(sphereCB)

    cuboidCB.stateChanged.connect(modifier.enableCuboid)
    sphereCB.stateChanged.connect(modifier.enableSphere)

    cuboidCB.setChecked(True)
    sphereCB.setChecked(True)

    widget.show()
    widget.resize(1200, 800)

    sys.exit(app.exec_())