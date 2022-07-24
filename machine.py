class Pin:
    OUT = 'OUT'
    PULL_UP = 'PULL_UP'
    PULL_DOWN = 'PULL_DOWN'
    IN = 'IN'

    def __init__(self, address, pin_type, resistor_type=None):
        self._value = 0

    def value(self, value=None):
        if value is not None:
            self._value = value
        return self._value
