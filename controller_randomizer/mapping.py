from strenum import StrEnum
from typing import Dict
import random
import vgamepad as vg


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


def get_random_mapping() -> Dict[Button, Button]:
    # TODO implement randomizing algorithm
    available_buttons = list(randomized_buttons)
    random.shuffle(available_buttons)
    for key in randomized_mapping:
        randomized_mapping[key] = available_buttons.pop()

    final_dict = dict(const_mapping)
    final_dict.update(randomized_mapping)
    return final_dict


# These buttons are not changed during randomization
const_mapping = {
    Button.START: Button.START,
    Button.BACK: Button.BACK,
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
