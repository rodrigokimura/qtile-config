import os

from libqtile import bar, widget
from libqtile.config import Screen
from libqtile.lazy import lazy

from colors import Color
from widgets import LeftPowerline, RightPowerline, Volume, shared_task_list

CUR_DIR = os.path.realpath(os.path.dirname(__file__))

_terminal = "kitty"
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
                    widget.ThermalSensor(fmt=" {}", background=Color.RED.value),
                    (
                        widget.CPU(
                            fmt=" {}",
                            background=Color.BLUE.value,
                            mouse_callbacks={
                                "Button1": lazy.spawn(_terminal + " -e bashtop")
                            },
                        ),
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
                    ),
                    (
                        widget.Memory(
                            fmt="{}",
                            background=Color.GREEN.value,
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
                    ),
                    (
                        widget.Net(fmt=" {}", background=Color.PURPLE.value),
                        widget.NetGraph(
                            type="line",
                            border_width=1,
                            line_width=1,
                            graph_color=Color.FOREGROUND.value,
                            border_color=Color.FOREGROUND.value,
                            background=Color.PURPLE.value,
                        ),
                    ),
                ).widgets,
                widget.Spacer(bar.STRETCH),
                *RightPowerline(
                    widget.OpenWeather(
                        background=Color.ORANGE.value,
                        location="Maringa, BR",
                        format="{main_temp: .0f}°{units_temperature} {icon} ({weather_details})",
                    ),
                    Volume(
                        background=Color.GREEN.value,
                        emoji=True,
                        fmt="{} ",
                        step=5,
                        mouse_callbacks={"Button3": lazy.spawn("pavucontrol -t 5")},
                    ),
                    widget.Bluetooth(
                        hci="/dev_44_73_D6_A4_E8_6C",
                        background=Color.RED.value,
                        fmt=" {} ",
                    ),
                    widget.Systray(
                        background=Color.RED.value,
                    ),
                    terminator_size=top_bar_size - 2,
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
                    widget.Clock(
                        format="📅 %d/%m/%Y %a 🕑 %H:%M ",
                        background=Color.BLUE.value,
                        mouse_callbacks={
                            "Button1": lazy.spawn(
                                _terminal
                                + ' --hold -e python3 -c "from datetime import datetime; from calendar import TextCalendar; now = datetime.now(); TextCalendar().prmonth(now.year, now.month)"'
                            )
                        },
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
