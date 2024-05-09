import RPi.GPIO as io

ledPin = 23
io.setmode(io.BCM)
io.setup(ledPin, io.OUT)

def setLedState(isLedOn : bool) :
    print(f"setting led state as {isLedOn}")
    outVoltage: bool = io.LOW if isLedOn else io.HIGH
    io.output(ledPin,outVoltage)