from typing import Dict
from .mapping import Button, xbox_map
import vgamepad as vg


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
