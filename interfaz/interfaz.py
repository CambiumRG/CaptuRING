# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap


class Ui_interfaz(object):
    def setupUi(self, interfaz, data):
        interfaz.setObjectName("CaptuRinG")
        interfaz.resize(480, 620)

        interfaz.setWindowIcon(QtGui.QIcon('icon.png'))

        self.imageL = QtWidgets.QLabel(interfaz)
        self.imageL.setGeometry(QtCore.QRect(10, 400, 200, 80))
        # loading image
        self.pixmap = QPixmap('CambiumLarge.jpg')
        self.scaledImg = self.pixmap.scaledToWidth(100)
        self.imageL.setPixmap(self.scaledImg)

        self.addressL = QtWidgets.QLabel(interfaz)
        self.addressL.setGeometry(QtCore.QRect(12, 450, 300, 40))
        self.urlLink = "<a href=\"http://www.cambiumresearch.eu\">Cambium RG</a>"
        self.addressL.setOpenExternalLinks(True)
        self.addressL.setObjectName("addressL")

        self.myFont = QtGui.QFont()  # Font type for titles
        self.myFont.setBold(True)

        self.shootingL = QtWidgets.QLabel(interfaz)
        self.shootingL.setGeometry(QtCore.QRect(10, 10, 300, 40))
        self.shootingL.setObjectName("shootingL")
        self.shootingL.setFont(self.myFont)

        self.optionsL = QtWidgets.QLabel(interfaz)
        self.optionsL.setGeometry(QtCore.QRect(320, 10, 300, 40))
        self.optionsL.setObjectName("optionsL")
        self.optionsL.setFont(self.myFont)

        # Frame Shooting
        self.frame = QtWidgets.QFrame(interfaz)
        self.frame.setGeometry(QtCore.QRect(10, 50, 300, 320))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.frame.setObjectName("frame")

        # Core Name
        self.nameCoreL = QtWidgets.QLabel(self.frame)
        self.nameCoreL.setGeometry(QtCore.QRect(30, 20, 165, 40))
        self.nameCoreL.setObjectName("nameCoreL")

        self.nameCore = QtWidgets.QLineEdit(self.frame)
        self.nameCore.setGeometry(QtCore.QRect(30, 55, 130, 35))
        self.nameCore.setObjectName("nameCore")

        # New nameCore button
        self.newcoreName = QtWidgets.QPushButton(self.frame)
        self.newcoreName.setGeometry(QtCore.QRect(180, 55, 90, 35))
        self.newcoreName.setObjectName("newcoreName")

        # sampleSize
        self.sampleSizeLabel = QtWidgets.QLabel(self.frame)
        self.sampleSizeLabel.setGeometry(QtCore.QRect(30, 100, 165, 30))
        self.sampleSizeLabel.setObjectName("sampleSizeLabel")

        self.tamanioMuestra = QtWidgets.QSpinBox(self.frame)
        self.tamanioMuestra.setGeometry(QtCore.QRect(30, 135, 130, 30))
        self.tamanioMuestra.setMaximum(99999)
        self.tamanioMuestra.setObjectName("tamanioMuestra")
        self.tamanioMuestra.setValue(data[4])

        # Create Sample button

        self.crearMuestra = QtWidgets.QPushButton(self.frame)
        self.crearMuestra.setGeometry(QtCore.QRect(60, 210, 180, 60))
        # Disabled until the user provides and confirms a sample name
        self.crearMuestra.setEnabled(False)
        self.crearMuestra.setToolTip("Provide a sample name and press 'Name It!' to enable capture")
        # NOTE: setStyleSheet is not called here intentionally
        # self.crearMuestra.setStyleSheet
        self.crearMuestra.setObjectName("crearMuestra")

        # FRAME02 Options

        self.frame_2 = QtWidgets.QFrame(interfaz)
        self.frame_2.setGeometry(QtCore.QRect(320, 50, 140, 430))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        # offset
        self.offsetLabel = QtWidgets.QLabel(self.frame_2)
        self.offsetLabel.setGeometry(QtCore.QRect(10, 5, 120, 30))
        self.offsetLabel.setObjectName("offsetLabel")

        self.offset = QtWidgets.QSpinBox(self.frame_2)
        self.offset.setGeometry(QtCore.QRect(10, 40, 120, 30))
        self.offset.setMaximum(99999)
        self.offset.setObjectName("offset")
        self.offset.setValue(data[1])

        # speed/step
        self.spstepLabel = QtWidgets.QLabel(self.frame_2)
        self.spstepLabel.setGeometry(QtCore.QRect(10, 75, 120, 30))
        self.spstepLabel.setObjectName("spstepLabel")

        self.stepSpeed = QtWidgets.QSpinBox(self.frame_2)
        self.stepSpeed.setGeometry(QtCore.QRect(10, 100, 120, 30))
        self.stepSpeed.setMaximum(99999)
        self.stepSpeed.setObjectName("stepSpeed")
        self.stepSpeed.setValue(data[2])

        # Initial speed
        self.inSpeedLabel = QtWidgets.QLabel(self.frame_2)
        self.inSpeedLabel.setGeometry(QtCore.QRect(10, 135, 120, 30))
        self.inSpeedLabel.setObjectName("inSpeedLabel")

        self.initSpeed = QtWidgets.QSpinBox(self.frame_2)
        self.initSpeed.setGeometry(QtCore.QRect(10, 170, 120, 30))
        self.initSpeed.setMaximum(99999)
        self.initSpeed.setObjectName("initSpeed")
        self.initSpeed.setValue(data[3])

        ######
        #####

        # sizeStep
        self.sizeStepLabel = QtWidgets.QLabel(self.frame_2)
        self.sizeStepLabel.setGeometry(QtCore.QRect(10, 205, 120, 30))
        self.sizeStepLabel.setObjectName("sizeStepLabel")

        self.sizeStep = QtWidgets.QSpinBox(self.frame_2)
        self.sizeStep.setGeometry(QtCore.QRect(10, 240, 120, 30))
        self.sizeStep.setObjectName("sizeStep")
        self.sizeStep.setMaximum(99999)
        self.sizeStep.setValue(data[5])

        # spindleSize
        self.spindleSizeLabel = QtWidgets.QLabel(self.frame_2)
        self.spindleSizeLabel.setGeometry(QtCore.QRect(10, 275, 120, 30))
        self.spindleSizeLabel.setObjectName("spindleSizeLabel")

        self.tamanioHusillo = QtWidgets.QSpinBox(self.frame_2)
        self.tamanioHusillo.setGeometry(QtCore.QRect(10, 310, 120, 30))
        self.tamanioHusillo.setMaximum(99999)
        self.tamanioHusillo.setObjectName("tamanioHusillo")
        self.tamanioHusillo.setValue(data[6])

        # Platform
        self.platformLabel = QtWidgets.QLabel(self.frame_2)
        self.platformLabel.setGeometry(QtCore.QRect(10, 345, 120, 30))
        self.platformLabel.setObjectName("platformLabel")

        self.platform = QtWidgets.QSpinBox(self.frame_2)
        self.platform.setGeometry(QtCore.QRect(10, 380, 120, 30))
        self.platform.setMaximum(99999)
        self.platform.setObjectName("platform")
        self.platform.setValue(data[7])

        # Sample Size Y (2D scanning)
        self.sampleSizeYLabel = QtWidgets.QLabel(self.frame_2)
        self.sampleSizeYLabel.setGeometry(QtCore.QRect(10, 5, 120, 30))
        self.sampleSizeYLabel.setObjectName("sampleSizeYLabel")

        # Extend frame_2 to accommodate new controls
        self.frame_2.setGeometry(QtCore.QRect(320, 50, 140, 520))

        # Reorganize Y-axis controls in a scrollable area or extend downward
        self.sampleSizeYLabel.setGeometry(QtCore.QRect(10, 425, 120, 30))
        self.tamanioMuestraY = QtWidgets.QSpinBox(self.frame_2)
        self.tamanioMuestraY.setGeometry(QtCore.QRect(10, 460, 120, 30))
        self.tamanioMuestraY.setMaximum(99999)
        self.tamanioMuestraY.setObjectName("tamanioMuestraY")
        self.tamanioMuestraY.setValue(data[8])

        # Step Size Y
        self.sizeStepYLabel = QtWidgets.QLabel(self.frame_2)
        self.sizeStepYLabel.setGeometry(QtCore.QRect(10, 495, 120, 30))
        self.sizeStepYLabel.setObjectName("sizeStepYLabel")

        self.sizeStepY = QtWidgets.QSpinBox(self.frame_2)
        self.sizeStepY.setGeometry(QtCore.QRect(10, 530, 120, 30))
        self.sizeStepY.setObjectName("sizeStepY")
        self.sizeStepY.setMaximum(99999)
        self.sizeStepY.setValue(data[9])

        self.retranslateUi(interfaz)

        QtCore.QMetaObject.connectSlotsByName(interfaz)

    def retranslateUi(self, interfaz):
        _translate = QtCore.QCoreApplication.translate
        interfaz.setWindowTitle(_translate("CaptuRing", "CaptuRING"))
        self.imageL.show()

        self.addressL.setText(_translate("CaptuRing", self.urlLink))

        self.shootingL.setText(_translate("CaptuRing", "Image Shooting"))
        self.optionsL.setText(_translate("CaptuRing", "Options"))

        self.nameCoreL.setText(_translate("CaptuRing", "Sample Name"))

        self.newcoreName.setText(_translate("CaptuRing", "Name It!"))

        self.sampleSizeLabel.setText(
            _translate("CaptuRing", "Sample size (mm)"))
        self.offsetLabel.setText(_translate("CaptuRing", "Offset"))
        self.spindleSizeLabel.setText(_translate("CaptuRing", "Spindle size"))
        self.sizeStepLabel.setText(_translate("CaptuRing", "Step size"))
        self.crearMuestra.setText(_translate("CaptuRing", "CAPTURE"))
        self.platformLabel.setText(_translate("CaptuRing", "Platform"))
        self.spstepLabel.setText(_translate("CaptuRing", "Speed/step"))
        self.inSpeedLabel.setText(_translate("CaptuRing", "Initial speed"))
        self.sampleSizeYLabel.setText(_translate("CaptuRing", "Sample size Y (mm)"))
        self.sizeStepYLabel.setText(_translate("CaptuRing", "Step size Y"))
