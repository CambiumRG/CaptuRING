import serial
import time
#import piggyphoto
import gphoto2 as gp  # Nueva libreria para gestion camara
import math
import signal
import os
import subprocess

# Funcion para escribir por pantalla lo que ha mandado el Arduino por el puerto Serie


def readPrintArduino(arduino):
    rawString = arduino.readlines()
    for i in range(len(rawString)):
        print(rawString[i])

# Funcion para leer todo hasta que el Arduino mande un texto concreto y entonces escribirlo en pantalla


def readUntilTextArduino(arduino, text):
    rawString = arduino.read_until(text)
    print(rawString)

# Funcion para escribir en el Arduino el comando que queramos y luego por pantalla lo que ha mandado respondiendo el Arduino por el puerto Serie


def writePrintArduino(arduino, texto):
    arduino.write(texto.encode())
    readPrintArduino(arduino)

# Funcion para escribir en el Arduino el comando que queramos y luego esperar hasta que mande ok y, entonces, presentar por pantalla lo que ha mandado respondiendo el Arduino por el puerto Serie


def writeUntilTextArduino(arduino, textWrite, textRead):
    arduino.write(textWrite.encode())
    readUntilTextArduino(arduino, textRead)

# Comando para resetear el Arduino


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
    # Lectura de las lineas que manda el Arduino al iniciar con la version del Marlin, etc. e impresion en pantalla de ese texto
    print("Read Passed")
    # Comando para hacer el Home al eje X
    writeUntilTextArduino(conn, "G28 X\r", "ok")
    print("Write Passed")
    textoXMin = "G0 X" + str(xmin-10) + " F" + \
        str(initSpeed) + "\r"  # Comando para ir a xmin
    tiempoSleep = 60 * float(xmin) / float(initSpeed)
    writeUntilTextArduino(conn, textoXMin, "ok")
    print("De camino a xmin = " + str(xmin-10))  # ?
    time.sleep(tiempoSleep)

# Toma de fotografia


def takeSamples(conn, offset, speedStep, sampleSize, sizeStep, spindle, platform, nameCore):
    xmin = (spindle-sampleSize)/2 + platform + offset  # mm
    xmax = (spindle+sampleSize)/2 + platform + offset  # mm
    # Para cerrar el puerto de la camara si se ha automontado
    subprocess.call(["gio", "mount", "-s", "gphoto2"])
    time.sleep(1)
    # Cambio
    xMin = math.floor(xmin)
    xMax = math.ceil(xmax)
    sizeStep = math.ceil(sizeStep)

    ##
    global shoots
    shoots = (xMax - xMin) / sizeStep

    for i in range(xMin, xMax, sizeStep):
        textoMovimiento = "G0 X" + str(i) + " F" + str(speedStep) + "\r"
        #now = datetime.datetime.now()

        # Eliminado  + str(shoot).zfill(3)
        nombreImagen = nameCore + "_" + str(i) + "mm_" + ".jpg"
        path = "Outputs/" + nameCore + "/" + nombreImagen  # Nuevo "Outputs/"
        tiempoSleepPaso = 60 * float(sizeStep) / float(speedStep)
        writeUntilTextArduino(conn, textoMovimiento, "ok")
        time.sleep(tiempoSleepPaso)
        # Tomar imagen
        subprocess.run(["gphoto2", "--capture-image-and-download", "--filename",
                       path], stdout=subprocess.PIPE, universal_newlines=True)
        print("Foto realizada en x = " + str(i) +
              " con nombre " + str(nombreImagen))

        global progress
        progress = i/shoots

    print("Shooting Process Finished")

    subprocess.call(["gio", "mount", "-s", "gphoto2"])

    # Vuelta a casa
    textoXhome = "G0 X" + str(math.floor(spindle/2)) + \
        " F" + str(speedStep) + "\r"
    writeUntilTextArduino(conn, textoXhome, "ok")
    print("Captura finalizada correctamente.")

    conn.close()
