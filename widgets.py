import math
import subprocess
from typing import Any, Iterable, List, Tuple, Union

from libqtile import bar, hook, widget
from libqtile.widget import base
from libqtile.widget.base import _Widget
from libqtile.widget.currentscreen import CurrentScreen as BuiltinCurrentScreen
from libqtile.widget.generic_poll_text import GenPollText
from libqtile.widget.textbox import TextBox
from libqtile.widget.volume import Volume as BuiltinVolume

from colors import kanagawa
from scripts import decrease_volume, increase_volume, toggle_audio_profile


class CurrentLayout(base._TextBox):
    """
    Display the name of the current layout of the current group of the screen,
    the bar containing the widget, is on.
    """

    def __init__(self, width=bar.CALCULATED, **config):
        base._TextBox.__init__(self, "", width, **config)
        self._icon_mapping = {
            "max": "󰁌",
            "columns": "",
        }
        self._fallback_icon = ""

    def _configure(self, qtile, bar):
        base._TextBox._configure(self, qtile, bar)
        layout_id = self.bar.screen.group.current_layout
        self.text = self._icon_mapping.get(
            self.bar.screen.group.layouts[layout_id].name, self._fallback_icon
        )
        self.setup_hooks()

        self.add_callbacks(
            {
                "Button1": qtile.cmd_next_layout,
                "Button2": qtile.cmd_prev_layout,
            }
        )

    def hook_response(self, layout, group):
        if group.screen is not None and group.screen == self.bar.screen:
            self.text = self._icon_mapping.get(layout.name, self._fallback_icon)
            self.bar.draw()

    def setup_hooks(self):
        hook.subscribe.layout_change(self.hook_response)

    def remove_hooks(self):
        hook.unsubscribe.layout_change(self.hook_response)

    def finalize(self):
        self.remove_hooks()
        base._TextBox.finalize(self)


class CurrentScreen(BuiltinCurrentScreen):
    def __init__(self, width=bar.CALCULATED, **config):
        defaults = [
            (
                "active_background_color",
                "00ff00",
                "Background color when screen is active",
            ),
            (
                "inactive_background_color",
                "ff0000",
                "Background color when screen is inactive",
            ),
        ]
        base._TextBox.__init__(self, "", width, **config)
        self.add_defaults(BuiltinCurrentScreen.defaults + defaults)

    def update_text(self):
        super().update_text()
        if self.qtile.current_screen == self.bar.screen:
            self.background = self.active_background_color
            self.update(self.active_text)
        else:
            self.background = self.inactive_background_color
            self.update(self.inactive_text)
        self.draw()


class Terminator(TextBox):
    def __init__(self, hack_offset: int = -1, **config: Any) -> None:
        super().__init__(**config)
        self.hack_offset = hack_offset

    def draw(self):
        if not self.can_draw():
            return
        self.drawer.clear(self.background or self.bar.background)

        # size = self.bar.height if self.bar.horizontal else self.bar.width
        self.drawer.ctx.save()

        if not self.bar.horizontal:
            # Left bar reads bottom to top
            if self.bar.screen.left is self.bar:
                self.drawer.ctx.rotate(-90 * math.pi / 180.0)
                self.drawer.ctx.translate(-self.length, 0)

            # Right bar is top to bottom
            else:
                self.drawer.ctx.translate(self.bar.width, 0)

                self.drawer.ctx.rotate(90 * math.pi / 180.0)

        size = self.bar.height if self.bar.horizontal else self.bar.width

        self.layout.draw(
            (self.actual_padding or 0) - self._scroll_offset,
            int(size / 2.0 - self.layout.height / 2.0) + self.hack_offset,
        )
        self.drawer.ctx.restore()

        self.drawer.draw(
            # offsetx=self.offsetx, offsety=self.offsety - HACK_OFFSET, width=self.width, height=self.height + (HACK_OFFSET * 2)
            offsetx=self.offsetx,
            offsety=self.offsety,
            width=self.width,
            height=self.height,
        )

        # We only want to scroll if:
        # - User has asked us to scroll and the scroll width is smaller than the layout (should_scroll=True)
        # - We are still scrolling (is_scrolling=True)
        # - We haven't already queued the next scroll (scroll_queued=False)
        if self._should_scroll and self._is_scrolling and not self._scroll_queued:
            self._scroll_queued = True
            if self._scroll_offset == 0:
                interval = self.scroll_delay
            else:
                interval = self.scroll_interval
            self._scroll_timer = self.timeout_add(interval, self.do_scroll)


class DynamicTerminator(Terminator):
    def __init__(self, active_foreground: str, **config: Any):
        super().__init__(**config)
        self.active_foreground = active_foreground
        self.inactive_foreground = self.foreground

    def draw(self):
        super().draw()

    def _configure(self, qtile, bar):
        base._TextBox._configure(self, qtile, bar)
        hook.subscribe.current_screen_change(self.update_text)
        self.update_text()

    def update_text(self):
        if self.qtile.current_screen == self.bar.screen:
            self.foreground = self.active_foreground
        else:
            self.foreground = self.inactive_foreground
        self.draw()


class GenericVolume(GenPollText):
    def __init__(self, **config):
        super().__init__(**config)
        self.volume = 0
        self.func = self._poll_func
        self.update_interval = 0.2
        self._txt = ""
        self.mouse_callbacks = {
            **self.mouse_callbacks,
            "Button1": toggle_audio_profile,
            "Button4": increase_volume,
            "Button5": decrease_volume,
        }

    def _get_volume(self):
        result = subprocess.check_output("pulsemixer --get-volume".split())
        result = result.decode("utf-8").strip()
        return int(result.split()[0])

    def _poll_func(self):
        vol = self._get_volume()
        if vol != self.volume:
            self.volume = vol
            self._update_drawer()
        return self._txt

    def _update_drawer(self):
        full_block = "█"
        empty_block = "▓"
        progress_bar = (
            int(self.volume / 10) * full_block
            + (10 - int(self.volume / 10)) * empty_block
        )
        self._txt = f"{progress_bar} {str(self.volume).rjust(3)}% "

        subprocess.Popen(
            f"dunstify Volume: -h int:value:{self.volume} -u LOW".split(" ")
        )


class Volume(BuiltinVolume):
    def _update_drawer(self):
        super()._update_drawer()
        full_block = "█"
        empty_block = "▓"
        progress_bar = (
            int(self.volume / 10) * full_block
            + (10 - int(self.volume / 10)) * empty_block
        )
        self.text = f" {progress_bar} {str(self.volume).rjust(3)}%"

        subprocess.Popen(["dunstify", f"Volume: ", "-h", f"int:value:{self.volume}"])


def left_terminator(foreground, background, fontsize=26):
    return Terminator(
        fmt="",
        foreground=foreground,
        background=background,
        fontsize=fontsize,
        padding=0,
        markup=False,
        hack_offset=-1,
        font="MesloLGS NF",
    )


def right_terminator(foreground, background, fontsize=26):
    return Terminator(
        fmt="",
        foreground=foreground,
        background=background,
        fontsize=fontsize,
        padding=0,
        markup=False,
        hack_offset=0,
        font="MesloLGS NF",
    )


class RightPowerline:
    def __init__(
        self,
        *widgets: List[_Widget],
        terminator_size: int = 24,
        background: str = kanagawa.base00,
    ) -> None:
        self._widgets = []
        first = widgets[0]
        self._widgets.append(
            left_terminator(first.background, background, terminator_size)
        )
        for i in range(len(widgets)):
            current = widgets[i]
            self._widgets.append(current)
            if i == len(widgets) - 1:
                break
            next = widgets[i + 1]
            self._widgets.append(
                left_terminator(next.background, current.background, terminator_size)
            )

    @property
    def widgets(self) -> List[_Widget]:
        return self._widgets


class LeftPowerline:
    def __init__(
        self,
        *widgets: Union[_Widget, Tuple[_Widget, ...]],
        terminator_size: int = 24,
        background: str = kanagawa.base00,
    ) -> None:
        self._widgets = []
        for i in range(len(widgets)):
            current = widgets[i]
            if isinstance(current, Iterable):
                current = current[0]
                for w in widgets[i]:
                    self._widgets.append(w)
            else:
                self._widgets.append(current)
            if i == len(widgets) - 1:
                break
            next = widgets[i + 1]
            if isinstance(next, Iterable):
                next = next[0]
            self._widgets.append(
                right_terminator(current.background, next.background, terminator_size)
            )
        last = widgets[-1]
        if isinstance(last, Iterable):
            last = last[-1]
        self._widgets.append(
            right_terminator(last.background, background, terminator_size)
        )

    @property
    def widgets(self) -> List[_Widget]:
        return self._widgets


def _parse_text(text: str):
    text = text.lower()
    if " - " in text:
        text = text.split(" - ")[-1]
    if "google chrome" in text:
        text = "chrome"
    elif "firefox" in text:
        text = "firefox"
    elif "visual studio code" in text:
        text = "vscode"
    elif "edge" in text:
        text = "edge"
    elif "nvim" in text:
        text = text.split("/")[-1]
    return text.lower()


def shared_task_list():
    return widget.TaskList(
        parse_text=_parse_text,
        background=kanagawa.base00,
        foreground=kanagawa.base05,
        highlight_method="border",
        rounded=True,
        icon_size=0,
        margin_x=3,
        margin_y=1,
        max_title_width=150,
        title_width_method="uniform",
        width=200,
        borderwidth=2,
        border=kanagawa.base09,
        unfocused_border=kanagawa.base03,
    )
