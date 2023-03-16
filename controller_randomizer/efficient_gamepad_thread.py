"""
zlib/libpng license

Copyright (c) 2023 Kai Anter

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.
2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.
3. This notice may not be removed or altered from any source distribution.

This source file is derived from github.com/Zuzu-Typ/XInput-Python/XInput.py Version 0.4.0.

-----

zlib/libpng license

Copyright (c) 2019 Zuzu_Typ

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.
2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.
3. This notice may not be removed or altered from any source distribution.
"""

from XInput import (EventHandler,
                    EVENT_CONNECTED,
                    EVENT_DISCONNECTED,
                    EVENT_BUTTON_PRESSED,
                    EVENT_BUTTON_RELEASED,
                    FILTER_PRESSED_ONLY,
                    FILTER_RELEASED_ONLY,
                    EVENT_TRIGGER_MOVED,
                    TRIGGER_LEFT,
                    EVENT_STICK_MOVED,
                    STICK_LEFT,
                    get_events)
from threading import Thread, Event
import time


class EfficientGamepadThread(Thread):
    """This class serves as a more efficient replacement for the original Xinput.py/GamepadThread class.
    Instead of always polling the controllers for new events, this new class has a polling rate of around 1000 Hz,
    which results in a lower CPU usage.

    Another change to the original class is that it only supports adding new handlers during init time.
    This might be changed later.
    """

    def __init__(self, *event_handlers, auto_start=True):
        super().__init__(daemon=True)

        for event_handler in event_handlers:
            if event_handler is None or not issubclass(type(event_handler), EventHandler):
                raise TypeError("The event handler must be a subclass of XInput.EventHandler")

        self.handlers = set(event_handlers)
        self.event = Event()  # exit condition for thread

        if auto_start:
            self.start()

    def run(self):
        """
        This is the polling function. It gets the changes that occurred since get_event was last called and then
        triggers events for the handler.
        :return:
        """
        while not self.event.is_set():
            self._refresh_events()
            time.sleep(0.001)  # not really 1000Hz but close enough

    def stop(self):
        self.event.set()

    def _refresh_events(self):
        events = get_events()
        for event in events:  # filtering events
            if event.type == EVENT_CONNECTED or event.type == EVENT_DISCONNECTED:
                for handler in self.handlers:
                    if handler.has_controller(event.user_index):
                        handler.process_connection_event(event)

            elif event.type == EVENT_BUTTON_PRESSED or event.type == EVENT_BUTTON_RELEASED:
                for handler in self.handlers:
                    if handler.has_controller(event.user_index):
                        if not ((handler.filter & (FILTER_PRESSED_ONLY + FILTER_RELEASED_ONLY)) and not (
                                handler.filter & (FILTER_PRESSED_ONLY << (event.type - EVENT_BUTTON_PRESSED)))):
                            if event.button_id & handler.filter:
                                handler.process_button_event(event)
            elif event.type == EVENT_TRIGGER_MOVED:
                for handler in self.handlers:
                    if handler.has_controller(event.user_index):
                        if (TRIGGER_LEFT << event.trigger) & handler.filter:
                            handler.process_trigger_event(event)
            elif event.type == EVENT_STICK_MOVED:
                for handler in self.handlers:
                    if handler.has_controller(event.user_index):
                        if (STICK_LEFT << event.stick) & handler.filter:
                            handler.process_stick_event(event)
            else:
                raise ValueError("Event type not recognized")
