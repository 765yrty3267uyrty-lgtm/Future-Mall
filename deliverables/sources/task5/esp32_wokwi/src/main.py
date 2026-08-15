"""
Future Mall - Smart Garage Gate (ESP32 + MicroPython)

Wokwi project: diagram.json + wokwi.toml live in this folder.

Behaviour:
  - IN button  (GPIO16): a car ENTERS  -> count += 1, yellow LED flashes
  - OUT button (GPIO17): a car EXITS   -> count -= 1, blue  LED flashes
  - count is clamped between 0 and MAX_CARS (15)
  - green LED on when there is free space (count < MAX_CARS)
  - red  LED on when the garage is FULL   (count == MAX_CARS)
  - serial console prints every change (helps the grader verify logic)

Pin map:
  GPIO13 -> green LED  (free space)
  GPIO14 -> red LED    (garage full)
  GPIO26 -> yellow LED (car entering)
  GPIO27 -> blue LED   (car exiting)
  GPIO16 -> IN button
  GPIO17 -> OUT button
"""
import machine
import time

MAX_CARS = 15

# --- pins ---------------------------------------------------------------
in_button   = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)
out_button  = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_UP)
green_led   = machine.Pin(13, machine.Pin.OUT)
red_led     = machine.Pin(14, machine.Pin.OUT)
yellow_led  = machine.Pin(26, machine.Pin.OUT)
blue_led    = machine.Pin(27, machine.Pin.OUT)

car_count = 0


def all_off():
    green_led.value(0)
    red_led.value(0)
    yellow_led.value(0)
    blue_led.value(0)


def update_status():
    """Free-space LEDs track the count."""
    green_led.value(1 if car_count < MAX_CARS else 0)
    red_led.value(1 if car_count == MAX_CARS else 0)


def car_enters():
    global car_count
    if car_count < MAX_CARS:
        car_count += 1
        yellow_led.value(1)
        time.sleep_ms(200)
        yellow_led.value(0)
        print("CAR IN  -> free slots:", MAX_CARS - car_count)
    else:
        red_led.value(1)
        time.sleep_ms(200)
        red_led.value(0)
        print("GARAGE FULL! Cannot accept more cars.")
    update_status()


def car_exits():
    global car_count
    if car_count > 0:
        car_count -= 1
        blue_led.value(1)
        time.sleep_ms(200)
        blue_led.value(0)
        print("CAR OUT -> free slots:", MAX_CARS - car_count)
    else:
        green_led.value(1)
        time.sleep_ms(200)
        green_led.value(0)
        print("Garage is empty, nothing to exit.")
    update_status()


def debounce(pin):
    """Simple software debounce: wait for a stable read."""
    state = 0
    t0 = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), t0) < 30:
        if pin.value() == 0:
            state += 1
        else:
            state -= 1
        time.sleep_ms(2)
    return state > 0


print()
print("Future Mall Smart Garage Gate - ready. Max cars:", MAX_CARS)
all_off()
update_status()

while True:
    if in_button.value() == 0 and debounce(in_button):
        while in_button.value() == 0:      # wait for release
            time.sleep_ms(10)
        car_enters()

    if out_button.value() == 0 and debounce(out_button):
        while out_button.value() == 0:     # wait for release
            time.sleep_ms(10)
        car_exits()