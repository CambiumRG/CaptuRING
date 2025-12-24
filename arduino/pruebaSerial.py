import time
import math
import subprocess

"""Utility helpers for communicating with a Marlin/Arduino-like serial
device and driving a camera capture loop. Printing and reading functions are
provided to facilitate sending commands and waiting for responses.

Notes:
- Positions are expressed in millimetres (mm).
- Speeds/feedrates are assumed to be in mm/min (consistent with Marlin G-code
    feedrates), and sleeps convert movement times accordingly.
- Some functions call external commands (`gphoto2`, `gio`) and therefore
    require those tools to be installed and available in PATH (typically on
    Linux systems).
"""


def readPrintArduino(arduino):
        """Read all available lines from a serial-like object and print them.

        This calls `arduino.readlines()` and prints each returned line to
        stdout. The `arduino` parameter should be a file-like or
        pyserial.Serial-compatible object.

        Args:
                arduino: Serial or file-like object exposing `readlines()`.

        Side effects:
                Prints lines to stdout. Returns None.
        """
        rawString = arduino.readlines()
        for i in range(len(rawString)):
                print(rawString[i])

# Read, send and show
def readUntilTextArduino(arduino, text):
    """Read from `arduino` until `text` is found, then print the result.

    The `text` argument may be a string or bytes depending on the serial
    implementation. This is a thin helper which delegates to
    `arduino.read_until()` and prints the returned bytes/string.

    Args:
        arduino: Serial or file-like object exposing `read_until()`.
        text: Terminator to wait for (string or bytes).

    Side effects:
        Prints the data read to stdout. Returns None.
    """
    rawString = arduino.read_until(text)
    print(rawString)

# Write, show in screen and sent
def writePrintArduino(arduino, texto):
    """Write a text command to `arduino` and print any available response.

    The supplied `texto` string is encoded to bytes with the default
    encoding before being written. After writing, this calls
    `readPrintArduino()` to show any lines returned by the device.

    Args:
        arduino: Serial or file-like object exposing `write()`.
        texto: Text command to send (string). A trailing newline or \r may be
               required depending on the firmware's command format.
    """
    arduino.write(texto.encode())
    readPrintArduino(arduino)

# Write, wait and show
def writeUntilTextArduino(arduino, textWrite, textRead):
    """Write `textWrite` to `arduino` and block until `textRead` is seen.

    This sends a command and then uses `readUntilTextArduino()` to wait for
    an expected acknowledgement or marker in the device output (for
    example: 'ok').

    Args:
        arduino: Serial or file-like object exposing `write()`.
        textWrite: Command string to write (will be encoded to bytes).
        textRead: Terminator string/bytes to wait for in responses.
    """
    arduino.write(textWrite.encode())
    readUntilTextArduino(arduino, textRead)

# Restore arduino
def resetArduino(arduino):
    """Reset a Marlin/Arduino device and re-initialize the serial buffers.

    The function sends the Marlin `M999` command (reset), waits for an
    'ok' acknowledgement, clears input/output buffers, and re-opens the
    serial connection so the device can be used again.

    Args:
        arduino: A pyserial.Serial instance (or compatible) exposing
                 `write()`, `reset_input_buffer()`, `reset_output_buffer()`,
                 `close()` and `open()`.

    Side effects:
        Sends commands to the device and re-opens the serial port.
    """
    writeUntilTextArduino(arduino, 'M999\r', 'ok')
    arduino.reset_input_buffer()
    arduino.reset_output_buffer()
    arduino.close()
    arduino.open()


def placeSample(conn, offset, initSpeed, sampleSize, spindle, platform):
    """Prepare the stage and move to starting position for a sample run.

    Calculates the X start (`xmin`) and end (`xmax`) positions for the
    sample area using the provided offsets, homes the X axis, and moves the
    stage to a position slightly before `xmin` so the acquisition routine
    can proceed from there.

    Parameters are interpreted as follows:
      - offset, platform, spindle, sampleSize: distances in millimetres (mm)
      - initSpeed: feedrate in mm/min

    Args:
        conn: Serial connection to the motion controller (used for G-code
              commands and simple text responses).
        offset: Offset added to computed sample positions (mm).
        initSpeed: Initial move feedrate (mm/min).
        sampleSize: Size of the sample area (mm).
        spindle: Position reference (mm).
        platform: Base platform offset (mm).

    Side effects:
        Sends G-code to `conn`, waits for acknowledgements and sleeps for
        the expected movement duration to ensure the stage arrives.
    """
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
    """Traverse the sample area and capture images at each step.

    Moves the stage from `xmin` to `xmax` in steps of `sizeStep`, pausing
    between moves to allow the stage to settle, and captures a photo at
    each position using `gphoto2`. The images are saved to
    `Outputs/<nameCore>/<nameCore>_<X>mm_.jpg`.

    Requirements:
      - `gphoto2` and `gio` must be installed and available on the system.

    Args:
        conn: Serial connection to the motion controller (used for G-code
              commands and simple text responses).
        offset, sampleSize, spindle, platform: distances in mm used to
              compute the X range.
        speedStep: Feedrate for step moves (mm/min).
        sizeStep: Step size between captures (mm).
        nameCore: Base name for output images and folder.

    Side effects:
        Calls external processes (`gio`, `gphoto2`), writes image files,
        moves the stage via `conn` and closes the serial connection when
        finished.
    """
    xmin = (spindle-sampleSize)/2 + platform + offset  # mm
    xmax = (spindle+sampleSize)/2 + platform + offset  # mm
    # Para cerrar el puerto de la camara si se ha automontado
    subprocess.call(["gio", "mount", "-s", "gphoto2"]) # Requires library installation
    time.sleep(1)
    # Round xMin/xMax
    xMin = math.floor(xmin)
    xMax = math.ceil(xmax)
    sizeStep = math.ceil(sizeStep)


    for i in range(xMin, xMax, sizeStep):
        textoMovimiento = "G0 X" + str(i) + " F" + str(speedStep) + "\r"
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
    print("Shooting Process Finished")

    subprocess.call(["gio", "mount", "-s", "gphoto2"])

    # Back to home and show
    textoXhome = "G0 X" + str(math.floor(spindle/2)) + \
        " F" + str(speedStep) + "\r"
    writeUntilTextArduino(conn, textoXhome, "ok")
    print("Shooting Process Finished.")

    conn.close()
