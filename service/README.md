## A possibility to enable run at bootup is to use the _systemd_ files. _systemd_ provides a standard process for controlling what programs run when a Linux system boots up. Note that systemd is available only from the Jessie versions of Raspbian OS.

### Create A Unit File

`sudo nano /lib/systemd/system/fan_control.service`


`sudo chmod 644 /lib/systemd/system/fan_control.service`

### Configure systemd

`sudo systemctl daemon-reload`

`sudo systemctl enable fan_control.service`

`sudo reboot`
