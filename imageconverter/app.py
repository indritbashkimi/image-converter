#!/usr/bin/env python3
#
#  Image Converter 0.4.0.0
#
#  Copyright 2015 Indrit Bashkimi <indrit.bashkimi@gmail.com>
#

def run():
    import sys
    import platform

    NAME = 'Image Converter'
    VERSION = '0.4.0.0'
    system = platform.system()  # -> 'Linux' oppure: system = os.name -> 'posix'
    python_version = int(platform.python_version()[0])

    if python_version < 3:
        print('python3 not found')
        sys.exit()

    from main_window import MainWindow

    window = MainWindow()

if __name__ == '__main__':
    run()
