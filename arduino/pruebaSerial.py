import serial
import time
# import piggyphoto TODO check imports
import gphoto2 as gp
import math
import signal
import os
import subprocess

# Screen
def readPrintArduino(arduino):
    rawString = arduino.readlines()
    for i in range(len(rawString)):
        print(rawString[i])

# Read, send and show
def readUntilTextArduino(arduino, text):
    rawString = arduino.read_until(text)
    print(rawString)

# Write, show in screen and sent
def writePrintArduino(arduino, texto):
    arduino.write(texto.encode())
    readPrintArduino(arduino)

# Write, wait and show
def writeUntilTextArduino(arduino, textWrite, textRead):
    arduino.write(textWrite.encode())
    readUntilTextArduino(arduino, textRead)

# Restore arduino
def resetArduino(arduino):
    writeUntilTextArduino(arduino, 'M999\r', 'ok')
    arduino.reset_input_buffer()
    arduino.reset_output_buffer()
    arduino.close()
    arduino.open()


def placeSample(conn, offset, initSpeed, sampleSize, spindle, platform):
    xmin = (spindle-sampleSize)/2 + platform + offset  # mm
    xmax = (spindle+sampleSize)/2 + platform + offset  # mm
    readUntilTextArduino(conn, "LOW")
    # Read lines and start Marlin, show
    print("Read Passed")
    # Home x axis
    writeUntilTextArduino(conn, "G28 X\r", "ok")
    print("Write Passed")
    textoXMin = "G0 X" + str(xmin-10) + " F" + \
        str(initSpeed) + "\r"  # To xmin
    tiempoSleep = 60 * float(xmin) / float(initSpeed)
    writeUntilTextArduino(conn, textoXMin, "ok")
    print("De camino a xmin = " + str(xmin-10))  # ?
    time.sleep(tiempoSleep)

# Shooting process
def takeSamples(conn, offset, speedStep, sampleSize, sizeStep, spindle, platform, nameCore):
    xmin = (spindle-sampleSize)/2 + platform + offset  # mm
    xmax = (spindle+sampleSize)/2 + platform + offset  # mm
    # Para cerrar el puerto de la camara si se ha automontado
    subprocess.call(["gio", "mount", "-s", "gphoto2"])
    time.sleep(1)
    # Round xMin/xMax
    xMin = math.floor(xmin)
    xMax = math.ceil(xmax)
    sizeStep = math.ceil(sizeStep)

    # TODO number of shoots
    global shoots
    shoots = (xMax - xMin) / sizeStep

    for i in range(xMin, xMax, sizeStep):
        textoMovimiento = "G0 X" + str(i) + " F" + str(speedStep) + "\r"
        #now = datetime.datetime.now()

        # TODO  + str(shoot).zfill(3)
        nombreImagen = nameCore + "_" + str(i) + "mm_" + ".jpg"
        path = "Outputs/" + nameCore + "/" + nombreImagen  # Nuevo "Outputs/"
        tiempoSleepPaso = 60 * float(sizeStep) / float(speedStep)
        writeUntilTextArduino(conn, textoMovimiento, "ok")
        time.sleep(tiempoSleepPaso)
        # Image capturing and download
        subprocess.run(["gphoto2", "--capture-image-and-download", "--force-overwrite", "--filename",
                       path], stdout=subprocess.PIPE, universal_newlines=True)
        print("Foto realizada en x = " + str(i) +
              " con nombre " + str(nombreImagen))

        # TODO show progress
        global progress
        progress = i/shoots

    print("Shooting Process Finished")

    subprocess.call(["gio", "mount", "-s", "gphoto2"])

    # Back to home and show
    textoXhome = "G0 X" + str(math.floor(spindle/2)) + \
        " F" + str(speedStep) + "\r"
    writeUntilTextArduino(conn, textoXhome, "ok")
    print("Shooting Process Finished.")

    conn.close()
