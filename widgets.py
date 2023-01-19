import math
from typing import Any, List

from libqtile import widget
from libqtile.widget.base import _Widget
from libqtile.widget.textbox import TextBox

from colors import Color


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
    widgets: List[_Widget]

    def __init__(
        self,
        *widgets: List[_Widget],
        terminator_size: int = 24,
        background: str = Color.BACKGROUND.value
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
    widgets: List[_Widget]

    def __init__(
        self,
        *widgets: List[_Widget],
        terminator_size: int = 24,
        background: str = Color.BACKGROUND.value
    ) -> None:
        self._widgets = []
        for i in range(len(widgets)):
            current = widgets[i]
            self._widgets.append(current)
            if i == len(widgets) - 1:
                break
            next = widgets[i + 1]
            self._widgets.append(
                right_terminator(current.background, next.background, terminator_size)
            )
        last = widgets[-1]
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
    if "firefox" in text:
        text = "firefox"
    if "visual studio code" in text:
        text = "vscode"
    if "edge" in text:
        text = "edge"
    return text.lower()


def shared_task_list():
    return widget.TaskList(
        parse_text=_parse_text,
        border=Color.GREEN.value,
        foreground=Color.GREEN.value,
        highlight_method="border",
        rounded=True,
        icon_size=0,
    )
