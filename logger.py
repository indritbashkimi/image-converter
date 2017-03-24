import sys


class Logger:
    def __init__(self):
        self.terminal = sys.__stdout__
        self.console = True
        self.log = False
        self.log = ''

    def write(self, msg):
        if self.console:
            self.terminal.write(msg)
        if self.log:
            self.log += msg+'\n'

    def flush(self):
        self.terminal.flush()

    def display(self):
        self.terminal.write(self.log)
        pass

    def set_console_status(self, status):
        self.console = status

    def get_console_status(self):
        return self.console

    def clear(self):
        self.log = ''