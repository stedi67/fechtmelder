class Pin:
    OUT = 'OUT'
    PULL_UP = 'PULL_UP'
    IN = 'IN'

    def __init__(self, address, pin_type, resistor_type=None):
        self.value = 0

    def value(self, value=None):
        if value is not None:
            self.value = value
        return self.value
