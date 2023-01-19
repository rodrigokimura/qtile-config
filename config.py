import enum

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.log_utils import logger
from libqtile.utils import guess_terminal

from keys import Modifiers, keys
from layouts import Columns


class Color(enum.Enum):
    BACKGROUND = "#282a36"
    FOREGROUND = "#f8f8f2"
    GREY = "#44475a"
    BLUE = "#6272a4"
    CYAN = "#8be9fd"
    GREEN = "#3caea3"
    ORANGE = "#ffb86c"
    PINK = "#ff79c6"
    PURPLE = "#bd93f9"
    RED = "#ff5555"
    YELLOW = "#f1fa8c"


def _parse_text(text: str):
    if " - " in text:
        return text.split(" - ")[-1]
    if "Google Chrome" in text:
        text = "Chrome"
    if "Firefox" in text:
        text = "Firefox"
    if "Visual Studio Code" in text:
        text = "VSCode"
    return text


def _main_screen():
    return Screen(
        wallpaper=f"~/Pictures/triple-monitor/{_wallpaper_name}_2.jpg",
        wallpaper_mode="fill",
        top=bar.Bar(
            [
                widget.Spacer(),
                widget.CPU(background=Color.BLUE.value, mouse_callbacks={'Button1': lazy.spawn( _terminal + ' -e bashtop')}),
                widget.CPUGraph(
                    type="line",
                    border_width=1,
                    line_width=1,
                    graph_color=Color.FOREGROUND.value,
                    border_color=Color.FOREGROUND.value,
                    background=Color.BLUE.value,
                    mouse_callbacks={'Button1': lazy.spawn( _terminal + ' -e bashtop')}
                ),
                widget.Memory(background=Color.GREEN.value, mouse_callbacks={'Button1': lazy.spawn( _terminal + ' -e bashtop')}),
                widget.MemoryGraph(
                    type="line",
                    border_width=1,
                    line_width=1,
                    graph_color=Color.FOREGROUND.value,
                    border_color=Color.FOREGROUND.value,
                    background=Color.GREEN.value,
                    mouse_callbacks={'Button1': lazy.spawn( _terminal + ' -e bashtop')}
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
                    format="{main_temp: .0f}°{units_temperature} {weather_details}",
                ),
                widget.Sep(),
                widget.Volume(emoji=True, fmt='Vol: {}'),
                widget.Volume(emoji=False, fmt='{}'),
                widget.Sep(),
                # widget.Bluetooth(),
                widget.Systray(),
            ],
            32,
            background=Color.BACKGROUND.value,
        ),
        bottom=bar.Bar(
            [
                widget.CurrentLayoutIcon(),
                widget.LaunchBar(
                    progs=[
                        ("code", "code"),
                        ("chrome", "google-chrome"),
                        ("edge", 'microsoft-edge-stable --proxy-server="http://192.168.0.119:8899;https://192.168.0.119:8899"'),
                        ("slack", "flatpak run com.slack.Slack"),
                        ("audio", "gnome-control-center sound"),
                    ],
                    text_only=True,
                ),
                widget.Prompt(),
                widget.Sep(),
                widget.TaskList(parse_text=_parse_text),
                widget.Spacer(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Clock(format="📅 %d/%m/%Y %a 🕑 %H:%M"),
                widget.QuickExit(default_text="[X]", countdown_format="[{}]"),
            ],
            32,
        ),
    )


def _secondary_screen_left():
    return Screen(
        wallpaper=f"~/Pictures/triple-monitor/{_wallpaper_name}_1.jpg",
        wallpaper_mode="fill",
        bottom=bar.Bar(
            [
                widget.CurrentLayoutIcon(),
                widget.TaskList(parse_text=_parse_text),
            ],
            32,
        ),
    )


def _secondary_screen_right():
    return Screen(
        wallpaper=f"~/Pictures/triple-monitor/{_wallpaper_name}_3.jpg",
        wallpaper_mode="fill",
        bottom=bar.Bar(
            [
                widget.CurrentLayoutIcon(),
                widget.TaskList(parse_text=_parse_text),
            ],
            32,
        ),
    )

keys = keys

layouts = [
    Columns(
        border_focus=Color.BLUE.value,
        border_focus_stack=Color.BLUE.value,
        border_width=4,
        border_on_single=True,
        margin=3,
        margin_on_single=5,
        wrap_focus_columns=False,
        wrap_focus_rows=False,
        wrap_focus_stacks=False,
    ),
    layout.Max(),
]

widget_defaults = dict(
    font="Cascadia Code",
    fontsize=16,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    _secondary_screen_left(),
    _main_screen(),
    _secondary_screen_right(),
]

mouse = [
    Drag(
        [Modifiers.META.value],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [Modifiers.META.value],
        "Button3",
        lazy.window.set_size_floating(),
        start=lazy.window.get_size(),
    ),
    Click([Modifiers.META.value], "Button3", lazy.window.toggle_floating()),
    Click([Modifiers.META.value], "Button2", lazy.window.toggle_fullscreen()),
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
