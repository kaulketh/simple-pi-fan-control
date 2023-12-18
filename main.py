import sys

import hw_setup
from control import FanControl

if __name__ == '__main__':
    try:
        FanControl(fan_pin=hw_setup.FAN_PIN,
                   thresholds=(hw_setup.MIN, hw_setup.MAX),
                   poll=hw_setup.CHECK_INTERVAL)
    except Exception as e:
        sys.stderr.write(f"!!! Fan control was not started\n{e}\n")
