# Import libraries
import os
import time
from time import sleep

import machine
import network
import st7789
import vga1_bold_16x32 as font
import webrepl


# Wifi connection setup (URL: https://www.youtube.com/watch?v=10Y89xaVkqw)
def setup_wifi():
    wifi = network.WLAN(network.AP_IF)  # access point = AP, station mode = STA
    wifi.active(True)
    wifi.config(essid='ESP 32', password='12345678', authmode=network.AUTH_WPA_WPA2_PSK)
    webrepl.start(password="12345678")


# Read medication files
files = os.listdir()
for file in files:
    print(file)

filename = "medication.txt"

try:
    with open(filename, "r") as file:
        days = []
        for line in file:
            line_words = line.strip().split()
            days.extend(line_words)
        print(days)

except OSError:
    print("Medication file not found.")

# Setup Stepper Motor

IN1 = machine.Pin(26, machine.Pin.OUT)
IN2 = machine.Pin(25, machine.Pin.OUT)
IN3 = machine.Pin(33, machine.Pin.OUT)
IN4 = machine.Pin(32, machine.Pin.OUT)
pins = [IN1, IN2, IN3, IN4]
sequence = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]


def step(seq):
    for i in range(len(pins)):
        pins[i].value(seq[i])


rotations = 0
filling_counter = 0


# play sound with Piezo
def play_mario():
    # Define frequencies for notes
    E7 = 2637
    C7 = 2093
    G7 = 3136
    G6 = 1568
    E6 = 1319
    A6 = 1760
    AS6 = 1865
    F7 = 2794
    D7 = 2349
    B6 = 1976
    A7 = 3520

    # Piezo play notes function
    def play(pin, melodies, delays, duty):
        pwm = machine.PWM(pin)
        for note in melodies:
            pwm.freq(note)
            pwm.duty(duty)
            time.sleep(delays)

        pwm.duty(0)
        pwm.deinit()

        # Mario song frequencies

    mario = [
        E7, E7, 1, E7, 1, C7, E7, 1,
        G7, 1, 1, 1, G6, 1, 1, 1,
        C7, 1, 1, G6, 1, 1, E6, 1,
        1, A6, 1, B6, 1, AS6, A6, 1,
        G6, E7, 1, G7, A7, 1, F7, G7,
        1, E7, 1, C7, D7, B6, 1, 1,
        C7, 1, 1, G6, 1, 1, E6, 1,
        1, A6, 1, B6, 1, AS6, A6, 1,
        G6, E7, 1, G7, A7, 1, F7, G7,
        1, E7, 1, C7, D7, B6, 1, 1,
    ]

    play(p23, mario, 0.15, 50)


# Display Setup
def setup_display() -> st7789.ST7789:
    """
    The driver library can be found here: https://github.com/russhughes/st7789_mpy
    """
    spi = machine.SPI(1, baudrate=30000000, polarity=1,
                      sck=machine.Pin(18), mosi=machine.Pin(19))
    device = st7789.ST7789(spi, 135, 240,
                           reset=machine.Pin(23, machine.Pin.OUT), cs=machine.Pin(5, machine.Pin.OUT),
                           dc=machine.Pin(16, machine.Pin.OUT), backlight=machine.Pin(4, machine.Pin.OUT),
                           rotations=[(0x00, 240, 320, 0, 0), (0x60, 320, 240, 0, 0), (0xc0, 240, 320, 0, 0),
                                      (0xa0, 320, 240, 0, 0)],
                           rotation=1, options=1)

    device.init()
    device.inversion_mode(True)
    device.sleep_mode(False)

    return device


# Buttons Class Setup
class Button:
    def __init__(self, pin_number: int, inverted: bool) -> None:
        self._pin = machine.Pin(pin_number, machine.Pin.IN, machine.Pin.PULL_UP)
        self._inverted = inverted

    @property
    def state(self) -> bool:
        return not bool(self._pin.value()) if self._inverted else bool(self._pin.value())


# create button objects
fill_button_left = Button(0, True)
weekly_mode_button_right = Button(35, True)

# Set display parameters
display = setup_display()
display.on()
display.rect(0, 0, 135, 240, st7789.BLACK)
print(f"Display: h={display.height()}px, w={display.width()}px")
y_index = 11

# Start output of medications according to the day of the week
current_day = 6

while True:

    # Filling mode
    if fill_button_left.state:
        current_day = (current_day + 1) % 7

        display.text(font, days[current_day], 40, 110)
        for x in range(74):
            for step in sequence:
                for i in range(len(pins)):
                    pins[i].value(step[i])
                    time.sleep(0.001)

            x = x + 1
            if x == 70:
                x = 0
                filling_counter = filling_counter + 1
                if filling_counter == 8:
                    time.sleep(5)  # 24 hours in real operation (=86400 seconds)

                    for i in range(4):
                        play_mario()
                        if weekly_mode_button_right.state:
                            sleep(2)
                            break

    # Weekly operation mode
    elif weekly_mode_button_right.state:
        if rotations == 0:
            for x in range(740):
                for step in sequence:
                    for i in range(len(pins)):
                        pins[i].value(step[i])
                        sleep(0.001)

                x = x + 1
                if x == 210:
                    x = 0
                    rotations = rotations + 1
                    break

        else:
            # Rotate only 1/7 per day starting from Monday
            current_day = (current_day + 1) % 7
            display.text(font, days[current_day], 40, 110)

            for x in range(74):
                for step in sequence:
                    for i in range(len(pins)):
                        pins[i].value(step[i])
                        sleep(0.001)

                x = x + 1
                if x == 70:
                    time.sleep(5)  # 24 hours in real operation (=86400 seconds)
                    for i in range(10):
                        play_mario()
                        if weekly_mode_button_right.state:
                            break
