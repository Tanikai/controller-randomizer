import tkinter as tk
from controller_randomizer.gamepad_randomizer import RandomizedGamepadThread
from datetime import datetime
from XInput import get_connected


class Application:

    def __init__(self):
        self.gamepad_thread = RandomizedGamepadThread()
        self.gamepad_thread.start()

        self.root = tk.Tk()
        self.root.title = "Controller Randomizer"
        self.root.geometry("300x200")

        self.fr_status = tk.Frame(self.root)
        self.fr_status.pack(side=tk.TOP, fill=tk.X)

        self.fr_controls = tk.Frame(self.root)
        self.fr_controls.pack(side=tk.TOP, fill=tk.X)

        self.bt_randomize = tk.Button(self.fr_controls, text="Randomize Mapping", command=self._on_randomize_click)
        self.bt_randomize.pack(side=tk.LEFT)

        self.me_output = tk.Listbox(self.root)
        self.me_output.pack(fill=tk.X)

    def start(self):
        try:
            self.log("--- Controller Randomizer ---")
            self.root.mainloop()
        except Exception as e:
            print("Exception in GUI thread:", e)
        finally:
            self.cleanup()

    def cleanup(self):
        self.gamepad_thread.stop()

    def _on_randomize_click(self):
        self.gamepad_thread.randomize()
        self.log("Randomized!")

    def log(self, msg):
        self.me_output.insert(tk.END, datetime.now().strftime("%H:%M:%S - ") + msg)


if __name__ == "__main__":
    connected = get_connected()
    if not connected[0]:
        print("Error: Controller 1 has to be connected")
        exit(1)
    elif connected[1]:
        print("Error: Controller 2 is already in use")
        exit(1)

    a = Application()
    a.start()
