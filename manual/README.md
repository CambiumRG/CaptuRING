# CaptuRING

This is a Digitization Project made by [Cambium Research Group](https://cambiumresearch.eu), 2021.
The extended manual is presented in the [attached document](https://github.com/CambiumRG/CaptuRING/blob/main/manual/CRUserManual_v1.0.0.pdf)
## About
CaptuRING [[1](#references)] is a Do-It-Yourself tool for wood sample digitization. Although the main objective of the tool is taking high resolution images from wood samples, the system could operate with other kind of samples. 

If you use this tool, *please cite*: García-Hidalgo, M., García-Pedrero, Á., Colón, D., Sangüesa-Barreda, G., García-Cervigón, A. I., López-Molina, J., Hernández-Alonso, H., Rozas, V., Olano, J. M. & Alonso-Gómez, V. (2022). CaptuRING: A do-it-yourself tool for wood sample digitization. *Methods in Ecology and Evolution*, 00, 1– 7. https://doi.org/10.1111/2041-210X.13847

*Disclaimer*

The standard use of CaptuRING with Raspberry Pi/Raspbian based on Debian Buster is explained. Variations on harware characteristics will require modifications in the CaptuRING&reg; code related to the port uses in other OS.

First Sight

See the detailed user manual in manual>UserManual.pdf

## Component Check-List


*CaptuRING motion Hardware*
1. Photography enlarger base
2. Led lighting
3. C-Beam linear actuator + NEMA 23 stepper motor
4. Endstop switch
5. Linear rails
6. Driver IC for stepper motor
7. Arduino® based 3D printer controller
8. Power supply (12 V DC / 150W source)
9. Sample Holder (3D Print) *
10. Rail adapter (3D Print) *

Electric cable for connections in case they are not provided, screws and glue for component fixing.

*Optical and controlling devices*
1. Raspberry Pi Kit (with microSD, power source, cables and case)
2. Peripherals (Screen monitor, keyboard and mouse)
3. DSLR Camera compatible with the [*gphoto2*](http://www.gphoto.org/) system**
4. Camera Lens



For an efficient shopping, you can purchase the listed components in a store specialized in electronics or '3D printing'.

*The 3D print models provided are just one proposal. Please confirm that the 3D print models and sizes are compatible with the rest of components. We highly recommend developing different sample holders or rail adapters depending on your requirements and share them with the community.

**You can look at the [supported cameras here](http://www.gphoto.org/proj/libgphoto2/support.php).

## *Motion Hardware* 

## Assembling
Once you have confirmed that all the listed components are compatible you can assemble the whole tool according to the following architecture.

#### Assembling map  
Detailed version [here](CRAssembling.pdf)
<p align="center">
  <img src="https://github.com/CambiumRG/CaptuRING/blob/main/manual/images/assembling.png" title="Assembling architecture" width="300">  
</p>

#### Connection map
Detailed version [here](CRConnection.pdf)

<p align="center">
  <img src="https://github.com/CambiumRG/CaptuRING/blob/main/manual/images/cring_sch.jpg" title="CR Conection architecture" width="300">
</p>

_Arduino Board_

<p align="center">
  <img src="https://github.com/CambiumRG/CaptuRING/blob/main/manual/images/MKS1.png" title="MKS Conection architecture" width="300">
</p>

_Digital Camera_

The digital camera and 3D Printinng Controller Card must be connected to Raspberry Pi through USB Port. You can use a USB hub if needed.

## Install and Set-Up

1. Raspberry Pi must be configured according to [Raspberry Pi](raspberrypi.com) version with Raspbian OS
2. Configure 3D printer board based on Arduino following its specific [user manual](https://github.com/makerbase-mks/SGEN_L/blob/master/MKS%20SGEN_L%20Datasheet.pdf)
   1. Configure the measurements of the spindle, motor direction and end-stop switch options according to the specific firmware instructions.
3. Install the python dependencies:
   1. [PyQt5](https://pypi.org/project/PyQt5/)
   2. [serial (pyserial)](https://pypi.org/project/pyserial/)
   3. [gphoto2](https://pypi.org/project/gphoto2/)

4. Download [CaptuRING code](https://github.com/cambiumrg/capturing) and store it in an specific folder.  

## Launch CaptuRING

1. Open a new Terminal window
   1. Option: Activate a specific [Python environment](https://docs.python.org/3/library/venv.html)
2. Go to CaptuRING folder
3. Write and execute: _python main.py_
4. See [My First Shoot](#my-first-shoot) instructions

<p align="center">
  <img src="https://github.com/CambiumRG/CaptuRING/blob/main/manual/images/window.png" title="Interface">
</p>

## Possible Issues

* _Python error:_ Confirm that your Python version is compatible with CaptuRING code. If it is not, you can create a specific virtual environment with Python 3.7
* _Dependencies error:_ Make sure you installed all the dependencies
* Depending on distributions, some _dependencies_ should be configured following their respective instructions 

## My First Shoot
### Sample placement
1. Measure the length of your sample
2. Place the sample centered on the sample holder
3. Switch on all the electronic components
4. Confirm that the camera placement in height on the enlarger base allows a sharp caption of the sample

### Shooting Process
Once CaptuRING software is launched:
1. Enter your device characteristics in the Options sections. (Only for the first time)
   1. _Offset:_ Variation between the center of the specimen and the center of the sample holder
   2. _Speed/step:_ Screw speed in the caption process
   3. _Initial speed:_ Screw speed for start-up
   4. _Step size:_ Size of each step
   5. _Spindle size:_ Total length of the screw
   6. _Platform:_ Variation between the center of the sample holder and the screw platform
2. Enter the Sample Name
3. Click on 'Name it!'
4. Enter sample size in mm
5. Click on 'CAPTURE'
6. Digitized images are stored in the Output/’Sample Name’ folder

Current code is the first release of the CaptuRING® software to control the digitization process described in "CaptuRING: A Do-It-Yourself tool for woodsample digitization" (García-Hidalgo, 2022). 

*Original code is registered with number 00 / 2022 / 737 according to the Ley de Propiedad Intelectual (Real Decreto Legislativo 1/1996, de 12 de abril) by Ministry of Culture and Sport of Spain. At the same time, this work is released as Free Open Source to be used and modified according to the user requirements and different hardware characteristics but referencing the original work (See Citation).*


## References

[1] García-Hidalgo, M., García-Pedrero, Á., Colón, D., Sangüesa-Barreda, G., García-Cervigón, A. I., López-Molina, J., Hernández-Alonso, H., Rozas, V., Olano, J. M. & Alonso-Gómez, V. (2022). CaptuRING: A do-it-yourself tool for wood sample digitization. *Methods in Ecology and Evolution*, 00, 1– 7. https://doi.org/10.1111/2041-210X.13847




