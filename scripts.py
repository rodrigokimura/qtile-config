import os
import subprocess
from typing import Any, Dict, Optional, Sequence, Tuple

from libqtile.config import Screen

from colors import kanagawa
from meta_config import BLUETOOTH_DEVICE, CUR_DIR, WIFI_PASSWORD, WIFI_SSID


class CLIValues(tuple):
    def __str__(self):
        return " ".join(str(i) for i in self)


class CLIOptions:
    def __init__(self, opts: Dict[str, Tuple[Any, ...]]) -> None:
        self.opts = {name: CLIValues(cli_args) for name, cli_args in opts.items()}

    def __str__(self) -> str:
        return " ".join(f"--{name} {cli_args}" for name, cli_args in self.opts.items())


class CLICommand(subprocess.Popen):
    def __init__(
        self,
        command: str,
        args: Optional[Sequence[str]] = None,
        options: Optional[CLIOptions] = None,
        cwd: str = ".",
    ) -> None:
        if args:
            args = " ".join(str(i) for i in args)
            command = f"{command} {args}"
        if options:
            command = f"{command} {options}"
        super().__init__(command.split(), cwd=cwd)


class CLICommands:
    def __init__(self, commands: Sequence[CLICommand]) -> None:
        self.commands = commands

    def wait(self) -> None:
        for command in self.commands:
            command.wait()


def generate_wallpapers(screens: Sequence[Screen]):
    base_command = "pipenv run python src/app.py"
    cwd = os.path.expanduser("~/dev/project_wallpaper")

    colors = (
        kanagawa.base03,
        kanagawa.base04,
        kanagawa.base05,
        kanagawa.base08,
        kanagawa.base09,
        kanagawa.base0C,
        kanagawa.base00,
    )
    radius = int(((1920 * 1.5) ** 2 + (1080) ** 2) ** 0.5)
    wp_configs = {
        1: CLIOptions(
            {
                "center": (int(1920 * 1.5), 0),
                "radius": (radius,),
            }
        ),
        2: CLIOptions(
            {
                "center": (int(1920 / 2), 0),
                "radius": (radius,),
            }
        ),
        3: CLIOptions(
            {
                "center": (int(-1920 / 2), 0),
                "radius": (radius,),
            }
        ),
    }

    commands = CLICommands(
        [
            CLICommand(
                base_command,
                [f"{CUR_DIR}/wallpapers/wp{index}.png", *colors],
                cwd=cwd,
                options=options,
            )
            for index, options in wp_configs.items()
        ]
    )
    commands.wait()

    for index, screen in enumerate(screens, start=1):
        screen.cmd_set_wallpaper(f"{CUR_DIR}/wallpapers/wp{index}.png", mode="fill")


def configure_monitors():
    cmd = """
    xrandr --output 'DisplayPort-0'--pos '0x0' --left-of 'HDMI-A-0'
     --output 'HDMI-A-0' --pos '1920x0'
     --output 'DVI-D-0' --pos '3840x0' --right-of 'HDMI-A-0'
    """
    cmd = cmd.replace("\n", "")
    cwd = os.path.expanduser("~")
    CLICommand(
        cmd,
        cwd=cwd,
    )


def start_compositor():
    subprocess.Popen("picom".split())


def start_virtual_webcam():
    base_command = "make run"
    cwd = os.path.expanduser("~/dev/project_webcam")
    CLICommand(
        base_command,
        cwd=cwd,
    )


def start_systray_menu():
    base_command = "make run"
    cwd = os.path.expanduser("~/dev/project_systray")
    CLICommand(
        base_command,
        cwd=cwd,
    )


def toggle_audio_profile():
    base_command = "pipenv run python src/app.py"
    cwd = os.path.expanduser("~/dev/project_audio")
    CLICommand(
        base_command,
        cwd=cwd,
    )


def increase_volume():
    CLICommands(
        [
            CLICommand(
                "pulsemixer",
                args=["--change-volume", "+5", "--max-volume", "100"],
            ),
            CLICommand(
                "aplay",
                args=[f"{CUR_DIR}/beep2.wav"],
            ),
        ]
    )


def decrease_volume():
    CLICommands(
        [
            CLICommand(
                "pulsemixer",
                args=["--change-volume", "-5", "--max-volume", "100"],
            ),
            CLICommand(
                "aplay",
                args=[f"{CUR_DIR}/beep2.wav"],
            ),
        ]
    )


def connect_bluetooth():
    base_command = "bluetoothctl connect"
    CLICommand(
        base_command,
        args=[BLUETOOTH_DEVICE],
    )


def connect_wifi():
    base_command = "nmcli device wifi connect"
    CLICommand(
        base_command,
        args=[WIFI_SSID, "password", WIFI_PASSWORD],
    )


def start_calendar():
    base_command = "make run"
    cwd = os.path.expanduser("~/dev/project_calendar")
    CLICommand(
        base_command,
        cwd=cwd,
    )
