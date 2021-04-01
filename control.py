import os
import sys
import time

import RPi.GPIO as GPIO


class FanControl:
    def __init__(self,
                 fan_pin: int,
                 check_interval: float = 60,
                 max_temp: float = 65, min_temp: float = 45
                 ):
        self.__wait = check_interval
        self.__min = min_temp
        self.__max = max_temp
        self.__pin = fan_pin
        self.__out = sys.stdout

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__pin, GPIO.OUT)
        GPIO.output(self.__pin, False)

        self.__run()

    def __pin_state(self) -> int:
        """
        gets the state of pin, if 0 is switched to LOW

        """
        GPIO.setup(self.__pin, GPIO.OUT)
        r = GPIO.input(self.__pin)
        self.__out.write(f"Fan pin {self.__pin}, state={r}\n")
        return int(r)

    def __temp(self) -> float:
        result = os.popen("vcgencmd measure_temp").readline()
        self.__out.write(f"Core {result}")
        return float(result.replace("temp=", "").replace("'C\n", ""))

    def __run(self):
        while True:
            temp = self.__temp()
            try:
                if temp >= self.__max and self.__pin_state() == 0:
                    self.__out.write(f"{temp}°C >= max limit, fan on.\n")
                    GPIO.output(self.__pin, True)
                if temp <= self.__min and self.__pin_state() == 1:
                    self.__out.write(f"{temp}°C, temperature ok, fan off.\n")
                    GPIO.output(self.__pin, False)

            except Exception as e:
                self.__out.write(f"{self.__temp()}")
                sys.stderr.write(f"Interrupted, power off fan! \n{e}\n")
                GPIO.output(self.__pin, False)
                self.__out.write("Interrupted, cancelling...\n")
                GPIO.cleanup()

            time.sleep(self.__wait)


if __name__ == '__main__':
    pass
