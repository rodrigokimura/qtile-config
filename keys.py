import enum

from libqtile.config import Key
from libqtile.lazy import lazy
from libqtile.log_utils import logger
from libqtile.utils import guess_terminal


class Arrows(enum.Enum):
    LEFT = "Left"
    RIGHT = "Right"
    UP = "Up"
    DOWN = "Down"


class Modifiers(enum.Enum):
    META = "mod4"
    ALT = "mod1"
    CTRL = "control"
    SHIFT = "shift"


_terminal = guess_terminal()

_wallpaper_name = "stanislausnationalforest"

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
        lazy.spawn(_terminal),
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
        [Modifiers.META.value, "control"],
        "r",
        lazy.reload_config(),
        desc="Reload the config",
    ),
    Key(
        [Modifiers.META.value],
        "r",
        lazy.spawncmd(),
        desc="Spawn a command using a prompt widget",
    ),
]


_media_keys = [
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("amixer sset 'Master' 5%+"),
        desc="Launch terminal",
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("amixer sset 'Master' 5%-"),
        desc="Launch terminal",
    ),
]

keys = _focus_keys + _move_keys + _resize_keys + _shortcut_keys + _media_keys