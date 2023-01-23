import os

from libqtile import bar, widget
from libqtile.config import Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from colors import Color
from widgets import LeftPowerline, RightPowerline, shared_task_list

CUR_DIR = os.path.realpath(os.path.dirname(__file__))

_terminal = guess_terminal()
_wallpaper_name = "stanislausnationalforest"


def _main_screen():
    top_bar_size = 26
    bottom_bar_size = 26
    return Screen(
        wallpaper=f"~/Pictures/triple-monitor/{_wallpaper_name}_2.jpg",
        wallpaper_mode="fill",
        top=bar.Bar(
            size=top_bar_size,
            widgets=[
                *LeftPowerline(
                    widget.ThermalSensor(background=Color.RED.value),
                    widget.CPUGraph(
                        type="line",
                        border_width=1,
                        line_width=1,
                        graph_color=Color.FOREGROUND.value,
                        border_color=Color.FOREGROUND.value,
                        background=Color.BLUE.value,
                        mouse_callbacks={
                            "Button1": lazy.spawn(_terminal + " -e bashtop")
                        },
                    ),
                    widget.CPU(
                        fmt="{}",
                        background=Color.BLUE.value,
                        mouse_callbacks={
                            "Button1": lazy.spawn(_terminal + " -e bashtop")
                        },
                    ),
                    widget.MemoryGraph(
                        type="line",
                        border_width=1,
                        line_width=1,
                        graph_color=Color.FOREGROUND.value,
                        border_color=Color.FOREGROUND.value,
                        background=Color.GREEN.value,
                        mouse_callbacks={
                            "Button1": lazy.spawn(_terminal + " -e bashtop")
                        },
                    ),
                    widget.Memory(
                        background=Color.GREEN.value,
                        mouse_callbacks={
                            "Button1": lazy.spawn(_terminal + " -e bashtop")
                        },
                    ),
                    widget.NetGraph(
                        type="line",
                        border_width=1,
                        line_width=1,
                        graph_color=Color.FOREGROUND.value,
                        border_color=Color.FOREGROUND.value,
                        background=Color.PURPLE.value,
                    ),
                    widget.Net(background=Color.PURPLE.value),
                ).widgets,
                widget.Spacer(bar.STRETCH),
                *RightPowerline(
                    widget.OpenWeather(
                        background=Color.ORANGE.value,
                        location="Maringa, BR",
                        format="{main_temp: .0f}°{units_temperature} {icon} ({weather_details})",
                    ),
                    widget.Volume(
                        background=Color.GREEN.value,
                        emoji=True,
                        fmt="Vol: {}",
                        mouse_callbacks={"Button3": lazy.spawn("pavucontrol -t 5")},
                    ),
                    widget.Volume(
                        background=Color.GREEN.value,
                        emoji=False,
                        fmt="{}",
                        mouse_callbacks={"Button3": lazy.spawn("pavucontrol -t 5")},
                    ),
                    widget.Systray(
                        background=Color.RED.value,
                    ),
                    terminator_size=top_bar_size - 2,
                    # widget.Bluetooth(),
                ).widgets,
            ],
            margin=0,
            border_width=0,
            background=Color.BACKGROUND.value,
        ),
        bottom=bar.Bar(
            [
                *LeftPowerline(
                    widget.CurrentScreen(
                        active_text=" ⬤",
                        inactive_text=" ◯",
                        active_color=Color.FOREGROUND.value,
                        inactive_color=Color.FOREGROUND.value,
                        background=Color.GREEN.value,
                        foreground=Color.FOREGROUND.value,
                    ),
                    widget.CurrentLayoutIcon(
                        scale=0.7,
                        background=Color.BLUE.value,
                        foreground=Color.FOREGROUND.value,
                    ),
                    terminator_size=bottom_bar_size - 2,
                ).widgets,
                shared_task_list(),
                *RightPowerline(
                    widget.Clipboard(
                        fmt="📋 {}",
                        background=Color.GREEN.value,
                        max_width=20,
                    ),
                    widget.Notify(
                        fmt="🔔 {} ",
                        background=Color.GREEN.value,
                        audiofile=f"{CUR_DIR}/beep.wav",
                        scroll=True,
                        width=200,
                    ),
                    widget.Clock(
                        format="📅 %d/%m/%Y %a 🕑 %H:%M",
                        background=Color.BLUE.value,
                    ),
                    widget.QuickExit(
                        default_text="[X]",
                        countdown_format="[{}]",
                        background=Color.RED.value,
                    ),
                ).widgets,
            ],
            size=bottom_bar_size,
        ),
    )


def _secondary_screen_left():
    bottom_bar_size = 26
    return Screen(
        wallpaper=f"~/Pictures/triple-monitor/{_wallpaper_name}_1.jpg",
        wallpaper_mode="fill",
        bottom=bar.Bar(
            [
                *LeftPowerline(
                    widget.CurrentScreen(
                        active_text=" ⬤",
                        inactive_text=" ◯",
                        active_color=Color.FOREGROUND.value,
                        inactive_color=Color.FOREGROUND.value,
                        background=Color.GREEN.value,
                        foreground=Color.FOREGROUND.value,
                    ),
                    widget.CurrentLayoutIcon(
                        scale=0.7,
                        background=Color.BLUE.value,
                        foreground=Color.FOREGROUND.value,
                    ),
                    terminator_size=bottom_bar_size - 2,
                ).widgets,
                shared_task_list(),
                widget.Spacer(bar.STRETCH),
            ],
            size=bottom_bar_size,
        ),
    )


def _secondary_screen_right():
    bottom_bar_size = 26
    return Screen(
        wallpaper=f"~/Pictures/triple-monitor/{_wallpaper_name}_3.jpg",
        wallpaper_mode="fill",
        bottom=bar.Bar(
            [
                *LeftPowerline(
                    widget.CurrentScreen(
                        active_text=" ⬤",
                        inactive_text=" ◯",
                        active_color=Color.FOREGROUND.value,
                        inactive_color=Color.FOREGROUND.value,
                        background=Color.GREEN.value,
                        foreground=Color.FOREGROUND.value,
                    ),
                    widget.CurrentLayoutIcon(
                        scale=0.7,
                        background=Color.BLUE.value,
                        foreground=Color.FOREGROUND.value,
                    ),
                    terminator_size=bottom_bar_size - 2,
                ).widgets,
                shared_task_list(),
                widget.Spacer(),
            ],
            size=bottom_bar_size,
        ),
    )


screens = [
    _secondary_screen_left(),
    _main_screen(),
    _secondary_screen_right(),
]
