#!/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# setup
# created 24.12.2023
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# -----------------------------------------------------------
import platform
import subprocess
import sys

from setuptools import setup, find_packages
from setuptools.command.install import install


class InstallService(install):
    FILE_NAME = 'fan_control.service'
    FILE_CONTENT = '''
    [Unit]
    Description=Fan control service
    After=multi-user.target
    
    [Service]
    Type=idle
    ExecStart=/usr/bin/python3 /home/pi/fan_control/main.py
    
    [Install]
    WantedBy=multi-user.target
    '''

    def run(self):
        install.run(self)  # Call the default install functionality
        # Add code here to create the service
        with open(f'/etc/systemd/system/{InstallService.FILE_NAME}',
                  'w') as service_file:
            service_file.write(InstallService.FILE_CONTENT)

        # Example command to create a service (modify this based on your needs)
        if platform.system() == 'Linux':
            try:
                subprocess.run(['systemctl', 'daemon-reload'])
                subprocess.run(
                    ['systemctl', 'enable', InstallService.FILE_NAME],
                    check=True)
                sys.stdout.write(
                    f'Service "{InstallService.FILE_NAME}" enabled successfully.\n')

            except subprocess.CalledProcessError as e:
                sys.stderr.write(f'Failed to enable service: {e}\n')


setup(
    name='simple-pi-fan-control',
    version='1.0',
    packages=find_packages(exclude=[]),
    author='Thomas Kaulke',
    author_email='kaulketh@gmail.com',
    description='The program reads the CPU+GPU temperature and switches GPIO channel.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kaulketh/simple-pi-fan-control',
    license=open('LICENSE.md').read(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'RPi.GPIO'
    ],
    cmdclass={
        'install': InstallService,
    }
)

if __name__ == '__main__':
    setup()
