import os
import subprocess
from typing import Any, Dict, Optional, Sequence, Tuple

from libqtile.config import Screen


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
        cwd: str = "/",
    ) -> None:
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
        "#a57662",
        "#182931",
    )

    wp_configs = {
        1: CLIOptions(
            {
                "start": (0, 0),
                "end": (1920, 1080),
                "colors": colors,
            }
        ),
        2: CLIOptions(
            {
                "start": (0, -2333),
                "end": (0, 1080),
                "colors": colors,
            }
        ),
        3: CLIOptions(
            {
                "start": (1920, 0),
                "end": (0, 1080),
                "colors": colors,
            }
        ),
    }

    commands = CLICommands(
        [
            CLICommand(
                base_command,
                f"wp{index}.png",
                cwd=cwd,
                options=options,
            )
            for index, options in wp_configs.items()
        ]
    )

    commands.wait()

    for i, screen in enumerate(screens, start=1):
        screen.cmd_set_wallpaper(
            os.path.expanduser(f"~/dev/project_wallpaper/wp{i}.png"), mode="fill"
        )


def start_compositor():
    subprocess.Popen(
        "picom --experimental-backends".split(),
    )
