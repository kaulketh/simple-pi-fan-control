from control import FanControl

# noinspection PyUnresolvedReferences
from settings import FAN_PIN, CHECK_INTERVAL, MIN, MAX

if __name__ == '__main__':
    # FanControl(fan_pin=FAN_PIN, check_interval=CHECK_INTERVAL, max_temp=MAX, min_temp=MIN)
    FanControl(fan_pin=FAN_PIN, check_interval=CHECK_INTERVAL)
