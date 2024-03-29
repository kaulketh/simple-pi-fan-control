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
        * If the temperature is greater than or equal the max value, and the
          pin is
          not already activated, GPIO pin will set to HIGH
        * Is the temperature lower than or equal to the minimum value, and the
          pin
          is set to HIGH, GPIO pin will set to LOW
* **_config.py_** : Settings:
    * GPIO pin of connected fan
    * Max temperature at which the fan is switched on
    * Min temperature at which the fan is switched off
    * Check interval, in seconds

* **_main.py_**: An instance of FanControl will load with passed parameters.

### Auto run at boot up

One possibility is described in **_service_** directory. Refer
to [README](service/README.md)

### Installation possibilities and steps

* Clone this repository and configure manually
* Install distribution, service enabled automatically
* Adapt _config.py_ 