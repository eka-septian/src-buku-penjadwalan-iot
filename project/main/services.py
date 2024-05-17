from random import getrandbits
from project import led_pin, io

class Light:
    def __init__(self, pin: int):
        self.pin_number = pin

    def get_state(self) -> bool:
        return io.input(self.pin_number)

    @staticmethod
    def turn_on(pin: int) -> None:
        print("Turn on")
        io.output(pin, io.LOW)

    @staticmethod
    def turn_of(pin: int) -> None:
        print("Turn off")
        io.output(pin, io.HIGH)

# ledPin = 23
# io.setmode(io.BCM)
# io.setup(ledPin, io.OUT)

# def setLedState(isLedOn : bool) :
#     print(f"setting led state as {isLedOn}")
#     outVoltage: bool = io.LOW if isLedOn else io.HIGH
#     io.output(ledPin,outVoltage)
