from typing import NamedTuple


class Command(NamedTuple):
    name: str
    command: str
    description: str

    def as_command_set_dict(self):
        return {self.name: self.command}


commands = [
    Command("nvim", "kitty -e nvim", "Launch Neovim"),
    Command("code", "code", "Launch VSCode"),
    Command("browser", "qutebrowser", "Launch qutebrowser"),
    Command("chrome", "google-chrome-stable", "Launch Chrome"),
    Command(
        "edge",
        'microsoft-edge-stable --proxy-server="http://192.168.0.119:8899;https://192.168.0.119:8899"',
        "Launch Edge using proxy",
    ),
    Command("postman", "postman", "Launch Postman"),
    Command("slack", "slack", "Launch Slack"),
    Command("discord", "discord", "Launch Discord"),
    Command("audio", "pavucontrol -t 5", "Launch Audio Settings"),
    Command("spotify", "flatpak run com.spotify.Client", "Launch Spotify"),
]
