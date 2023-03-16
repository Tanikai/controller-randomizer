from XInput import EventHandler, EVENT_BUTTON_PRESSED, FILTER_NONE
from .mapped_vgamepad import MappedVirtualGamepad
from .mapping import Button, get_random_mapping
from .efficient_gamepad_thread import EfficientGamepadThread


class RandomizedGamepadHandler(EventHandler):
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


class RandomizedGamepadThread:
    def __init__(self):
        self.gamepad_handler = RandomizedGamepadHandler()
        self.gamepad_thread = None

    def start(self):
        self.gamepad_thread = EfficientGamepadThread(self.gamepad_handler)

    def stop(self):
        self.gamepad_thread.stop()

    def randomize(self):
        self.gamepad_handler.randomize_mapping()
