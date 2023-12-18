import os
import sys
import time
import traceback

import RPi.GPIO as GPIO


class FanControl:

    def __init__(self, fan_pin: int, thresholds: tuple, poll: float):
        self.__RL = 15  # request limit
        self.__wait = poll if poll > self.__RL else self.__RL
        self.__thresholds = thresholds  # min, max
        self.__pin = fan_pin
        self.__out = sys.stdout

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__pin, GPIO.OUT)
        GPIO.output(self.__pin, False)

        self.__temperatures = None
        self.__run()

    @property
    def __pin_state(self) -> int:
        """
        state of pin, if 0 is switched to LOW
        """
        GPIO.setup(self.__pin, GPIO.OUT)
        state = int(GPIO.input(self.__pin))
        self.__out.write(
            f"<<< Fan GPIO{self.__pin}: current state = {state}\n")
        return state

    @property
    def __t_via_file(self) -> float:
        """
        CPU temperature

        Reading the "/sys/class/thermal/thermal_zone0/temp" file, which provides
        the CPU temperature in milli degrees Celsius on a Raspberry Pi, has a
        relatively low impact on system performance compared to using
        vcgencmd measure_temp.
        You can read this file to obtain the CPU temperature quite frequently
        without causing significant overhead. The actual frequency depends on
        your application's requirements, but generally querying this file
        every few seconds (e.g., 1-5 seconds) should not cause any performance
        issues.
        Keep in mind that reading the temperature too frequently might not be
        necessary for many applications.
        Temperature changes relatively slowly compared to other sensor data,
        so intervals of a few seconds should be adequate for most temperature-
        based control systems.
        Always consider balancing the frequency of readings with the actual
        need of your application to avoid unnecessary CPU usage, especially
        if you're performing other resource-intensive tasks simultaneously.
        """
        _path = "/sys/class/thermal/thermal_zone0/temp"
        with open(_path, "r") as file:
            result = float(file.read()) / 1_000
        self.__out.write(f"<<< {_path} >> {result}\n")
        return result

    @property
    def __t_via_gpu(self) -> float:
        """
        CPU's temperature via GPU core temperature

        Calling "vcgencmd measure_temp" too frequently might not be advisable
        due to potential performance impacts.
        While it's a convenient command to retrieve the Raspberry Pi's
        CPU temperature, querying it too often could cause unnecessary
        overhead. The command vcgencmd measure_temp is a part of the Raspberry
        Pi's firmware and interacts with the VideoCore GPU, which in turn
        reads the CPU's temperature.
        Typically, calling this command every few seconds (e.g., 5 seconds)
        should not cause significant issues.
        However, if you're querying it more frequently (e.g., multiple times
        per second), it might affect the system's performance, especially if
        you're running resource-intensive tasks simultaneously.
        Consider optimizing your temperature reading frequency based on your
        specific application's requirements.
        For most temperature-controlled applications,
        checking the temperature every few seconds (e.g., 5-10 seconds)
        should be sufficient to monitor and control a fan or other cooling
        systems effectively without imposing a notable performance burden on
        the Raspberry Pi.
        """
        _cmd = "vcgencmd measure_temp"
        result = os.popen(_cmd).readline()
        self.__out.write(f"<<< {_cmd} >> {result}")
        return float(result.replace("temp=", "").replace("'C\n", ""))

    def __run(self):
        while True:
            # noinspection PyBroadException
            try:
                cpu_t1 = self.__t_via_file
                cpu_t2 = self.__t_via_gpu
                self.__temperatures = cpu_t1 and cpu_t2

                def action(msg_part, pin_state):
                    GPIO.output(self.__pin, pin_state)
                    self.__out.write(f">>> {cpu_t1}°C "
                                     f"and {cpu_t2}°C {msg_part}\n")

                if (self.__temperatures >= self.__thresholds[0]
                        and self.__pin_state == 0):
                    action(">= max limit, switch on fan.", True)
                if (self.__temperatures <= self.__thresholds[1]
                        and self.__pin_state == 1):
                    action(", temperatures ok, switch off fan.", False)

            except Exception as e:
                t = traceback.format_exc()
                self.__out.write(f"!!! {self.__temperatures}")
                sys.stderr.write(
                    f"!!! Interrupted, power off fan! \n{t}\n{e}\n")
                GPIO.output(self.__pin, False)
                self.__out.write("!!! Interrupted, cancelling...\n")
                GPIO.cleanup()
            time.sleep(self.__wait)


if __name__ == '__main__':
    pass
