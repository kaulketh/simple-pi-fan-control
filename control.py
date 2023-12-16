import os
import sys
import time
import traceback

import RPi.GPIO as GPIO

import hw_setup


class FanControl:

    def __init__(self,
                 fan_pin: int = hw_setup.FAN_PIN,
                 max_temp: float = hw_setup.MAX,
                 min_temp: float = hw_setup.MIN,
                 poll: float = hw_setup.CHECK_INTERVAL
                 ):
        self.__wait = poll if poll > 30 else 30  # request limit
        self.__min = min_temp
        self.__max = max_temp
        self.__pin = fan_pin
        self.__out = sys.stdout

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__pin, GPIO.OUT)
        GPIO.output(self.__pin, False)

        self.__tcg = None
        self.__run()

    @property
    def __pin_state(self) -> int:
        """
        state of pin, if 0 is switched to LOW
        """
        GPIO.setup(self.__pin, GPIO.OUT)
        state = int(GPIO.input(self.__pin))
        self.__out.write(f"<<< Fan pin {self.__pin}, state={state}\n")
        return state

    @property
    def __cpu_t(self) -> float:
        """
        CPU temperature
        """
        _path = "/sys/class/thermal/thermal_zone0/temp"
        with open(_path, "r") as file:
            result = float(file.read()) / 1_000
        self.__out.write(f"<<< {_path} >> {result}\n")
        return result

    @property
    def __gpu_t(self) -> float:
        """
        GPU core temperature
        """
        _cmd = "vcgencmd measure_temp"
        result = os.popen(_cmd).readline()
        self.__out.write(f"<<< {_cmd} >> {result}\n")
        return float(result.replace("temp=", "").replace("'C\n", ""))

    def __run(self):
        while True:
            # noinspection PyBroadException
            try:
                c = self.__cpu_t
                g = self.__gpu_t
                self.__tcg = c and g

                msg_part = ""
                if self.__tcg >= self.__max and self.__pin_state == 0:
                    msg_part = ">= max limit, fan on."
                    GPIO.output(self.__pin, True)
                if self.__tcg <= self.__min and self.__pin_state == 1:
                    msg_part = ", temperature ok, fan off."
                    GPIO.output(self.__pin, False)
                self.__out.write(f">>> {c}°C and {g}°C {msg_part}\n")

            except Exception as e:
                t = traceback.format_exc()
                self.__out.write(f"!!! {self.__tcg}")
                sys.stderr.write(
                    f"!!! Interrupted, power off fan! \n{t}\n{e}\n")
                GPIO.output(self.__pin, False)
                self.__out.write("!!! Interrupted, cancelling...\n")
                GPIO.cleanup()
            time.sleep(self.__wait)


if __name__ == '__main__':
    pass
