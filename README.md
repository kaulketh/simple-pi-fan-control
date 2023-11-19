### Plan

I would have to switch the fan directly using a small piece of software via a
GPIO pin. The program reads the CPU+GPU temperature and then switches the fan. 
The OS should start the program periodically or automatically.

### Structure

The GPIO pins of the Raspberry Pi have 3V3 logic and cannot switch the power
even of such a small fan directly. That's why a switching amplifier is needed.
This is quite easy to implement with a transistor.

### Hardware required in addition to the Raspberry Pi and its case with fan

* 1 NPN transistor e.g. BC547 B
* 1 Resistor 4,7 kOhm

See [circuit diagram](hardware/circuit_diagram.png)
and [wiring image](hardware/wiring.png)

### The Python code

* Only required package: [**_RPi.GPIO_**](https://pypi.org/project/RPi.GPIO/)
   
* **_control.py_** : FanControl class
    * In an infinite loop temperature is checked in a certain time interval
        * If the temperature is greater than or equal the max value, and the pin is
          not already activated, GPIO pin will set to HIGH
        * Is the temperature lower than or equal to the minimum value, and the pin
          is set to HIGH, GPIO pin will set to LOW
    * parameters:
        * GPIO pin of connected fan
        * Max temperature at which the fan is switched on, 60 °C per default
        * Min temperature at which the fan is switched off, 50 °C per default
        * Check interval, in seconds, 30 per default
    
* **_main.py_**: An instance of FanControl will load with given parameters.


### Auto run at boot up

One possibility is described in **_service_** directory. Refer
to [README](service/README.md)