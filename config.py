import os

from libqtile import bar, layout, widget
from libqtile.config import Match, Screen
from libqtile.lazy import lazy
from libqtile.log_utils import logger
from libqtile.utils import guess_terminal

from colors import Color
from commands import commands
from keys import keys, mouse
from layouts import layouts
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
                widget.Spacer(bar.STRETCH),
                *RightPowerline(
                    widget.CPU(
                        fmt="{}",
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
                    widget.Memory(
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
                    widget.Net(background=Color.PURPLE.value),
                    widget.NetGraph(
                        type="line",
                        border_width=1,
                        line_width=1,
                        graph_color=Color.FOREGROUND.value,
                        border_color=Color.FOREGROUND.value,
                        background=Color.PURPLE.value,
                    ),
                    widget.ThermalSensor(background=Color.RED.value),
                    widget.OpenWeather(
                        background=Color.ORANGE.value,
                        location="Maringa, BR",
                        format="{main_temp: .0f}°{units_temperature} {icon} ({weather_details})",
                    ),
                    terminator_size=top_bar_size - 2,
                    # widget.Bluetooth(),
                ).widgets,
                widget.Sep(),
                widget.Volume(
                    emoji=True,
                    fmt="Vol: {}",
                    mouse_callbacks={"Button3": lazy.spawn("pavucontrol -t 5")},
                ),
                widget.Volume(
                    emoji=False,
                    fmt="{}",
                    mouse_callbacks={"Button3": lazy.spawn("pavucontrol -t 5")},
                ),
                widget.Sep(),
                widget.Systray(),
            ],
            margin=0,
            border_width=0,
            background=Color.BACKGROUND.value,
        ),
        bottom=bar.Bar(
            [
                *LeftPowerline(
                    widget.CurrentLayoutIcon(
                        scale=0.7,
                        background=Color.BLUE.value,
                        foreground=Color.FOREGROUND.value,
                    ),
                    terminator_size=bottom_bar_size - 2,
                ).widgets,
                shared_task_list(),
                widget.Spacer(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                *RightPowerline(
                    widget.Clipboard(
                        background=Color.CYAN.value,
                    ),
                    widget.Notify(
                        fmt="🔔 {} ",
                        background=Color.GREEN.value,
                        audiofile=f"{CUR_DIR}/beep.wav",
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


keys = keys
mouse = mouse
layouts = layouts

widget_defaults = dict(
    font="Cascadia Code",
    fontsize=16,
    padding=2,
)
extension_defaults = widget_defaults.copy()

screens = [
    _secondary_screen_left(),
    _main_screen(),
    _secondary_screen_right(),
]


dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    border_focus=Color.GREEN.value,
    border_normal=Color.PURPLE.value,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ],
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wmname = "LG3D"
