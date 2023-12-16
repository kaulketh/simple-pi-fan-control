import sys

from control import FanControl

if __name__ == '__main__':
    try:
        FanControl()
    except Exception as e:
        sys.stderr.write(f"!!! Fan control was not started\n{e}\n")
