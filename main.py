import sys

import config
from control import FanControl

if __name__ == '__main__':
    try:
        FanControl(fan_pin=config.FAN_PIN,
                   thresholds=(config.MIN, config.MAX),
                   poll=config.CHECK_INTERVAL)
    except Exception as e:
        sys.stderr.write(f"!!! Fan control was not started\n{e}\n")
