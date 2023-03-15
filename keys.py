import enum

from libqtile import extension
from libqtile.config import Click, Drag, Key
from libqtile.lazy import lazy

from colors import kanagawa
from commands import commands
from meta_config import CUR_DIR, TERMINAL


class Arrows(enum.Enum):
    LEFT = "h"
    RIGHT = "l"
    UP = "k"
    DOWN = "j"


class Modifiers(enum.Enum):
    META = "mod4"
    ALT = "mod1"
    CTRL = "control"
    SHIFT = "shift"


_focus_keys = [
    Key(
        [Modifiers.META.value],
        Arrows.LEFT.value,
        lazy.layout.left(),
        desc="Move focus to left",
    ),
    Key(
        [Modifiers.META.value],
        Arrows.RIGHT.value,
        lazy.layout.right(),
        desc="Move focus to right",
    ),
    Key(
        [Modifiers.META.value],
        Arrows.DOWN.value,
        lazy.layout.down(),
        desc="Move focus down",
    ),
    Key(
        [Modifiers.META.value], Arrows.UP.value, lazy.layout.up(), desc="Move focus up"
    ),
    Key(
        [Modifiers.ALT.value],
        "Tab",
        lazy.layout.next(),
        desc="Move window focus to other window",
    ),
]

_move_keys = [
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [Modifiers.META.value, Modifiers.CTRL.value],
        Arrows.LEFT.value,
        lazy.layout.shuffle_left(),
        desc="Move window to the left",
    ),
    Key(
        [Modifiers.META.value, Modifiers.CTRL.value],
        Arrows.RIGHT.value,
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key(
        [Modifiers.META.value, Modifiers.CTRL.value],
        Arrows.DOWN.value,
        lazy.layout.shuffle_down(),
        desc="Move window down",
    ),
    Key(
        [Modifiers.META.value, Modifiers.CTRL.value],
        Arrows.UP.value,
        lazy.layout.shuffle_up(),
        desc="Move window up",
    ),
    Key(
        [Modifiers.META.value, Modifiers.SHIFT.value],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
]

_resize_keys = [
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key(
        [Modifiers.META.value, Modifiers.SHIFT.value],
        Arrows.LEFT.value,
        lazy.layout.grow_left(),
        desc="Grow window to the left",
    ),
    Key(
        [Modifiers.META.value, Modifiers.SHIFT.value],
        Arrows.RIGHT.value,
        lazy.layout.grow_right(),
        desc="Grow window to the right",
    ),
    Key(
        [Modifiers.META.value, Modifiers.SHIFT.value],
        Arrows.DOWN.value,
        lazy.layout.grow_down(),
        desc="Grow window down",
    ),
    Key(
        [Modifiers.META.value, Modifiers.SHIFT.value],
        Arrows.UP.value,
        lazy.layout.grow_up(),
        desc="Grow window up",
    ),
    Key(
        [Modifiers.META.value],
        "n",
        lazy.layout.normalize(),
        desc="Reset all window sizes",
    ),
]

_shortcut_keys = [
    Key(
        [Modifiers.META.value],
        "Return",
        lazy.spawn(TERMINAL),
        desc="Launch terminal",
    ),
    Key(
        [Modifiers.META.value],
        "Tab",
        lazy.next_layout(),
        desc="Toggle between layouts",
    ),
    Key([Modifiers.META.value], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [Modifiers.META.value, Modifiers.CTRL.value],
        "r",
        lazy.reload_config(),
        desc="Reload the config",
    ),
    Key(
        [Modifiers.META.value, Modifiers.SHIFT.value],
        "s",
        lazy.spawn("flameshot gui"),
        desc="Start a manual capture in GUI mode",
    ),
    Key(
        [Modifiers.META.value],
        "e",
        lazy.spawn(TERMINAL + " -e ranger"),
        desc="Open file manager",
    ),
    Key(
        [Modifiers.META.value],
        "m",
        lazy.run_extension(
            extension.CommandSet(
                fontsize=15,
                dmenu_prompt=">_ ",
                foreground=kanagawa.base0B,
                selected_foreground=kanagawa.base00,
                selected_background=kanagawa.base0B,
                commands={
                    k: v for c in commands for k, v in c.as_command_set_dict().items()
                },
            )
        ),
    ),
]


_media_keys = [
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("pulsemixer --change-volume +5 --max-volume 100"),
        lazy.spawn(f"aplay '{CUR_DIR}/beep2.wav'"),
        desc="Increase volume",
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("pulsemixer --change-volume -5 --max-volume 100"),
        lazy.spawn(f"aplay '{CUR_DIR}/beep2.wav'"),
        desc="Decrease volume",
    ),
    Key(
        [],
        "XF86AudioPlay",
        lazy.spawn("playerctl play-pause"),
        desc="Play/Pause music",
    ),
    Key(
        [],
        "XF86AudioNext",
        lazy.spawn("playerctl next"),
        desc="Next music",
    ),
    Key(
        [],
        "XF86AudioPrev",
        lazy.spawn("playerctl previous"),
        desc="Previous music",
    ),
]

keys = _focus_keys + _move_keys + _resize_keys + _shortcut_keys + _media_keys

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
    Click([Modifiers.META.value], "Button2", lazy.window.toggle_floating()),
]
