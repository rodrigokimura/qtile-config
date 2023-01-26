# What is [Qtile](https://github.com/qtile/qtile)?

A full-featured, hackable tiling window manager written and configured in Python

## Features

- Simple, small and extensible. It's easy to write your own layouts, widgets and commands.
- Configured in Python.
- Runs as an X11 WM or a Wayland compositor.
- Command shell that allows all aspects of Qtile to be managed and inspected.
- Complete remote scriptability - write scripts to set up workspaces, manipulate windows, update status bar widgets and more.
- Qtile's remote scriptability makes it one of the most thoroughly unit-tested window managers around.


# My custom features

- Volume widget with progress bar and notification (dunst 1.9)
![Volume widget](https://raw.githubusercontent.com/rodrigokimura/qtile-config/master/screenshots/volume.png)
- Helper class for Powerline terminators
- Custom Column layout:
    - Command to move window to right/left column moves to next screen when in last/first column;
    - Command to focus window to right/left moves focus to next screen when in last/first column;
- Custom Max layout:
    - Implements command to move/focus window to match custom column layout (above);

# Screenshots 🖵

![Qtile Screenshots](https://raw.githubusercontent.com/rodrigokimura/qtile-config/master/screenshots/main_screen.png)
