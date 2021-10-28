from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from interfaz.interfaz import Ui_interfaz
from db.controllerDB import createDataBase, getParams, changeData
# from stitcher.stitcher import stitcherMain
from arduino.pruebaSerial import placeSample, takeSamples
import sqlite3, os, base64, serial
from tkinter import Tk
from tkinter.filedialog import askopenfilenames, askdirectory


class WindInterfaz(qtw.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_interfaz()
        params = getParams()
        self.ui.setupUi(self, params)
     
        #control parameters
        self.ui.offset.valueChanged.connect(lambda: changeData( "OFFSET", self.ui.offset.value()))
        self.ui.stepSpeed.valueChanged.connect(lambda: changeData( "SPEED_STEP", self.ui.stepSpeed.value()))
        self.ui.initSpeed.valueChanged.connect(lambda: changeData( "INITIAL_SPEED", self.ui.initSpeed.value()))
        self.ui.tamanioMuestra.valueChanged.connect(lambda: changeData( "SAMPLE_SIZE", self.ui.tamanioMuestra.value()))
        self.ui.sizeStep.valueChanged.connect(lambda: changeData( "SIZE_STEP", self.ui.sizeStep.value()))
        self.ui.tamanioHusillo.valueChanged.connect(lambda: changeData( "SPINDLE_SIZE", self.ui.tamanioHusillo.value()))
        self.ui.platform.valueChanged.connect(lambda: changeData( "PLATFORM", self.ui.platform.value()))
        self.ui.newcoreName.clicked.connect(self.coreNamef)
        self.ui.crearMuestra.clicked.connect(lambda: self.createSample())
        
        #image control
        #self.ui.panoramasList.currentIndexChanged.connect(lambda: self.selectPanorama())
        #self.ui.panoramasList.currentIndexChanged.connect(lambda: self.updateImages())
        #self.ui.imagenesList.currentIndexChanged.connect(lambda: self.selectImg())
        #self.ui.obtainImg.clicked.connect(lambda: self.obtain())
        #self.ui.addImg.clicked.connect(lambda: self.addImg())
        #self.ui.removeImg.clicked.connect(lambda: self.remove())
        #self.ui.newPanorama.clicked.connect(lambda: self.addPanorama())
        
        #self.ui.newcoreName.clicked.connect(self.coreNamef)
        #self.ui.stitch.clicked.connect(lambda: self.stitchImgs())
        #self.updatePanoramas()
        #self.showImg("interfaz/no-image.png")

      
    def coreNamef(self):
        global coreName
        coreName = self.ui.nameCore.text()
        
        if coreName.strip() == "" or coreName.strip() == "None":
            qtw.QMessageBox.critical(self, "Fail", "No valid name for the core.")
        else:
            try:
                os.mkdir("Outputs/" + coreName)
            except OSError as error:
               qtw.QMessageBox.critical(self, "Fail", "This name is duplicated. Are you sure to continue?")     
        
    #image control show img selected still awaits
#     def showImg(self, img):
#         if type(img) is bytes:
#             qimg = qtg.QImage.fromData(img)
#             image = qtg.QPixmap.fromImage(qimg)
#         else:
#             image = qtg.QPixmap(img)
#         image = image.scaledToHeight(481)
#         scene = qtw.QGraphicsScene()
#         scene.addPixmap(image)
        #self.ui.previewMuestra.setScene(scene)

#     def addPanorama(self):
#         name= self.ui.nombreMuestra.text()
#         if name.strip() == "" or name.strip() == "None":
#             qtw.QMessageBox.critical(self, "Fail", "No valid name for the sample.")
#         else:
#             panoramas = getPanoramas()
#             aux=True
#             for pano in panoramas:
#                 if pano[1].strip() == name.strip():
#                     qtw.QMessageBox.critical(self, "Duplicate", "There is already a sample with that name.")
#                     aux=False
#             if aux:
#                 insertPanorama( name, -1)
#                 self.updatePanoramas()
#                 self.updateImages()

#     def updatePanoramas(self):
#         panoramas = getPanoramas()
#         self.ui.panoramasList.clear()
#         self.ui.panoramasList.addItem("None")
#         if len(panoramas) != 0:
#             for pano in panoramas:
#                 self.ui.panoramasList.addItem(pano[1])
                
    
#     def updateImages(self):
#         self.ui.imagenesList.clear()
#         print("UpdateImgs")
#         if self.ui.panoramasList.currentText() != "None":
#             panoramas = getPanoramas()
#             for pano in panoramas:
#                 if self.ui.panoramasList.currentText() == pano[1]:
#                     images = getImgs( pano[0])
#                     self.ui.imagenesList.addItem("None")
#                     if len(images) != 0:
#                         for img in images:
#                             self.ui.imagenesList.addItem(img[2])

#     def addImg(self):
#         panoramaName = self.ui.panoramasList.currentText()
#         if panoramaName == "None":
#             qtw.QMessageBox.critical(self, "None", "Select a panorama first.")
#         else:
#             Tk().withdraw()
#             images = askopenfilenames(filetypes=[('Images', '.jpg'),('Images', '.JPG'),  ('Images', '.png')],
#                                         title='Select the image/s')
#             panoramas = getPanoramas()
#             for pano in panoramas:
#                 if self.ui.panoramasList.currentText() == pano[1]:
#                     aux=True
#                     imagesDB = getImgs( pano[0])
#                     for imgs in imagesDB:
#                         for img in images:
#                             paths, name = os.path.split(img)
#                             if imgs[2] == name:
#                                 qtw.QMessageBox.critical(self, "Duplicate", "There is already an image with the name " + name + ".")
#                                 aux=False
#                     if aux:
#                         for img in images:
#                             paths, name = os.path.split(img)
#                             insertImg( pano[0], img, name)
#                         self.updateImages()
                    
#     def obtain(self):
#         if self.ui.panoramasList.currentText() == "None":
#             qtw.QMessageBox.critical(self, "None", "Select a panorama first.")
#         elif self.ui.imagenesList.currentText() == "None":
#             self.obtainPanorama()
#         else:
#             self.obtainImage()
    
#     def obtainImage(self):
#         Tk().withdraw()
#         folder = askdirectory(title='Select the folder to store the image')
#         imgName = self.ui.imagenesList.currentText()
#         panoramas = getPanoramas()
#         for pano in panoramas:
#             if self.ui.panoramasList.currentText() == pano[1]:
#                 imagesDB = getImgs( pano[0])
#                 for imgs in imagesDB:
#                     if self.ui.imagenesList.currentText() == imgs[2]:
#                         with open(folder+"/"+imgs[2], "wb") as fh:
#                             fh.write(imgs[3])

#     def obtainPanorama(self):
#         aux=True
#         panoramas = getPanoramas()
#         for pano in panoramas:
#             if self.ui.panoramasList.currentText() == pano[1]:
#                 if pano[2] != -1:
#                     aux=False
#                     Tk().withdraw()
#                     folder = askdirectory(title='Select the folder to store the image')
#                     stImg= getStitched( pano[2])
#                     with open(folder+"/"+pano[1], "wb") as fh:
#                             fh.write(stImg[1])
#         if aux:
#             qtw.QMessageBox.critical(self, "Empty", "There is no panorama.")
# 
#     def selectPanorama(self):
#         print("selectPano")
#         if self.ui.panoramasList.currentText() != "None":
#             panoramas = getPanoramas()
#             for pano in panoramas:
#                 if self.ui.panoramasList.currentText() == pano[1]:
#                     if pano[2] != -1:
#                         stImg= getStitched( pano[2])
#                         self.showImg(stImg[1])
#                     else:
#                         self.showImg("interfaz/no-image.png")
#         else:
#             self.showImg("interfaz/no-image.png")
#                   
#     def selectImg(self):
#         print("selectIMG")
#         if self.ui.imagenesList.currentText() != "None":
#             panoramas = getPanoramas()
#             for pano in panoramas:
#                 if self.ui.panoramasList.currentText() == pano[1]:
#                     imagesDB = getImgs( pano[0])
#                     for imgs in imagesDB:
#                         if self.ui.imagenesList.currentText() == imgs[2]:
#                             self.showImg(imgs[3])
#         else: 
#             self.selectPanorama()
#     
#     def stitchImgs(self):
#         panoramas = getPanoramas()
#         for pano in panoramas:
#             if self.ui.panoramasList.currentText() == pano[1]:
#                 if self.ui.imagenesList.itemText(1) == "":     
#                     reply = qtw.QMessageBox.critical(self, "Empty", "There is not enough images, you have to create or add the samples first.")
#                 else:
#                     deleteStitched(pano[2])
#                     res = stitcherMain(pano[0])
#                     if res==True:
#                         os.remove("aux.jpg")
#                         self.selectPanorama()                                            
#                     else:
#                         reply = qtw.QMessageBox.critical(self, "Fail", "The stitcher failed, check if the images are ordered left to right. If the images are in correct order do you wanna manually stitch the images?", qtw.QMessageBox.Yes, qtw.QMessageBox.No)
#                         if reply == qtw.QMessageBox.Yes:
#                             print("pene")
#                                      
#     def remove(self):
#         if self.ui.panoramasList.currentText() == "None":
#             qtw.QMessageBox.critical(self, "None", "Select an image first.")
#         elif self.ui.imagenesList.currentText() == "None":
#             self.removePanorama()
#         else:
#             self.removeImg()
#     
#     def removePanorama(self):
#         reply = qtw.QMessageBox.critical(self, "Are you sure?", "There is no image selected, this will remove the panorama, and all the images related with it. Are you sure?", qtw.QMessageBox.Yes, qtw.QMessageBox.No)
#         if reply == qtw.QMessageBox.Yes:
#             panoramas = getPanoramas()
#             for pano in panoramas:
#                 if self.ui.panoramasList.currentText() == pano[1]:
#                     imagesDB = getImgs( pano[0])
#                     for img in imagesDB:
#                         deleteImage( img[0])
#                     if pano[2] != -1:
#                         deleteStitched( pano[2])
#                     deletePanorama( pano[0])
#                     self.updatePanoramas()
# 
#     def removeImg(self):
#         panoramas = getPanoramas()
#         for pano in panoramas:
#             if self.ui.panoramasList.currentText() == pano[1]:
#                 imagesDB = getImgs( pano[0])
#                 for img in imagesDB:
#                     if self.ui.imagenesList.currentText() == img[2]:
#                         deleteImage( img[0])
#                         self.updateImages()
    

    def createSample(self):
        conn = serial.Serial('/dev/ttyUSB0', 250000, timeout=1, exclusive=True)
        aux = True
        reply = qtw.QMessageBox

        ###
        try:
            coreName
        except NameError:
            qtw.QMessageBox.critical(self, "Incorrect Core Name", "Input a valid (alphanumeric) Core Name.")
        else:
            
            if coreName.strip() == '' or coreName.strip() == "None":
                qtw.QMessageBox.critical(self, "Empty Core Name", "Input a valid (alphanumeric) Core Name.")
            
            else:
                
                placeSample(conn,
                        self.ui.offset.value(),
                        self.ui.initSpeed.value(),
                        self.ui.tamanioMuestra.value(),
                        self.ui.tamanioHusillo.value(),
                        self.ui.platform.value())

        
                reply = qtw.QMessageBox.information(self, "Check placement", "Is the sample correctly placed?", qtw.QMessageBox.Yes, qtw.QMessageBox.No)

                if reply == qtw.QMessageBox.Yes:
                    takeSamples(conn, 
                            self.ui.offset.value(),
                            self.ui.stepSpeed.value(),
                            self.ui.tamanioMuestra.value(),
                            self.ui.sizeStep.value(),
                            self.ui.tamanioHusillo.value(),
                            self.ui.platform.value(),
                            ##
                            coreName)
                 
                   
                    reply2 = qtw.QMessageBox.information(self, "Task finished","Image shooting finished", qtw.QMessageBox.Ok)#
            
                else:
                    reply3 = qtw.QMessageBox.critical(self, "Incorrect placement","Fix the core correctly and retry", qtw.QMessageBox.Ok)
                    

def createDB():
    if not os.path.isfile('.tornilloTron.db'):
        createDataBase()         

if __name__ == "__main__":
    app = qtw.QApplication([])
    createDB()
    widget = WindInterfaz()
    widget.show()
    app.exec_()


