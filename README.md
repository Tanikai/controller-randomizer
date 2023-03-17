# Controller-Randomizer

## About

This project reads the button presses of an XInput controller, maps it to other buttons defined in a randomized keymap, 
and sends the mapped inputs to a virtual controller. The virtual controller can be used in your favorite game for extra
fun and confusion during your gameplay.

## Requirements

- Windows (due to XInput)
- Python 3 (tested with Python 3.10)

## Installation

During installation of the requirements, a wizard for the *ViGEmBus* driver installation will open.

```shell
git clone https://github.com/Tanikai/controller-randomizer.git
cd controller-randomizer
pip install -r requirements.txt
```

## Usage

Run the randomizer with:

```shell
python main_gui.py
```

Your input controller has to be connected as Player 1.

## Contact

- **Kai Anter** - [GitHub](https://github.com/Tanikai) - [Mastodon](https://hachyderm.io/@tanikai)
