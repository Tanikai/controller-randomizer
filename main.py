from XInput import EventHandler, GamepadThread, get_connected, EVENT_BUTTON_PRESSED, EVENT_BUTTON_RELEASED, FILTER_NONE
import vgamepad as vg
from time import sleep
from strenum import StrEnum
from typing import Dict
import random
from threading import Thread


class Button(StrEnum):
    DPAD_UP = "DPAD_UP"
    DPAD_DOWN = "DPAD_DOWN"
    DPAD_LEFT = "DPAD_LEFT"
    DPAD_RIGHT = "DPAD_RIGHT"
    START = "START"
    BACK = "BACK"
    LEFT_THUMB = "LEFT_THUMB"
    RIGHT_THUMB = "RIGHT_THUMB"
    LEFT_SHOULDER = "LEFT_SHOULDER"
    RIGHT_SHOULDER = "RIGHT_SHOULDER"
    A = "A"
    B = "B"
    X = "X"
    Y = "Y"
    LEFT_TRIGGER = "LEFT_TRIGGER"  # analog triggers
    RIGHT_TRIGGER = "RIGHT_TRIGGER"


const_mapping = {
    Button.START: Button.START,  # dont change this
    Button.BACK: Button.BACK,  # dont change this
    Button.LEFT_THUMB: Button.LEFT_THUMB,
    Button.RIGHT_THUMB: Button.RIGHT_THUMB,
}

randomized_mapping = {
    Button.DPAD_UP: Button.DPAD_UP,
    Button.DPAD_DOWN: Button.DPAD_DOWN,
    Button.DPAD_LEFT: Button.DPAD_LEFT,
    Button.DPAD_RIGHT: Button.DPAD_RIGHT,
    Button.LEFT_SHOULDER: Button.LEFT_SHOULDER,
    Button.RIGHT_SHOULDER: Button.RIGHT_SHOULDER,
    Button.LEFT_TRIGGER: Button.LEFT_TRIGGER,
    Button.RIGHT_TRIGGER: Button.RIGHT_TRIGGER,
    Button.A: Button.A,
    Button.B: Button.B,
    Button.X: Button.X,
    Button.Y: Button.Y
}

randomized_buttons = [
    Button.DPAD_UP,
    Button.DPAD_DOWN,
    Button.DPAD_LEFT,
    Button.DPAD_RIGHT,
    Button.LEFT_SHOULDER,
    Button.RIGHT_SHOULDER,
    Button.LEFT_TRIGGER,
    Button.RIGHT_TRIGGER,
    Button.A,
    Button.B,
    Button.X,
    Button.Y
]

xbox_map = {
    Button.DPAD_UP: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
    Button.DPAD_DOWN: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
    Button.DPAD_LEFT: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
    Button.DPAD_RIGHT: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
    Button.START: vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
    Button.BACK: vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
    Button.LEFT_THUMB: vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
    Button.RIGHT_THUMB: vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
    Button.LEFT_SHOULDER: vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
    Button.RIGHT_SHOULDER: vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
    Button.A: vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
    Button.B: vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
    Button.X: vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
    Button.Y: vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
}

"""Randomizes button mappings. Maps from Button(StrEnum) -> Button(StrEnum)
"""


def get_random_mapping() -> Dict[Button, Button]:
    # TODO implement randomizing algorithm
    available_buttons = list(randomized_buttons)
    random.shuffle(available_buttons)
    for key in randomized_mapping:
        randomized_mapping[key] = available_buttons.pop()

    final_dict = dict(const_mapping)
    final_dict.update(randomized_mapping)
    return final_dict


class MappedVirtualGamepad:
    """Simulates a virtual Xbox gamepad with the given mapping.
    """
    out_gp = None
    analog_threshold = 0.1  # larger = button pressed
    button_map = None

    def __init__(self):
        self.out_gp = vg.VX360Gamepad()

    def set_custom_mapping(self, mapping: Dict[Button, Button]):
        self.button_map = mapping
        self.out_gp.reset()

    def _get_custom_mapping(self, button: Button) -> Button:
        if self.button_map is None:
            return button

        return self.button_map[button]

    def handle_trigger(self, trigger_button, value):
        if value > self.analog_threshold:
            self.press_button(trigger_button)
        else:
            self.release_button(trigger_button)

    def press_button(self, button: Button):
        """ Presses a button. Maps from Button(StrEnum) -> Simulated Controller.
        """
        mapped_button = self._get_custom_mapping(button)

        if mapped_button == Button.LEFT_TRIGGER:
            self.out_gp.left_trigger_float(1)
        elif mapped_button == Button.RIGHT_TRIGGER:
            self.out_gp.right_trigger_float(1)
        else:
            xbox_button = xbox_map[mapped_button]
            self.out_gp.press_button(button=xbox_button)

        self.out_gp.update()

    def release_button(self, button: Button):
        """ Releases a button. Maps from Button(StrEnum) -> Simulated Controller.
        """
        mapped_button = self._get_custom_mapping(button)

        if mapped_button == Button.LEFT_TRIGGER:
            self.out_gp.left_trigger_float(0)
        elif mapped_button == Button.RIGHT_TRIGGER:
            self.out_gp.right_trigger_float(0)
        else:
            xbox_button = xbox_map[mapped_button]
            self.out_gp.release_button(button=xbox_button)

        self.out_gp.update()


class RandomVirtualController(EventHandler):
    """ Reads the input from an XInput controller and outputs a random mapping to a virtual controller.
    """
    virt_gp = None

    def __init__(self, f=FILTER_NONE):
        super().__init__(0, filter=f)
        self.virt_gp = MappedVirtualGamepad()

    def process_button_event(self, event):
        if event.type == EVENT_BUTTON_PRESSED:
            self.virt_gp.press_button(event.button)
        else:
            self.virt_gp.release_button(event.button)

    def process_trigger_event(self, event):
        # 0: Left Trigger
        # 1: Right Trigger
        trigger = ""
        if event.trigger == 0:
            trigger = Button.LEFT_TRIGGER
        else:
            trigger = Button.RIGHT_TRIGGER

        self.virt_gp.handle_trigger(trigger, event.value)

    def process_stick_event(self, event):
        # Stick 0: Left Stick
        # Stick 1: Right Stick
        if event.stick == 0:
            self.virt_gp.out_gp.left_joystick_float(event.x, event.y)
        else:
            self.virt_gp.out_gp.right_joystick_float(event.x, event.y)

        self.virt_gp.out_gp.update()

    def process_connection_event(self, event):
        print("Connection Event:", event)

    def randomize_mapping(self):
        mapping = get_random_mapping()
        self.virt_gp.set_custom_mapping(mapping)


print(get_connected())

my_handler = RandomVirtualController()  # 0: specify used controller
my_gamepad_thread = GamepadThread(my_handler)

class ConsoleThread(Thread):
    def __init__(self, input_callback = None, name="input-thread"):
        self.input_callback = input_callback
        super(ConsoleThread, self).__init__(name=name)
        self.start()

    def run(self):
        while True:
            self.input_callback(input("Press enter to randomize your mapping"))

def my_input(input_text):
    if input_text == "exit":
        exit(0)

    my_handler.randomize_mapping()
    print("Randomized!")

cthread = ConsoleThread(my_input)

while (1):
    sleep(5)


# my_gamepad_thread.stop()
