from libqtile import hook, layout
from libqtile.config import Match

from colors import Color
from keys import keys, mouse
from layouts import layouts
from screens import screens
from scripts import generate_wallpapers, start_compositor

keys = keys
mouse = mouse
layouts = layouts

widget_defaults = dict(
    font="Cascadia Code",
    fontsize=16,
    padding=2,
)
extension_defaults = widget_defaults.copy()

screens = screens


dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = False
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
        Match(wm_class="flameshot"),
    ],
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wmname = "qtile"


@hook.subscribe.startup
def autostart(*args, **kwargs):
    start_compositor()
    generate_wallpapers(screens)
