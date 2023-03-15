from XInput import EventHandler, GamepadThread, get_connected, EVENT_BUTTON_PRESSED, EVENT_BUTTON_RELEASED, FILTER_NONE
import vgamepad as vg
from time import sleep
from strenum import StrEnum


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
    LEFT_TRIGGER = "LEFT_TRIGGER" # analog triggers
    RIGHT_TRIGGER = "RIGHT_TRIGGER"



class MappedVirtualGamepad:
    out_gp = None
    analog_threshold = 0.1  # larger = button pressed

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

    def __init__(self):
        self.out_gp = vg.VX360Gamepad()
    def handle_trigger(self, trigger_button, value):
        if value > self.analog_threshold:
            self.press_button(trigger_button)
        else:
            self.release_button(trigger_button)

    def press_button(self, button):
        if button == Button.LEFT_TRIGGER:
            self.out_gp.left_trigger_float(1)
        elif button == Button.RIGHT_TRIGGER:
            self.out_gp.right_trigger_float(1)
        else:
            self.out_gp.press_button(button=self.xbox_map[button])

        self.out_gp.update()

    def release_button(self, button):
        if button == Button.LEFT_TRIGGER:
            self.out_gp.left_trigger_float(0)
        elif button == Button.RIGHT_TRIGGER:
            self.out_gp.right_trigger_float(0)
        else:
            self.out_gp.release_button(button=self.xbox_map[button])

        self.out_gp.update()


class RandomVirtualController(EventHandler):
    virt_gp = None

    def __init__(self, f=FILTER_NONE):
        super().__init__(0, filter=f)
        self.virt_gp = MappedVirtualGamepad()

    def process_button_event(self, event):
        if event.type == EVENT_BUTTON_PRESSED:
            self.virt_gp.press_button(event.button)
        else:
            self.virt_gp.release_button(event.button)

        print("Button Event:", event)

    # put here the code to parse every event related only to the buttons

    def process_trigger_event(self, event):
        # 0: Left Trigger
        # 1: Right Trigger
        trigger = ""
        if event.trigger == 0:
            trigger = Button.LEFT_TRIGGER
        else:
            trigger = Button.RIGHT_TRIGGER

        self.virt_gp.handle_trigger(trigger, event.value)
        print("Trigger Event:", event)

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


print(get_connected())

my_handler = RandomVirtualController()  # 0: specify used controller
my_gamepad_thread = GamepadThread(my_handler)

while (1):
    sleep(5)

# my_gamepad_thread.stop()
