import sys

from control import FanControl
# noinspection PyUnresolvedReferences
from settings import FAN_PIN, CHECK_INTERVAL, MIN, MAX

if __name__ == '__main__':
    try:
        FanControl(fan_pin=FAN_PIN, min_temp=55,
                   thermalzone=True, check_interval=30)
    except Exception as e:
        sys.stderr.write(f"Fan control was not started\n{e}\n")
