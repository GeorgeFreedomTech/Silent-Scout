from machine import Pin, PWM
import time


def init_led(pin_id: int) -> PWM:
    """
    Initializes a Pulse Width Modulation (PWM) instance on a specified pin for LED control.

    Args:
        pin_id (int): The GPIO pin number.

    Returns:
        PWM: The configured PWM object.
    """
    return PWM(Pin(pin_id), freq=1000, duty=0)

def init_btn(pin_id: int) -> Pin:
    """
    Initializes a GPIO pin as a digital input with an internal pull-up resistor.

    Args:
        pin_id (int): The GPIO pin number.

    Returns:
        Pin: The configured Pin object.
    """
    return Pin(pin_id, Pin.IN, Pin.PULL_UP)

def led_off(led_pwm: PWM) -> None:
    """
    Turns off the LED by setting the PWM duty cycle to 0.
    """
    led_pwm.duty(0)

def led_on(led_pwm: PWM) -> None:
    """
    Turns on the LED at maximum brightness.
    """
    led_pwm.duty(1023)
    
def led_set_brightness(led_pwm: PWM, level_percent: int) -> None:
    """
    Sets the LED brightness based on a percentage value.

    Args:
        led_pwm (PWM): The PWM instance.
        level_percent (int): Brightness level from 0 to 100.
    """
    # Clamp percentage between 0 and 100
    level_percent = max(0, min(100, level_percent))
    duty_value = int(level_percent * 10.23)
    led_pwm.duty(duty_value)

def signal_success(led_pwm: PWM) -> None:
    """
    Triggers a visual success sequence (3 long pulses).
    
    The sequence consists of 1-second illumination followed by a 
    short pause, repeated 3 times.
    """
    for _ in range(3):
        led_on(led_pwm)
        time.sleep(1)
        led_off(led_pwm)
        time.sleep(0.2)