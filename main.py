import sys

from control import FanControl

from settings import FAN_PIN, CHECK_INTERVAL, MIN, MAX

if __name__ == '__main__':
    try:
        FanControl(fan_pin=FAN_PIN, check_interval=CHECK_INTERVAL, max_temp=MAX, min_temp=MIN)
        # FanControl(fan_pin=FAN_PIN)
    except Exception as e:
        sys.stderr.write(f"Fan control was not started\n{e}\n")
