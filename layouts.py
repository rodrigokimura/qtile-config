from libqtile import layout


class Columns(layout.Columns):
    def cmd_shuffle_left(self):
        cur = self.cc
        client = cur.cw
        if client is None:
            return
        if self.current <= 0 and len(cur) <= 1:
            # Move to left screen
            screen_idx = client.qtile.current_screen.index - 1
            if screen_idx < 0:
                return
            try:
                client.cmd_toscreen(screen_idx)
                client.qtile.focus_screen(screen_idx, False)
            except IndexError:
                return
            return
        super().cmd_shuffle_left()

    def cmd_shuffle_right(self):
        cur = self.cc
        client = cur.cw
        if client is None:
            return
        if self.current + 1 >= len(self.columns) and len(cur) <= 1:
            # Move to right screen
            screen_idx = client.qtile.current_screen.index + 1
            try:
                client.cmd_toscreen(screen_idx)
                client.qtile.focus_screen(screen_idx, False)
            except IndexError:
                return
            return
        super().cmd_shuffle_right()

    def cmd_left(self):
        if self.current > 0:
            self.current = self.current - 1
            self.group.focus(self.cc.cw, True)
        else:
            # Focus left screen
            screen_idx = self.group.qtile.current_screen.index - 1
            if screen_idx < 0:
                return
            try:
                self.group.qtile.focus_screen(screen_idx, False)
            except IndexError:
                return
            return

    def cmd_right(self):
        if len(self.columns) - 1 > self.current:
            self.current = self.current + 1
            self.group.focus(self.cc.cw, True)
        else:
            # Focus right screen
            screen_idx = self.group.qtile.current_screen.index + 1
            try:
                self.group.qtile.focus_screen(screen_idx, False)
            except IndexError:
                return
            return
