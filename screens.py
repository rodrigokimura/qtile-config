from libqtile import bar, widget
from libqtile.config import Screen
from libqtile.lazy import lazy

from colors import kanagawa
from commands import open_calendar
from meta_config import BLUETOOTH_DEVICE, TERMINAL
from widgets import CurrentLayout, CurrentScreen, DynamicTerminator
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
                        background=kanagawa.base0C,
                        foreground=kanagawa.base00,
                    ),
                    (
                        widget.CPU(
                            format=" {load_percent:.1f}%",
                            background=kanagawa.base02,
                            mouse_callbacks={
                                "Button1": lazy.spawn(TERMINAL + " -e bashtop")
                            },
                        ),
                        widget.CPUGraph(
                            type="line",
                            border_width=1,
                            line_width=1,
                            graph_color=kanagawa.base04,
                            border_color=kanagawa.base04,
                            background=kanagawa.base02,
                            mouse_callbacks={
                                "Button1": lazy.spawn(TERMINAL + " -e bashtop")
                            },
                        ),
                    ),
                    (
                        widget.Memory(
                            format=" {MemPercent:.1f}%",
                            background=kanagawa.base01,
                            mouse_callbacks={
                                "Button1": lazy.spawn(TERMINAL + " -e bashtop")
                            },
                        ),
                        widget.MemoryGraph(
                            type="line",
                            border_width=1,
                            line_width=1,
                            graph_color=kanagawa.base04,
                            border_color=kanagawa.base04,
                            background=kanagawa.base01,
                            mouse_callbacks={
                                "Button1": lazy.spawn(TERMINAL + " -e bashtop")
                            },
                        ),
                    ),
                    (
                        widget.Net(
                            format=" {down} \u2193\u2191 {up}",
                            background=kanagawa.base02,
                        ),
                        widget.NetGraph(
                            type="line",
                            border_width=1,
                            line_width=1,
                            graph_color=kanagawa.base04,
                            border_color=kanagawa.base04,
                            background=kanagawa.base02,
                        ),
                    ),
                ).widgets,
                widget.Spacer(bar.STRETCH),
                *RightPowerline(
                    # widget.OpenWeather(
                    #     background=Color.DARK.value,
                    #     location="Maringa, BR",
                    #     format="{main_temp:.0f}°{units_temperature} ",
                    # ),
                    Volume(
                        background=kanagawa.base02,
                        mouse_callbacks={
                            "Button3": lazy.spawn("pavucontrol -t 5"),
                        },
                    ),
                    widget.Bluetooth(
                        hci=f"/dev_{BLUETOOTH_DEVICE.replace(':', '_')}",
                        background=kanagawa.base01,
                        fmt="{} ",
                    ),
                    widget.Systray(
                        background=kanagawa.base0C,
                        fmt="{} ",
                    ),
                    widget.Sep(
                        linewidth=0,
                        background=kanagawa.base0C,
                    ),
                    terminator_size=top_bar_size - 2,
                ).widgets,
            ],
            margin=0,
            border_width=0,
            background=kanagawa.base00,
        ),
        bottom=bar.Bar(
            [
                CurrentScreen(
                    fmt=" {}",
                    active_text="⬤",
                    inactive_text="◯",
                    active_color=kanagawa.base00,
                    inactive_color=kanagawa.base00,
                    active_background_color=kanagawa.base0B,
                    inactive_background_color=kanagawa.base0C,
                    background=kanagawa.base0C,
                    foreground=kanagawa.base00,
                ),
                DynamicTerminator(
                    fmt="",
                    active_foreground=kanagawa.base0B,
                    foreground=kanagawa.base0C,
                    background=kanagawa.base0D,
                    fontsize=26,
                    padding=0,
                    markup=False,
                    hack_offset=0,
                    font="MesloLGS NF",
                ),
                *LeftPowerline(
                    CurrentLayout(
                        fontsize=30,
                        padding=8,
                        background=kanagawa.base0D,
                        foreground=kanagawa.base00,
                    ),
                    terminator_size=bottom_bar_size - 2,
                ).widgets,
                shared_task_list(),
                *RightPowerline(
                    widget.Clipboard(
                        fmt="📋 {}",
                        background=kanagawa.base02,
                        max_width=20,
                    ),
                    widget.Clock(
                        format="%d/%m/%Y %H:%M ",
                        background=kanagawa.base0D,
                        foreground=kanagawa.base00,
                        mouse_callbacks={"Button1": lazy.spawn(open_calendar.command)},
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
                CurrentScreen(
                    fmt=" {}",
                    active_text="⬤",
                    inactive_text="◯",
                    active_color=kanagawa.base00,
                    inactive_color=kanagawa.base00,
                    active_background_color=kanagawa.base0B,
                    inactive_background_color=kanagawa.base0C,
                    background=kanagawa.base0C,
                    foreground=kanagawa.base00,
                ),
                DynamicTerminator(
                    fmt="",
                    active_foreground=kanagawa.base0B,
                    foreground=kanagawa.base0C,
                    background=kanagawa.base0D,
                    fontsize=26,
                    padding=0,
                    markup=False,
                    hack_offset=0,
                    font="MesloLGS NF",
                ),
                *LeftPowerline(
                    CurrentLayout(
                        fontsize=30,
                        padding=8,
                        background=kanagawa.base0D,
                        foreground=kanagawa.base00,
                    ),
                    terminator_size=bottom_bar_size - 2,
                ).widgets,
                shared_task_list(),
                widget.Spacer(bar.STRETCH),
            ],
            size=bottom_bar_size,
            background=kanagawa.base00,
        ),
    )


def _secondary_screen_right():
    bottom_bar_size = 26
    return Screen(
        bottom=bar.Bar(
            [
                CurrentScreen(
                    fmt=" {}",
                    active_text="⬤",
                    inactive_text="◯",
                    active_color=kanagawa.base00,
                    inactive_color=kanagawa.base00,
                    active_background_color=kanagawa.base0B,
                    inactive_background_color=kanagawa.base0C,
                    background=kanagawa.base0C,
                    foreground=kanagawa.base00,
                ),
                DynamicTerminator(
                    fmt="",
                    active_foreground=kanagawa.base0B,
                    foreground=kanagawa.base0C,
                    background=kanagawa.base0D,
                    fontsize=26,
                    padding=0,
                    markup=False,
                    hack_offset=0,
                    font="MesloLGS NF",
                ),
                *LeftPowerline(
                    CurrentLayout(
                        fmt="{}",
                        fontsize=30,
                        padding=8,
                        background=kanagawa.base0D,
                        foreground=kanagawa.base00,
                    ),
                    terminator_size=bottom_bar_size - 2,
                ).widgets,
                shared_task_list(),
                widget.Spacer(),
            ],
            size=bottom_bar_size,
            background=kanagawa.base00,
        ),
    )


screens = [
    _secondary_screen_left(),
    _main_screen(),
    _secondary_screen_right(),
]
