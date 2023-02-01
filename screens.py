import os

from libqtile import bar, widget
from libqtile.config import Screen
from libqtile.lazy import lazy

from colors import Color
from meta_config import BLUETOOTH_DEVICE, TERMINAL
from widgets import GenericVolume as Volume
from widgets import LeftPowerline, RightPowerline, shared_task_list


def _main_screen():
    top_bar_size = 26
    bottom_bar_size = 26
    return Screen(
        top=bar.Bar(
            size=top_bar_size,
            widgets=[
                *LeftPowerline(
                    widget.ThermalSensor(
                        fmt=" {}",
                        background=Color.MID.value,
                        foreground=Color.FOREGROUND.value,
                    ),
                    (
                        widget.CPU(
                            fmt=" {}",
                            background=Color.DARK.value,
                            mouse_callbacks={
                                "Button1": lazy.spawn(TERMINAL + " -e bashtop")
                            },
                        ),
                        widget.CPUGraph(
                            type="line",
                            border_width=1,
                            line_width=1,
                            graph_color=Color.FOREGROUND.value,
                            border_color=Color.FOREGROUND.value,
                            background=Color.DARK.value,
                            mouse_callbacks={
                                "Button1": lazy.spawn(TERMINAL + " -e bashtop")
                            },
                        ),
                    ),
                    (
                        widget.Memory(
                            fmt="{}",
                            background=Color.MID.value,
                            mouse_callbacks={
                                "Button1": lazy.spawn(TERMINAL + " -e bashtop")
                            },
                        ),
                        widget.MemoryGraph(
                            type="line",
                            border_width=1,
                            line_width=1,
                            graph_color=Color.FOREGROUND.value,
                            border_color=Color.FOREGROUND.value,
                            background=Color.MID.value,
                            mouse_callbacks={
                                "Button1": lazy.spawn(TERMINAL + " -e bashtop")
                            },
                        ),
                    ),
                    (
                        widget.Net(fmt=" {}", background=Color.DARK.value),
                        widget.NetGraph(
                            type="line",
                            border_width=1,
                            line_width=1,
                            graph_color=Color.FOREGROUND.value,
                            border_color=Color.FOREGROUND.value,
                            background=Color.DARK.value,
                        ),
                    ),
                ).widgets,
                widget.Spacer(bar.STRETCH),
                *RightPowerline(
                    widget.OpenWeather(
                        background=Color.DARK.value,
                        location="Maringa, BR",
                        format="{main_temp: .0f}°{units_temperature} {icon} ({weather_details})",
                    ),
                    Volume(
                        background=Color.MID.value,
                        mouse_callbacks={
                            "Button3": lazy.spawn("pavucontrol -t 5"),
                        },
                    ),
                    widget.Bluetooth(
                        hci=f"/dev_{BLUETOOTH_DEVICE.replace(':', '_')}",
                        background=Color.DARK.value,
                        fmt=" {} ",
                    ),
                    widget.Systray(
                        background=Color.DARK.value,
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
                        background=Color.MID.value,
                        foreground=Color.FOREGROUND.value,
                    ),
                    widget.CurrentLayoutIcon(
                        scale=0.7,
                        background=Color.DARK.value,
                        foreground=Color.FOREGROUND.value,
                    ),
                    terminator_size=bottom_bar_size - 2,
                ).widgets,
                shared_task_list(),
                *RightPowerline(
                    widget.Clipboard(
                        fmt="📋 {}",
                        background=Color.MID.value,
                        max_width=20,
                    ),
                    widget.Clock(
                        format="📅 %d/%m/%Y %a 🕑 %H:%M ",
                        background=Color.DARK.value,
                        mouse_callbacks={
                            "Button1": lazy.spawn(
                                TERMINAL
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
        bottom=bar.Bar(
            [
                *LeftPowerline(
                    widget.CurrentScreen(
                        active_text=" ⬤",
                        inactive_text=" ◯",
                        active_color=Color.FOREGROUND.value,
                        inactive_color=Color.FOREGROUND.value,
                        background=Color.MID.value,
                        foreground=Color.FOREGROUND.value,
                    ),
                    widget.CurrentLayoutIcon(
                        scale=0.7,
                        background=Color.DARK.value,
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
        bottom=bar.Bar(
            [
                *LeftPowerline(
                    widget.CurrentScreen(
                        active_text=" ⬤",
                        inactive_text=" ◯",
                        active_color=Color.FOREGROUND.value,
                        inactive_color=Color.FOREGROUND.value,
                        background=Color.MID.value,
                        foreground=Color.FOREGROUND.value,
                    ),
                    widget.CurrentLayoutIcon(
                        scale=0.7,
                        background=Color.DARK.value,
                        foreground=Color.FOREGROUND.value,
                    ),
                    terminator_size=bottom_bar_size - 2,
                ).widgets,
                shared_task_list(),
                widget.Spacer(),
            ],
            size=bottom_bar_size,
            background=Color.BACKGROUND.value,
        ),
    )


screens = [
    _secondary_screen_left(),
    _main_screen(),
    _secondary_screen_right(),
]
