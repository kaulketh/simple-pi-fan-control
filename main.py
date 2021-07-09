import sys

from control import FanControl

if __name__ == '__main__':
    try:
        FanControl(fan_pin=27, min_temp=61, max_temp=68, poll_seconds=60)
    except Exception as e:
        sys.stderr.write(f"!!! Fan control was not started\n{e}\n")
