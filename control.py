import os
import sys
import time

import RPi.GPIO as GPIO


class FanControl:

    def __init__(self,
                 fan_pin: int,
                 max_temp: float = 60, min_temp: float = 50,
                 poll_seconds: float = 30
                 ):
        self.__wait = poll_seconds if poll_seconds >= 30 else 30  # poll limit
        self.__min = min_temp
        self.__max = max_temp
        self.__pin = fan_pin
        self.__out = sys.stdout

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__pin, GPIO.OUT)
        GPIO.output(self.__pin, False)

        self.__t = None
        self.__run()

    def __pin_state(self) -> int:
        """
        gets the state of pin, if 0 is switched to LOW

        """
        GPIO.setup(self.__pin, GPIO.OUT)
        r = GPIO.input(self.__pin)
        self.__out.write(f"<<< Fan pin {self.__pin}, state={r}\n")
        return int(r)

    @property
    def __cpu_t(self) -> float:
        t_cpu = "/sys/class/thermal/thermal_zone0/temp"
        with open(t_cpu, "r") as file:
            result = float(file.read()) / 1_000
        self.__out.write(f"<<< {t_cpu} >> {result}\n")
        return result

    @property
    def __gpu_t(self) -> float:
        t_gpu = "vcgencmd measure_temp"
        result = os.popen(t_gpu).readline()
        self.__out.write(f"<<< {t_gpu} >> {result}\n")
        return float(result.replace("temp=", "").replace("'C\n", ""))

    def __run(self):
        while True:
            try:
                temp1 = self.__cpu_t
                temp2 = self.__gpu_t
                self.__t = temp1 and temp2

                if self.__t >= self.__max and self.__pin_state() == 0:
                    self.__out.write(
                        f">>> "
                        f"{temp1}°C and {temp2}°C >= max limit, "
                        f"fan on.\n")
                    GPIO.output(self.__pin, True)
                if self.__t <= self.__min and self.__pin_state() == 1:
                    self.__out.write(
                        f">>> "
                        f"{temp1}°C and {temp2}°C , temperature ok, "
                        f"fan off.\n")
                    GPIO.output(self.__pin, False)

            except Exception as e:
                self.__out.write(f"!!! {self.__t}")
                sys.stderr.write(f"!!! Interrupted, power off fan! \n{e}\n")
                GPIO.output(self.__pin, False)
                self.__out.write("!!! Interrupted, cancelling...\n")
                GPIO.cleanup()
            time.sleep(self.__wait)


if __name__ == '__main__':
    pass
