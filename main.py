from XInput import EventHandler, GamepadThread, get_connected
from time import sleep


class MyHandler(EventHandler):
    def process_button_event(self, event):
        print("Button Event:", event)
    # put here the code to parse every event related only to the buttons

    def process_trigger_event(self, event):
        print("Trigger Event:", event)
    # event reserved for the two triggers

    def process_stick_event(self, event):
        print("Stick Event:", event)
    # event reserved for the two sticks

    def process_connection_event(self, event):
        print("Connection Event:", event)


print(get_connected())

my_handler = MyHandler(0) # 0: specify used controller
my_gamepad_thread = GamepadThread(my_handler)

while(1):
    sleep(1)


