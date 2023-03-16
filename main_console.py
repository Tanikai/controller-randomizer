from controller_randomizer.gamepad_randomizer import RandomizedGamepadThread
from threading import Thread
from time import sleep


class ConsoleThread(Thread):
    def __init__(self, input_callback=None, name="input-thread"):
        self.input_callback = input_callback
        super(ConsoleThread, self).__init__(name=name)
        self.start()

    def run(self):
        while True:
            self.input_callback(input("Press enter to randomize your mapping"))


if __name__ == "__main__":

    def console_input(input_text):
        if input_text == "exit":
            exit(0)

        gamepad_thread.randomize()
        print("Randomized!")


    cthread = ConsoleThread(console_input)

    gamepad_thread = RandomizedGamepadThread()
    gamepad_thread.start()

    while 1:
        sleep(5)
